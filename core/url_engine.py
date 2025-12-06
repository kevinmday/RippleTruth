# core/url_engine.py

import requests
from bs4 import BeautifulSoup

def fetch_url_text(url: str) -> str:
    """
    Fetches the webpage, extracts readable article text,
    removes scripts, navbars, duplicate junk.
    """
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
    except Exception as e:
        return f"[URL fetch error: {e}]"

    soup = BeautifulSoup(resp.text, "html.parser")

    # Remove script/junk
    for tag in soup(["script", "style", "header", "footer", "nav", "aside"]):
        tag.extract()

    # Strategy: get longest text block (best heuristic for article)
    paragraphs = [p.get_text(strip=True) for p in soup.find_all("p")]
    text = "\n".join(p for p in paragraphs if len(p) > 40)

    if not text:
        return "[No extractable article text found]"

    return text
