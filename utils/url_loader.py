import requests
import re
from bs4 import BeautifulSoup


def load_url_text(url: str) -> str:
    """
    RippleTruth URL Loader (Human-Readable Version)
    Fetches and converts webpages into clean text.
    Handles:
      • paywalls
      • bot blocks
      • 403/404/429/5xx situations
      • script/style/nav/footer stripping
    Produces clean narrative-ready input for:
      - RippleScan
      - Intention Math
      - Traceback Engine
    """

    # -----------------------------------------------------
    # FETCH HTML (friendly fail messages)
    # -----------------------------------------------------
    try:
        response = requests.get(
            url,
            timeout=10,
            headers={
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/124.0 Safari/537.36 RippleTruth/1.0"
                )
            }
        )

        status = response.status_code

        # --- Handle Known Error Codes ---
        if status == 403:
            return (
                "[403 Forbidden — Request Blocked]\n\n"
                "This website blocks automated scraping or requires a login.\n"
                "RippleTruth cannot access this URL directly.\n\n"
                "Fix Options:\n"
                "• Open it in your browser and copy/paste the article text\n"
                "• Try another publicly accessible news source\n"
            )

        if status == 404:
            return (
                "[404 Not Found]\n\n"
                "The link is broken or the page was removed."
            )

        if status == 429:
            return (
                "[429 Rate Limited]\n\n"
                "The website is temporarily blocking automated requests.\n"
                "Try again later or paste the text manually."
            )

        if status >= 500:
            return (
                f"[Server Error — {status}]\n\n"
                "The website is temporarily unavailable.\n"
                "Try again in a few minutes."
            )

        # Raise for unexpected HTTP failures
        response.raise_for_status()

    except requests.exceptions.Timeout:
        return (
            "[Connection Timeout]\n\n"
            "The website took too long to respond.\n"
            "Try loading it in your browser first, or paste the text manually."
        )

    except requests.exceptions.SSLError:
        return (
            "[SSL Error]\n\n"
            "The site uses a certificate configuration RippleTruth cannot validate."
        )

    except Exception as e:
        return f"[Unexpected URL Error: {str(e)}]"

    # -----------------------------------------------------
    # EXTRACT + CLEAN TEXT
    # -----------------------------------------------------
    html = response.text

    # Detect common paywall blocks
    if "enable javascript" in html.lower() or "subscribe" in html.lower():
        return (
            "[Blocked by Paywall / JS Renderer]\n\n"
            "This site requires JavaScript rendering or a subscription.\n"
            "RippleTruth cannot access it.\n\n"
            "Copy/paste the article text instead."
        )

    try:
        soup = BeautifulSoup(html, "html.parser")

        # Remove scripts, styles, nav, footer
        for tag in soup(["script", "style", "noscript", "header", "footer", "nav"]):
            tag.decompose()

        # Get raw text with paragraph structure
        text = soup.get_text(separator="\n")

        # Remove junk lines
        junk_patterns = [
            r"^\s*advertisement\s*$",
            r"^\s*subscribe\s*$",
            r"^\s*menu\s*$",
            r"^\s*sign in\s*$",
        ]

        cleaned_lines = []
        for line in text.split("\n"):
            line = line.strip()
            if not line:
                continue
            if any(re.match(p, line, re.IGNORECASE) for p in junk_patterns):
                continue
            cleaned_lines.append(line)

        final_text = "\n\n".join(cleaned_lines)

        # Collapse excessive whitespace inside lines
        final_text = re.sub(r"\s{2,}", " ", final_text).strip()

        if len(final_text) < 60:
            return (
                "[Readable Text Not Found]\n\n"
                "The page loaded successfully, but contained very little "
                "extractable article content.\n"
                "It may be:\n"
                "• An image-only article\n"
                "• A paywalled article\n"
                "• A script-rendered page\n\n"
                "Try pasting the text manually."
            )

        return final_text

    except Exception as e:
        return f"[HTML Parsing Error: {e}]"
