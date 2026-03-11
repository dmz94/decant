"""
Flask application for the Decant hosted surface.

Routes:
    GET  /        — Serve the index page.
    POST /convert — Accept URL or file, return converted HTML as JSON.
"""
import logging
import time
from functools import wraps

from flask import Flask, request, jsonify, render_template

import config
from convert import convert_url, convert_file, ConvertError
from fetch import FetchError

app = Flask(__name__)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)
log = logging.getLogger("decant")


# ---------------------------------------------------------------------------
# HTTP Basic Auth
# ---------------------------------------------------------------------------

def _check_auth(username: str, password: str) -> bool:
    return (
        username == config.BASIC_AUTH_USERNAME
        and password == config.BASIC_AUTH_PASSWORD
    )


def _auth_required_response():
    return (
        jsonify({"status": "error", "message": "Authentication required."}),
        401,
        {"WWW-Authenticate": 'Basic realm="Decant"'},
    )


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not config.BASIC_AUTH_ENABLED:
            return f(*args, **kwargs)
        auth = request.authorization
        if not auth or not _check_auth(auth.username, auth.password):
            return _auth_required_response()
        return f(*args, **kwargs)
    return decorated


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@app.route("/")
@requires_auth
def index():
    prefilled_url = request.args.get("url", "")
    return render_template("index.html", prefilled_url=prefilled_url)


@app.route("/convert", methods=["POST"])
@requires_auth
def convert():
    start = time.monotonic()
    source = None

    try:
        # File upload takes precedence
        uploaded = request.files.get("file")
        if uploaded and uploaded.filename:
            source = "file_upload"
            html_bytes = uploaded.read()
            converted_html, source_url = convert_file(html_bytes)
        else:
            url = request.form.get("url", "").strip()
            if not url:
                return jsonify({
                    "status": "error",
                    "message": "Please provide a URL or upload a file.",
                }), 422
            source = url
            converted_html, source_url = convert_url(url)

        elapsed_ms = int((time.monotonic() - start) * 1000)
        log.info("convert OK source=%s elapsed=%dms", source, elapsed_ms)

        return jsonify({
            "status": "ok",
            "html": converted_html,
        })

    except FetchError as e:
        elapsed_ms = int((time.monotonic() - start) * 1000)
        log.warning(
            "convert FETCH_ERROR source=%s error=%s elapsed=%dms",
            source, e, elapsed_ms,
        )
        return jsonify({
            "status": "error",
            "message": e.user_message,
        }), 422

    except ConvertError as e:
        elapsed_ms = int((time.monotonic() - start) * 1000)
        log.warning(
            "convert CONVERT_ERROR source=%s error=%s elapsed=%dms",
            source, e, elapsed_ms,
        )
        return jsonify({
            "status": "error",
            "message": e.user_message,
        }), 422

    except Exception:
        elapsed_ms = int((time.monotonic() - start) * 1000)
        log.exception(
            "convert UNEXPECTED_ERROR source=%s elapsed=%dms",
            source, elapsed_ms,
        )
        return jsonify({
            "status": "error",
            "message": "Something went wrong on our end. Try again in a moment.",
        }), 500


if __name__ == "__main__":
    app.run(debug=True, port=5001)
