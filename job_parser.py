import requests
from random import choice
from boilerpy3 import extractors

# List of user agents to rotate through
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.1 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/109.0",
    "Mozilla/5.0 (Linux; Android 10; SM-G973U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Mobile Safari/537.36"
]


def extract_text_from_txt(txt_file):
    """Extracts text from a text file file-like object."""
    try:
        text = txt_file.read().decode("utf-8")
    except AttributeError:
        text = txt_file.read()
    return text.strip()


def extract_text_from_url(url):
    """
    Fetches the page at the URL using randomized headers to mimic a real browser
    and extracts its main content using boilerpy3's ArticleExtractor.

    If the website returns a 403 status code, it raises an exception with a friendly message.
    """
    headers = {
        "User-Agent": choice(USER_AGENTS),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Referer": url
    }

    response = requests.get(url, headers=headers, timeout=10)

    if response.status_code == 403:
        raise Exception(
            f"Access to URL {url} was forbidden (status code 403). "
            "This website may be blocking automated scraping. Please try providing the job description as a file instead."
        )
    elif response.status_code != 200:
        raise Exception(f"Failed to fetch URL: {url} with status code {response.status_code}")

    # Use the ArticleExtractor from boilerpy3 to extract the main content.
    extractor = extractors.ArticleExtractor()
    content = extractor.get_content(response.text)
    return content.strip()
