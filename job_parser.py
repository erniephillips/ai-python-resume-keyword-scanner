import requests
from bs4 import BeautifulSoup

def extract_text_from_txt(txt_path):
    """Reads job description from a text file."""
    with open(txt_path, "r", encoding="utf-8") as file:
        return file.read().strip()

def extract_text_from_url(url):
    """
    Fetches the page at the URL using enhanced headers to mimic a real browser
    and extracts its text using BeautifulSoup.
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/115.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Referer": url
    }

    response = requests.get(url, headers=headers, timeout=10)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch URL: {url} with status code {response.status_code}")

    soup = BeautifulSoup(response.text, "html.parser")
    return soup.get_text(separator=" ", strip=True)
