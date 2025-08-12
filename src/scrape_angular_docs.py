import json
import os
import sys
from typing import List, Dict

import requests
from bs4 import BeautifulSoup

SITEMAP_URL = "https://angular.io/sitemap.xml"


def fetch_sitemap(url: str = SITEMAP_URL) -> str:
    """Download the sitemap XML from the Angular documentation site."""
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return response.text


def parse_sitemap(xml: str) -> List[str]:
    """Extract documentation URLs from the sitemap XML."""
    soup = BeautifulSoup(xml, "xml")
    urls = [loc.text for loc in soup.find_all("loc")]
    doc_urls = [u for u in urls if "angular.io/guide/" in u or "angular.io/tutorial" in u]
    return doc_urls


def scrape_page(url: str) -> Dict[str, List[str]]:
    """Fetch a documentation page and extract text and code blocks."""
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    main = soup.find("main") or soup
    text = main.get_text(separator=" ", strip=True)
    code_blocks = [pre.get_text("\n", strip=True) for pre in main.find_all("pre")]
    return {"url": url, "text": text, "code_blocks": code_blocks}


def scrape_docs(output_path: str, limit: int | None = None) -> None:
    """Scrape Angular docs and save them as a JSON array."""
    xml = fetch_sitemap()
    urls = parse_sitemap(xml)
    if limit is not None:
        urls = urls[:limit]

    results: List[Dict[str, List[str]]] = []
    for url in urls:
        try:
            results.append(scrape_page(url))
        except Exception as exc:  # pragma: no cover - network errors
            print(f"Failed to scrape {url}: {exc}", file=sys.stderr)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Scrape Angular documentation.")
    parser.add_argument("output", help="Path to write the JSON output.")
    parser.add_argument("--limit", type=int, default=None, help="Optional limit on number of pages to scrape.")
    args = parser.parse_args()

    os.makedirs(os.path.dirname(args.output) or ".", exist_ok=True)
    scrape_docs(args.output, args.limit)
