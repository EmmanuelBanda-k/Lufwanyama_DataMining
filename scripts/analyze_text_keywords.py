"""Text mining for Lufwanyama Town Council documents.

Reads the already-extracted council text files in
``data/cleaned/extracted_text`` and produces:

* ``outputs/text_keyword_frequency.csv``  - count of each keyword across all documents
* ``outputs/text_document_keyword_coverage.csv`` - per-document keyword hit summary
* ``outputs/lufwanyama_wordcloud.png``    - visual word cloud of the council corpus

No network access required.  Run directly::

    python scripts/analyze_text_keywords.py
"""

from __future__ import annotations

import csv
import re
from collections import Counter
from pathlib import Path

import matplotlib

matplotlib.use("Agg")  # headless backend -> works without a display
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent
TEXT_DIR = BASE_DIR / "data" / "cleaned" / "extracted_text"
OUTPUT_DIR = BASE_DIR / "outputs"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Keywords aligned with the notebook's information-retrieval search terms.
KEYWORDS = [
    "CDF", "budget", "project", "revenue", "grant", "bursary", "loan",
    "procurement", "financial", "performance", "community", "ward",
    "contract", "road", "water", "health", "education", "borehole",
    "latrine", "ablution", "maternity", "school", "classroom", "pump",
]

# Extra English stop words so the word cloud focuses on council content.
EXTRA_STOPWORDS = {
    "the", "and", "of", "to", "in", "for", "a", "an", "with", "on",
    "at", "by", "from", "is", "are", "was", "were", "be", "this",
    "that", "as", "it", "or", "not", "has", "have", "had", "will",
    "shall", "under", "per", "through", "between", "into", "within",
    "month", "year", "years", "kwacha", "k",
}


def iter_text_files(root: Path):
    """Yield (stem, lowercased text) for every non-empty extracted text file."""
    for txt in sorted(root.glob("*.txt")):
        try:
            size = txt.stat().st_size
        except OSError:
            continue
        if size == 0:
            continue
        try:
            text = txt.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        if not text.strip():
            continue
        yield txt.stem, text


def keyword_frequency(texts):
    """Return total keyword counts plus per-document coverage."""
    totals = Counter()
    coverage = []
    for stem, text in texts:
        lowered = text.lower()
        hits = 0
        for kw in KEYWORDS:
            count = len(re.findall(rf"\b{re.escape(kw)}\b", lowered))
            if count:
                totals[kw] += count
                hits += 1
        coverage.append({
            "document": stem,
            "keywords_found": hits,
            "characters": len(text),
        })
    return totals, coverage


def build_wordcloud(texts) -> Path:
    """Aggregate the corpus and render a word cloud PNG."""
    stopwords = set(STOPWORDS) | EXTRA_STOPWORDS
    corpus = "\n".join(text for _, text in texts)
    # Keep tokens that carry meaning (alpha, length >= 3).
    tokens = [t.lower() for t in re.findall(r"[A-Za-z][A-Za-z]{2,}", corpus)]
    filtered = [t for t in tokens if t not in stopwords]
    frequencies = Counter(filtered).most_common(200)
    frequencies = dict(frequencies)

    wc = WordCloud(
        width=1200,
        height=600,
        background_color="white",
        colormap="viridis",
        max_words=150,
        prefer_horizontal=0.9,
    )
    wc.generate_from_frequencies(frequencies)

    out = OUTPUT_DIR / "lufwanyama_wordcloud.png"
    wc.to_file(out)
    return out


def write_csv(rows, fieldnames, path):
    with path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main():
    if not TEXT_DIR.exists():
        print(f"Text directory not found: {TEXT_DIR}")
        print("Run the notebook first to extract text from the raw PDFs.")
        return

    texts = list(iter_text_files(TEXT_DIR))
    if not texts:
        print("No extracted text files found (all may be empty / scanned PDFs).")
        return

    # --- Keyword frequency report -----------------------------------------
    totals, coverage = keyword_frequency(texts)

    freq_rows = [
        {"keyword": k, "frequency": totals.get(k, 0)} for k in KEYWORDS
    ]
    freq_rows.sort(key=lambda r: r["frequency"], reverse=True)

    freq_csv = OUTPUT_DIR / "text_keyword_frequency.csv"
    write_csv(freq_rows, ["keyword", "frequency"], freq_csv)

    # --- Per-document coverage --------------------------------------------
    coverage.sort(key=lambda r: r["characters"], reverse=True)
    cov_csv = OUTPUT_DIR / "text_document_keyword_coverage.csv"
    write_csv(coverage, ["document", "keywords_found", "characters"], cov_csv)

    # --- Word cloud -------------------------------------------------------
    wc_path = build_wordcloud(texts)

    print("Text mining complete.")
    print(f"  Documents processed : {len(texts)}")
    print(f"  Keyword report      : {freq_csv}")
    print(f"  Coverage report     : {cov_csv}")
    print(f"  Word cloud image    : {wc_path}")

    top5 = ", ".join(f"{r['keyword']}={r['frequency']}" for r in freq_rows[:5])
    print(f"  Top keywords        : {top5}")


if __name__ == "__main__":
    main()
