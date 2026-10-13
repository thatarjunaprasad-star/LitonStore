import requests
from bs4 import BeautifulSoup
from typing import List, Dict
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def _fetch(url: str) -> str:
    """Fetch the HTML content of a URL with a fallback timeout."""
    try:
        resp = requests.get(url, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
        resp.raise_for_status()
        return resp.text
    except Exception as e:
        logger.error(f"Failed to fetch {url}: {e}")
        return ""

def scrape_daraz(search_term: str = "tea") -> List[Dict]:
    """Scrape Daraz Bangladesh for a given search term.

    Returns a list of dictionaries with keys: name, price, url.
    The implementation uses generic selectors – you may need to adjust them
    based on the current site layout.
    """
    base = "https://www.daraz.com.bd/catalog/"
    query = f"{search_term}/"
    url = base + query
    html = _fetch(url)
    if not html:
        return []
    soup = BeautifulSoup(html, "html.parser")
    items = []
    for card in soup.select("div[data-qa] .c3e8"):
        # NOTE: selectors are illustrative; adjust to real page.
        name_el = card.select_one('a[data-qa="product-name"]')
        price_el = card.select_one('span[data-qa="price"]')
        if not name_el or not price_el:
            continue
        name = name_el.get_text(strip=True)
        price = price_el.get_text(strip=True).replace("৳", "").replace(",", "")
        link = name_el["href"]
        if not link.startswith("http"):
            link = "https://www.daraz.com.bd" + link
        items.append({"name": name, "price": price, "url": link})
    logger.info(f"Daraz scraped {len(items)} items for term '{search_term}'.")
    return items

def scrape_ajkerdeal(search_term: str = "tea") -> List[Dict]:
    """Scrape AjkerDeal Bangladesh for a given search term.

    Returns a list of dictionaries with keys: name, price, url.
    """
    base = "https://ajkerdeal.com/search/"
    url = f"{base}{search_term}"
    html = _fetch(url)
    if not html:
        return []
    soup = BeautifulSoup(html, "html.parser")
    items = []
    for card in soup.select("div.product-item"):
        name_el = card.select_one("h2.product-title a")
        price_el = card.select_one("span.price")
        if not name_el or not price_el:
            continue
        name = name_el.get_text(strip=True)
        price = price_el.get_text(strip=True).replace("৳", "").replace(",", "")
        link = name_el["href"]
        if not link.startswith("http"):
            link = "https://ajkerdeal.com" + link
        items.append({"name": name, "price": price, "url": link})
    logger.info(f"AjkerDeal scraped {len(items)} items for term '{search_term}'.")
    return items

def scrape_all_sites(search_term: str = "tea") -> List[Dict]:
    """Aggregate data from all supported e‑commerce sites.

    This function can be extended with more site‑specific scrapers.
    """
    results: List[Dict] = []
    for func in (scrape_daraz,):
        try:
            results.extend(func(search_term))
        except Exception as e:
            logger.error(f"Error scraping with {func.__name__}: {e}")
    return results
