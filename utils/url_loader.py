import requests
import re


def load_url_text(url: str) -> str:
    """
    Downloads webpage text with friendly, human-readable error messages.
    RippleTruth often hits bot-blockers, paywalls, and 403/503 defenses.
    This function explains WHY a URL failed and HOW the user can fix it.
    """

    try:
        response = requests.get(
            url,
            timeout=10,
            headers={
                "User-Agent": "Mozilla/5.0 (compatible; RippleTruth/1.0)"
            }
        )

        # Handle known HTTP status codes gracefully
        if response.status_code == 403:
            return (
                "[URL Fetch Blocked — 403 Forbidden]\n\n"
                "The website rejected RippleTruth's request.\n"
                "This usually happens because:\n"
                "• The site blocks bots and automated scrapers\n"
                "• The URL requires login or session cookies\n"
                "• The firewall detected a non-browser request\n\n"
                "Try again using a public news article or copy/paste the text."
            )

        if response.status_code == 404:
            return (
                "[URL Not Found — 404]\n\n"
                "The webpage does not exist or the link was mistyped."
            )

        if response.status_code == 429:
            return (
                "[Rate Limited — 429 Too Many Requests]\n\n"
                "The site is rate-limiting automated requests.\n"
                "Try again in a few minutes, or paste the text manually."
            )

        if response.status_code >= 500:
            return (
                f"[Server Error — {response.status_code}]\n\n"
                "The website is temporarily unavailable.\n"
                "This is not a RippleTruth issue."
            )

        # Raise for any other unexpected HTTP status
        response.raise_for_status()

    except requests.exceptions.Timeout:
        return (
            "[Connection Timeout]\n\n"
            "The site took too long to respond.\n"
            "Try loading it in your browser first or use text paste mode."
        )

    except requests.exceptions.SSLError:
        return (
            "[SSL Error]\n\n"
            "The website uses a certificate or HTTPS configuration "
            "that RippleTruth cannot validate."
        )

    except Exception as e:
        return f"[Error loading URL: {e}]"

    # -------------------------------
    # HTML extraction
    # -------------------------------
    html = response.text

    # Remove scripts and styles
    html = re.sub(r"<script.*?>.*?</script>", "", html, flags=re.DOTALL)
    html = re.sub(r"<style.*?>.*?</style>", "", html, flags=re.DOTALL)

    # Remove HTML tags
    text = re.sub(r"<[^>]+>", " ", html)

    # Collapse whitespace
    text = re.sub(r"\s+", " ", text).strip()

    return text
