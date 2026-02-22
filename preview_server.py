"""
Flowdoc drag-drop preview server (dev tool only).

Runs the Flowdoc pipeline on uploaded HTML files and returns
converted output for visual inspection in a browser.

Usage (from project root):
    python preview_server.py
Then open http://localhost:5000 in a browser.
"""
from flask import Flask, request
import os

from flowdoc.core.sanitizer import sanitize
from flowdoc.core.parser import parse
from flowdoc.core.renderer import render

app = Flask(__name__)

PREVIEW_HTML = os.path.join(os.path.dirname(os.path.abspath(__file__)), "preview.html")


@app.route("/")
def index():
    """Serve the drag-drop preview page."""
    with open(PREVIEW_HTML, "r", encoding="utf-8") as f:
        return f.read()


@app.route("/convert", methods=["POST"])
def convert():
    """
    Accept uploaded HTML, run Flowdoc pipeline, return converted HTML.

    Form fields:
        file - HTML file to convert (required)
        font - optional; pass 'opendyslexic' to enable font toggle
    """
    f = request.files.get("file")
    if not f:
        return "No file received", 400

    raw_html = f.read().decode("utf-8", errors="replace")
    font = request.form.get("font", None)

    try:
        clean = sanitize(raw_html)
        doc = parse(clean)
        use_opendyslexic = (font == "opendyslexic")
        output = render(doc, use_opendyslexic=use_opendyslexic)
        return output, 200, {"Content-Type": "text/html; charset=utf-8"}
    except ValueError as e:
        # Validation error - non-semantic HTML, missing structure, etc.
        return f"<pre>Validation error: {e}</pre>", 422
    except Exception as e:
        return f"<pre>Error: {e}</pre>", 500


if __name__ == "__main__":
    app.run(debug=True, port=5000)