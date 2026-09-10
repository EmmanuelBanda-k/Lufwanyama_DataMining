import requests
from bs4 import BeautifulSoup
from pathlib import Path
from urllib.parse import urljoin
import time
import urllib3

# ============================================================
# LUFWANYAMA TOWN COUNCIL DATA COLLECTOR
# CSC 4792 - DATA MINING AND WAREHOUSING
# ============================================================

# Disable SSL certificate warnings
urllib3.disable_warnings(
    urllib3.exceptions.InsecureRequestWarning
)

BASE_URL = "https://www.lufwanyamacouncil.gov.zm"

# Important council pages
PAGES = {
    "homepage": BASE_URL + "/",
    "cdf": BASE_URL + "/?page_id=1901",
    "publications": BASE_URL + "/?page_id=195"
}

# Raw data directory
RAW_DIR = Path("data/raw")
RAW_DIR.mkdir(parents=True, exist_ok=True)

# Pretend to be a normal web browser
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/153.0 Safari/537.36"
    )
}


# ============================================================
# DOWNLOAD WEB PAGE
# ============================================================

def download_page(name, url):

    print("\n" + "-" * 60)
    print(f"Downloading: {name}")
    print(url)

    try:

        response = requests.get(
            url,
            headers=HEADERS,
            timeout=30,
            verify=False
        )

        print("Status:", response.status_code)

        response.raise_for_status()

        file_path = RAW_DIR / f"{name}.html"

        file_path.write_text(
            response.text,
            encoding="utf-8"
        )

        print("Saved:", file_path)

        return response.text

    except Exception as error:

        print("ERROR:", error)

        return None


# ============================================================
# EXTRACT LINKS FROM PAGE
# ============================================================

def collect_links(html, source_url):

    soup = BeautifulSoup(
        html,
        "html.parser"
    )

    links = []

    for link in soup.find_all(
        "a",
        href=True
    ):

        href = link["href"]

        full_url = urljoin(
            source_url,
            href
        )

        text = link.get_text(
            " ",
            strip=True
        )

        links.append({
            "text": text,
            "url": full_url
        })

    return links


# ============================================================
# DOWNLOAD PDF
# ============================================================

def download_pdf(url, filename):

    try:

        print(f"Downloading PDF: {filename}")

        response = requests.get(
            url,
            headers=HEADERS,
            timeout=60,
            verify=False
        )

        response.raise_for_status()

        file_path = RAW_DIR / filename

        file_path.write_bytes(
            response.content
        )

        print("Saved:", file_path)

    except Exception as error:

        print("PDF ERROR:", error)


# ============================================================
# MAIN PROGRAM
# ============================================================

print("=" * 60)
print("LUFWANYAMA TOWN COUNCIL DATA COLLECTION")
print("CSC 4792 - DATA MINING AND WAREHOUSING")
print("=" * 60)

all_links = []


# ============================================================
# DOWNLOAD IMPORTANT WEB PAGES
# ============================================================

for name, url in PAGES.items():

    html = download_page(
        name,
        url
    )

    if html:

        links = collect_links(
            html,
            url
        )

        for link in links:

            link["source_page"] = name

        all_links.extend(links)

    time.sleep(1)


# ============================================================
# FIND PDF DOCUMENTS
# ============================================================

pdf_links = []

for link in all_links:

    url = link["url"].lower()

    if ".pdf" in url:

        pdf_links.append(link)


print("\n" + "=" * 60)
print(
    f"PDF DOCUMENTS FOUND: {len(pdf_links)}"
)
print("=" * 60)


# ============================================================
# REMOVE DUPLICATE PDF URLS
# ============================================================

unique_pdfs = {}

for link in pdf_links:

    unique_pdfs[
        link["url"]
    ] = link


# ============================================================
# DOWNLOAD PDFs
# ============================================================

for number, link in enumerate(
    unique_pdfs.values(),
    start=1
):

    original_url = link["url"]

    filename = original_url.split("/")[-1]

    filename = filename.split("?")[0]

    if not filename:

        filename = f"document_{number}.pdf"

    if not filename.lower().endswith(".pdf"):

        filename = f"document_{number}.pdf"

    download_pdf(
        original_url,
        filename
    )

    time.sleep(1)


# ============================================================
# SUMMARY
# ============================================================

print("\n" + "=" * 60)
print("DATA COLLECTION COMPLETE")
print("=" * 60)

print(
    f"Web pages collected: {len(PAGES)}"
)

print(
    f"PDF documents found: {len(unique_pdfs)}"
)

print(
    f"Raw files saved in:"
)

print(
    RAW_DIR.resolve()
)

print("=" * 60)