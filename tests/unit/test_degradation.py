"""
Tests for HTML element degradation rules.

Validates placeholder generation for unsupported elements
and image preservation for images with external URLs.
"""
from bs4 import BeautifulSoup
from flowdoc.core.degradation import degrade_table, degrade_image, degrade_form, degrade_hr
from flowdoc.core.model import Image, Paragraph, Text


def test_table_counts_rows_and_columns():
    """Table placeholder includes correct dimensions."""
    html = "<table><tr><td>A</td><td>B</td></tr><tr><td>C</td><td>D</td></tr></table>"
    soup = BeautifulSoup(html, "lxml")
    element = soup.find("table")
    result = degrade_table(element)

    assert isinstance(result, Paragraph)
    assert len(result.inlines) == 1
    assert result.inlines[0].text == "[Table omitted - 2 rows, 2 columns]"


def test_table_handles_uneven_columns():
    """Table uses max column count across rows."""
    html = "<table><tr><td>A</td></tr><tr><td>B</td><td>C</td><td>D</td></tr></table>"
    soup = BeautifulSoup(html, "lxml")
    element = soup.find("table")
    result = degrade_table(element)

    assert result.inlines[0].text == "[Table omitted - 2 rows, 3 columns]"


# --- Image preservation (http/https src) ---

def test_image_with_https_src_preserved():
    """Image with https src returns Image model object."""
    html = '<img src="https://example.com/photo.jpg" alt="A sunset">'
    soup = BeautifulSoup(html, "lxml")
    element = soup.find("img")
    result = degrade_image(element)

    assert isinstance(result, Image)
    assert result.src == "https://example.com/photo.jpg"
    assert result.alt == "A sunset"


def test_image_with_http_src_preserved():
    """Image with http src returns Image model object."""
    html = '<img src="http://example.com/photo.jpg" alt="A photo">'
    soup = BeautifulSoup(html, "lxml")
    element = soup.find("img")
    result = degrade_image(element)

    assert isinstance(result, Image)
    assert result.src == "http://example.com/photo.jpg"
    assert result.alt == "A photo"


def test_image_with_https_src_no_alt():
    """Image with https src but no alt preserves with empty alt."""
    html = '<img src="https://example.com/photo.jpg">'
    soup = BeautifulSoup(html, "lxml")
    element = soup.find("img")
    result = degrade_image(element)

    assert isinstance(result, Image)
    assert result.src == "https://example.com/photo.jpg"
    assert result.alt == ""


# --- Image placeholder fallback ---

def test_image_with_alt_no_src_placeholder():
    """Image with alt but no src returns placeholder Text."""
    html = '<img alt="A beautiful sunset">'
    soup = BeautifulSoup(html, "lxml")
    element = soup.find("img")
    result = degrade_image(element)

    assert isinstance(result, Text)
    assert result.text == "[Image: A beautiful sunset]"


def test_image_without_alt_or_src():
    """Image without alt or src uses generic placeholder."""
    html = '<img>'
    soup = BeautifulSoup(html, "lxml")
    element = soup.find("img")
    result = degrade_image(element)

    assert isinstance(result, Text)
    assert result.text == "[Image not included]"


def test_image_with_empty_alt_no_src():
    """Image with empty alt and no src is treated as missing."""
    html = '<img alt="">'
    soup = BeautifulSoup(html, "lxml")
    element = soup.find("img")
    result = degrade_image(element)

    assert result.text == "[Image not included]"


def test_image_with_data_src_placeholder():
    """Image with data: src degrades to placeholder."""
    html = '<img src="data:image/png;base64,abc123" alt="Logo">'
    soup = BeautifulSoup(html, "lxml")
    element = soup.find("img")
    result = degrade_image(element)

    assert isinstance(result, Text)
    assert result.text == "[Image: Logo]"


def test_image_with_relative_src_placeholder():
    """Image with relative src (no scheme) degrades to placeholder."""
    html = '<img src="/images/photo.jpg" alt="Photo">'
    soup = BeautifulSoup(html, "lxml")
    element = soup.find("img")
    result = degrade_image(element)

    assert isinstance(result, Text)
    assert result.text == "[Image: Photo]"


# --- Form and HR (unchanged) ---

def test_form_returns_placeholder():
    """Form elements get static placeholder."""
    html = '<form><input type="text"></form>'
    soup = BeautifulSoup(html, "lxml")
    element = soup.find("form")
    result = degrade_form(element)

    assert isinstance(result, Paragraph)
    assert result.inlines[0].text == "[Form omitted]"


def test_hr_returns_separator():
    """HR becomes visual separator token."""
    result = degrade_hr()

    assert isinstance(result, Paragraph)
    assert result.inlines[0].text == "[-]"
