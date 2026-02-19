"""
Main content selection from sanitized DOM.

Implements deterministic content selection: main -> article -> body.
See decisions.md section 4 for selection rules.
"""
from bs4 import BeautifulSoup, Tag


def select_main_content(soup: BeautifulSoup) -> Tag:
    """
    Select main content area from DOM tree.
    
    Selection order (deterministic):
    1. First <main> element
    2. First <article> element  
    3. <body> element
    
    Navigation, headers, footers, and sidebars are excluded by selection.
    
    Args:
        soup: BeautifulSoup parsed DOM tree
        
    Returns:
        Tag object representing the main content subtree
        
    Raises:
        ValueError: If no body element exists (malformed HTML)
    """
    main = soup.find("main")
    if main:
        return main
    
    article = soup.find("article")
    if article:
        return article
    
    body = soup.find("body")
    if body:
        return body
    
    raise ValueError("No body element found in HTML")