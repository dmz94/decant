/* Decant surface — vanilla JS, no framework. */

(function () {
  "use strict";

  var urlForm = document.getElementById("url-form");
  var urlInput = document.getElementById("url-input");
  var dropZone = document.getElementById("drop-zone");
  var fileInput = document.getElementById("file-input");
  var outputSection = document.getElementById("output");
  var outputFrame = document.getElementById("output-frame");
  var sourceUrlSpan = document.getElementById("source-url");
  var errorDiv = document.getElementById("error");

  // --- Helpers ---

  function showError(message) {
    errorDiv.textContent = message;
    errorDiv.classList.remove("hidden");
    outputSection.classList.add("hidden");
  }

  function hideError() {
    errorDiv.classList.add("hidden");
  }

  function showLoading() {
    hideError();
    outputSection.classList.remove("hidden");
    sourceUrlSpan.textContent = "";
    outputFrame.removeAttribute("srcdoc");
    outputFrame.srcdoc = "<p style='padding:2rem;color:#888;font-family:system-ui'>Converting\u2026</p>";
  }

  function showResult(html, sourceUrl) {
    hideError();
    outputSection.classList.remove("hidden");
    outputFrame.srcdoc = html;
    if (sourceUrl) {
      sourceUrlSpan.textContent = sourceUrl;
    } else {
      sourceUrlSpan.textContent = "uploaded file";
    }
  }

  // --- Convert via URL ---

  function convertUrl(url) {
    showLoading();
    var formData = new FormData();
    formData.append("url", url);

    fetch("/convert", { method: "POST", body: formData })
      .then(function (resp) { return resp.json(); })
      .then(function (data) {
        if (data.status === "ok") {
          showResult(data.html, url);
        } else {
          showError(data.message || "Conversion failed.");
        }
      })
      .catch(function () {
        showError("Network error. Check your connection and try again.");
      });
  }

  // --- Convert via file ---

  function convertFile(file) {
    showLoading();
    var formData = new FormData();
    formData.append("file", file);

    fetch("/convert", { method: "POST", body: formData })
      .then(function (resp) { return resp.json(); })
      .then(function (data) {
        if (data.status === "ok") {
          showResult(data.html, "");
        } else {
          showError(data.message || "Conversion failed.");
        }
      })
      .catch(function () {
        showError("Network error. Check your connection and try again.");
      });
  }

  // --- Event listeners ---

  urlForm.addEventListener("submit", function (e) {
    e.preventDefault();
    var url = urlInput.value.trim();
    if (url) {
      convertUrl(url);
    }
  });

  // Drop zone click -> trigger file picker
  dropZone.addEventListener("click", function () {
    fileInput.click();
  });

  fileInput.addEventListener("change", function () {
    if (fileInput.files.length > 0) {
      convertFile(fileInput.files[0]);
    }
  });

  // Drag and drop
  ["dragenter", "dragover"].forEach(function (evt) {
    dropZone.addEventListener(evt, function (e) {
      e.preventDefault();
      e.stopPropagation();
      dropZone.classList.add("dragover");
    });
  });

  ["dragleave", "drop"].forEach(function (evt) {
    dropZone.addEventListener(evt, function (e) {
      e.preventDefault();
      e.stopPropagation();
      dropZone.classList.remove("dragover");
    });
  });

  dropZone.addEventListener("drop", function (e) {
    var files = e.dataTransfer.files;
    if (files.length > 0) {
      convertFile(files[0]);
    }
  });

  // Prevent default drag on the whole page
  document.addEventListener("dragover", function (e) { e.preventDefault(); });
  document.addEventListener("drop", function (e) { e.preventDefault(); });

  // --- Prefilled URL auto-submit ---

  if (window.__prefilled_url) {
    urlInput.value = window.__prefilled_url;
    convertUrl(window.__prefilled_url);
  }
})();
