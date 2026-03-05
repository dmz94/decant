"""
Degradation rules for unsupported HTML elements.

Converts tables, images, forms, and other unsupported elements into
placeholder model objects. See decisions.md section 7 for rules.
"""
from urllib.parse import urlparse

from bs4 import Tag
from flowdoc.core.model import Image, Paragraph, Text


def degrade_table(element: Tag) -> Paragraph:
    """
    Convert table to placeholder text with dimensions.
    
    v2 consideration: Simple tables could be rendered with readable styling.
    
    Args:
        element: BeautifulSoup Tag for <table>
        
    Returns:
        Paragraph with placeholder text showing row/column count
    """
    rows = element.find_all("tr")
    row_count = len(rows)
    
    # Find max columns across all rows
    col_count = 0
    for row in rows:
        cells = row.find_all(["td", "th"])
        col_count = max(col_count, len(cells))
    
    text = f"[Table omitted - {row_count} rows, {col_count} columns]"
    return Paragraph(inlines=[Text(text=text)])


def degrade_image(element: Tag) -> Image | Text:
    """
    Preserve image when src is http/https, otherwise placeholder.

    Per decisions.md section 7: images with external URLs are rendered
    as <img> tags. Images without valid src degrade to WARN placeholder.

    Args:
        element: BeautifulSoup Tag for <img>

    Returns:
        Image when src is http/https, Text placeholder otherwise
    """
    src = element.get("src", "").strip()
    alt = element.get("alt", "").strip()

    if src:
        scheme = urlparse(src).scheme.lower()
        if scheme in ("http", "https"):
            return Image(src=src, alt=alt)

    # Fallback: WARN placeholder
    if alt:
        text = f"[Image: {alt}]"
    else:
        text = "[Image not included]"

    return Text(text=text)


def degrade_form(element: Tag) -> Paragraph:
    """
    Convert form to placeholder.
    
    Forms are interactive and incompatible with static readable output.
    Will not be supported in future versions.
    
    Args:
        element: BeautifulSoup Tag for form element
        
    Returns:
        Paragraph with static placeholder
    """
    return Paragraph(inlines=[Text(text="[Form omitted]")])


def degrade_hr() -> Paragraph:
    """
    Convert horizontal rule to visual separator.
    
    v2 consideration: Could render as actual CSS border for visual clarity.
    
    Returns:
        Paragraph with separator token
    """
    return Paragraph(inlines=[Text(text="[-]")])