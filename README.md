# Lufwanyama Town Council Data Mining & Warehousing Project

## CSC 4792 - Data Mining and Warehousing

### University of Zambia

---

## 1. Project Overview

This project develops a structured dataset for **Lufwanyama Town Council, Zambia**.

The dataset was compiled from official Lufwanyama Town Council web pages, newsletters, reports, budgets, financial documents and other publicly available council publications.

The project focuses on extracting and organizing information relating to:

- Constituency Development Fund (CDF)
- Council budgets
- Revenue and government grants
- Community development projects
- Development programmes
- Infrastructure and public services

---

## 2. Objectives

The main objectives of this project are to:

- Collect council-related information from official sources.
- Extract useful information from PDF documents.
- Clean and structure the collected data.
- Organize CDF projects, budgets, revenue, grants and development programmes.
- Perform exploratory data analysis.
- Generate visualizations to identify funding and development patterns.
- Produce standardized CSV datasets for further analysis.

---

## 3. Data Source

The primary data source is the official Lufwanyama Town Council website:

https://www.lufwanyamacouncil.gov.zm/

The collected materials include:

- CDF publications
- Council newsletters
- Approved budgets
- Financial statements
- Performance reports
- Community engagement documents
- Project information
- Revenue and grant information
- Development programme information

---

## 4. Data Collection

The data collection process retrieved:

- **3 official web pages**
- **54 PDF documents**

The PDF documents were downloaded from the council website and stored in the `data/raw/` directory.

The project uses Python-based data collection and document processing techniques.

---

## 5. Data Processing

The following Python technologies were used:

- Python
- Pandas
- NumPy
- Requests
- BeautifulSoup
- PyPDF
- Matplotlib

The processing workflow was:

```text
Official Council Website
        ↓
Web Pages and PDF Documents
        ↓
Raw Data Collection
        ↓
PDF Text Extraction
        ↓
Data Identification
        ↓
Data Cleaning
        ↓
Data Structuring
        ↓
Exploratory Data Analysis
        ↓
Visualization
        ↓
CSV Export
```

---

## 6. Project Structure

```text
Lufwanyama_DataMining/
├── README.md
├── requirements.txt            # Python dependencies
├── app.py                      # Interactive Streamlit dashboard
├── data/
│   ├── raw/                    # Downloaded PDFs and HTML pages
│   ├── cleaned/
│   │   └── extracted_text/     # Extracted PDF text
│   └── final/                  # Pipe-separated CSV datasets
├── documentation/
│   └── data_description_paper.md
├── notebooks/
│   └── lufwanyama_data_mining.ipynb
├── outputs/                    # Generated charts, reports
└── scripts/
    ├── collect_lufwanyama.py   # Web/PDF scraper
    └── analyze_text_keywords.py # Text mining & word cloud
```

---

## 7. Running

### Install dependencies

```bash
pip install -r requirements.txt
```

### Interactive dashboard

```bash
streamlit run app.py
```

The dashboard loads the four datasets in `data/final/` and renders
interactive Plotly charts (CDF projects, budget, revenue/grants,
development programmes) plus a text-insights panel.

### Text mining

```bash
python scripts/analyze_text_keywords.py
```

Generates `outputs/text_keyword_frequency.csv`,
`outputs/text_document_keyword_coverage.csv` and
`outputs/lufwanyama_wordcloud.png` from the extracted council text.