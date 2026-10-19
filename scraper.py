
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/131.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
}


def fetch_website_contents(url):
    url = url.strip()

    if not url:
        raise ValueError("Please enter a website URL.")

    # Add HTTPS if the user omitted the protocol
    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    parsed = urlparse(url)

    if not parsed.hostname or "." not in parsed.hostname:
        raise ValueError("Please enter a valid website URL.")

    try:
        response = requests.get(
            url,
            headers=HEADERS,
            timeout=20,
            allow_redirects=True
        )
        response.raise_for_status()

    except requests.exceptions.Timeout as e:
        raise RuntimeError(
            "The website request timed out. Please try again."
        ) from e

    except requests.exceptions.ConnectionError as e:
        raise RuntimeError(
            "Connection failed. The domain may have a DNS problem, "
            "the server may be unavailable, or the website may block "
            "requests from the app's server."
        ) from e

    except requests.exceptions.HTTPError as e:
        status = (
            e.response.status_code
            if e.response is not None
            else "unknown"
        )
        raise RuntimeError(
            f"The website returned HTTP status {status}."
        ) from e

    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Website request failed: {e}") from e

    content_type = response.headers.get("Content-Type", "").lower()

    if "html" not in content_type:
        raise RuntimeError("The URL did not return an HTML webpage.")

    soup = BeautifulSoup(response.text, "html.parser")

    title = (
        soup.title.get_text(strip=True)
        if soup.title
        else "No title found"
    )

    for tag in soup([
        "script", "style", "nav", "footer", "header",
        "img", "input", "noscript", "svg"
    ]):
        tag.decompose()

    text = soup.get_text(separator="\n", strip=True)

    if not text:
        raise RuntimeError(
            "The page contains no readable text. It may require "
            "JavaScript to load its content."
        )

    # Limit the amount of text sent to the LLM
    text = text[:20000]

    return (
        f"Website URL: {response.url}\n"
        f"Title: {title}\n\n"
        f"Page contents:\n{text}"
    )
