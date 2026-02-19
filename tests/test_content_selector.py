"""
Tests for main content selection.

Validates deterministic selection order: main -> article -> body.
"""
import pytest
from bs4 import BeautifulSoup
from flowdoc.core.content_selector import select_main_content


def test_selects_main_when_present():
    """Returns <main> when it exists."""
    html = "<body><nav>Skip</nav><main>Content</main></body>"
    soup = BeautifulSoup(html, "lxml")
    result = select_main_content(soup)
    assert result.name == "main"
    assert "Content" in result.get_text()


def test_selects_article_when_no_main():
    """Falls back to <article> when no <main>."""
    html = "<body><nav>Skip</nav><article>Content</article></body>"
    soup = BeautifulSoup(html, "lxml")
    result = select_main_content(soup)
    assert result.name == "article"


def test_selects_body_when_no_main_or_article():
    """Falls back to <body> when neither <main> nor <article> exist."""
    html = "<body><p>Just body content</p></body>"
    soup = BeautifulSoup(html, "lxml")
    result = select_main_content(soup)
    assert result.name == "body"


def test_prefers_main_over_article():
    """Prefers <main> when both <main> and <article> exist."""
    html = "<body><article>Article</article><main>Main</main></body>"
    soup = BeautifulSoup(html, "lxml")
    result = select_main_content(soup)
    assert result.name == "main"
    assert "Main" in result.get_text()


# Note: We don't test the "no body" error case because HTML parsers (lxml)
# automatically add <body> tags during parsing, making this scenario impossible
# to trigger in practice. The ValueError in content_selector.py remains as
# defensive coding.