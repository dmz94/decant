"""
Tests for extract mode pipeline.

Validates extract mode behavior including known limitations.
Extract mode uses Trafilatura for boilerplate removal - formatting
preservation is best-effort, not guaranteed.

Known documented limitations in extract mode:
- <pre> code blocks are converted to <blockquote>
- Some inline spacing may be lost around inline elements
"""
import pytest
from pathlib import Path
from flowdoc.core.parser import parse, extract_with_trafilatura
from flowdoc.core.renderer import render


def test_extract_with_trafilatura_returns_string():
    """extract_with_trafilatura returns a non-empty string."""
    html = "<html><body><h1>Title</h1><p>Content</p></body></html>"
    result = extract_with_trafilatura(html)
    assert isinstance(result, str)
    assert len(result) > 0


def test_extract_with_trafilatura_falls_back_on_no_headings():
    """Falls back to original HTML if Trafilatura strips all headings."""
    html = "<html><body><p>No headings here at all</p></body></html>"
    result = extract_with_trafilatura(html)
    assert result == html


def test_extract_mode_preserves_headings():
    """Extract mode preserves heading structure."""
    fixture_path = Path(__file__).parent / "fixtures" / "input" / "simple_article.html"
    html = fixture_path.read_text(encoding='utf-8')
    extracted = extract_with_trafilatura(html)
    assert "<h1" in extracted
    assert "<h2" in extracted


def test_extract_mode_pre_becomes_blockquote():
    """
    Known limitation: <pre> blocks are converted to <blockquote> by Trafilatura.

    This is documented extract mode behavior, not a bug.
    Content is preserved, block type changes.
    In transform mode, <pre> is preserved correctly.
    """
    fixture_path = Path(__file__).parent / "fixtures" / "input" / "simple_article.html"
    html = fixture_path.read_text(encoding='utf-8')
    extracted = extract_with_trafilatura(html)
    # <pre> is converted - content should still be present
    assert "Hello, World" in extracted
    # <pre> tag is not preserved in extract mode
    assert "<pre>" not in extracted


def test_transform_mode_preserves_pre():
    """Transform mode preserves <pre> blocks exactly."""
    fixture_path = Path(__file__).parent / "fixtures" / "input" / "simple_article.html"
    html = fixture_path.read_text(encoding='utf-8')
    # Direct parse() call = transform mode (no Trafilatura)
    doc = parse(html)
    output = render(doc)
    assert "<pre>" in output


def test_transform_mode_preserves_strong():
    """Transform mode preserves <strong> inline formatting."""
    fixture_path = Path(__file__).parent / "fixtures" / "input" / "simple_article.html"
    html = fixture_path.read_text(encoding='utf-8')
    doc = parse(html)
    output = render(doc)
    assert "<strong>efficient high-level data structures</strong>" in output


def test_transform_mode_preserves_links():
    """Transform mode preserves links."""
    fixture_path = Path(__file__).parent / "fixtures" / "input" / "simple_article.html"
    html = fixture_path.read_text(encoding='utf-8')
    doc = parse(html)
    output = render(doc)
    assert 'href="https://python.org"' in output


def test_extract_mode_full_pipeline_wikipedia():
    """Extract mode processes Wikipedia fixture without crashing."""
    fixture_path = Path(__file__).parent / "fixtures" / "input" / "wikipedia_dyslexia.html"
    html = fixture_path.read_text(encoding='utf-8')
    extracted = extract_with_trafilatura(html)
    # Capture title before extraction
    from bs4 import BeautifulSoup
    original_soup = BeautifulSoup(html, "lxml")
    original_title = original_soup.find("title")
    doc = parse(extracted, original_title=original_title)
    output = render(doc)
    assert "<!DOCTYPE html>" in output
    assert len(output) > 1000
