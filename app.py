"""Interactive dashboard for the Lufwanyama Town Council datasets.

Run with::

    streamlit run app.py

Uses the four pipe-separated CSVs in ``data/final``.  No network access needed.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

BASE_DIR = Path(__file__).resolve().parent
FINAL_DIR = BASE_DIR / "data" / "final"
OUTPUTS_DIR = BASE_DIR / "outputs"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

@st.cache_data
def load(path: Path) -> pd.DataFrame:
    if not path.exists():
        st.warning(f"Dataset not found: {path.name}")
        return pd.DataFrame()
    return pd.read_csv(path, sep="|", encoding="utf-8")


def fmt_money(value) -> str:
    try:
        return f"K{float(value):,.2f}"
    except (TypeError, ValueError):
        return "n/a"


# ---------------------------------------------------------------------------
# Layout
# ---------------------------------------------------------------------------

st.set_page_config(
    page_title="Lufwanyama Town Council",
    layout="wide",
)

st.title("Lufwanyama Town Council - Data Mining Dashboard")
st.caption("CSC 4792 - Data Mining and Warehousing | University of Zambia")

# ---------------------------------------------------------------------------
# Load datasets
# ---------------------------------------------------------------------------

cdf = load(FINAL_DIR / "db-unza26-csc4792-lufwanyama-cdf-projects.csv")
budget = load(FINAL_DIR / "db-unza26-csc4792-lufwanyama-budget.csv")
revenue = load(FINAL_DIR / "db-unza26-csc4792-lufwanyama-revenue-grants.csv")
programmes = load(FINAL_DIR / "db-unza26-csc4792-lufwanyama-programmes.csv")

# ---------------------------------------------------------------------------
# KPI summary
# ---------------------------------------------------------------------------

left, mid, right = st.columns(3)
if not cdf.empty:
    left.metric(
        "CDF Projects",
        len(cdf),
        help="Total number of structured CDF projects",
    )
    mid.metric(
        "Total Project Funding", fmt_money(cdf["amount_kwacha"].sum())
    )
    right.metric(
        "Avg Project Cost", fmt_money(cdf["amount_kwacha"].mean())
    )
if not budget.empty:
    budget_total = budget.loc[budget["indicator"] == "Approved Council Budget", "amount_kwacha"]
    if not budget_total.empty:
        st.metric("Approved 2025 Budget", fmt_money(budget_total.iloc[0]))

st.markdown("---")

# ---------------------------------------------------------------------------
# CDF projects
# ---------------------------------------------------------------------------

if not cdf.empty:
    st.header("CDF Projects")

    tab1, tab2 = st.tabs(["By Category", "All Projects"])
    with tab1:
        funding_by_cat = (
            cdf.groupby("category", as_index=False)["amount_kwacha"]
            .sum()
            .sort_values("amount_kwacha", ascending=False)
        )
        fig = px.bar(
            funding_by_cat,
            x="category",
            y="amount_kwacha",
            text=funding_by_cat["amount_kwacha"].apply(fmt_money),
            title="CDF Funding by Category",
            labels={"amount_kwacha": "Total Funding (Kwacha)", "category": "Category"},
            color="category",
        )
        fig.update_traces(textposition="outside")
        fig.update_layout(showlegend=False, xaxis_tickangle=-30)
        st.plotly_chart(fig, use_container_width=True)

        counts = cdf["category"].value_counts().reset_index()
        counts.columns = ["category", "count"]
        fig2 = px.pie(
            counts,
            names="category",
            values="count",
            title="Projects by Category (count)",
        )
        st.plotly_chart(fig2, use_container_width=True)

    with tab2:
        show = cdf[["project_id", "category", "amount_kwacha", "raw_project_text", "source"]]
        show["amount_kwacha"] = show["amount_kwacha"].apply(fmt_money)
        st.dataframe(show, use_container_width=True, hide_index=True)

# ---------------------------------------------------------------------------
# Budget
# ---------------------------------------------------------------------------

if not budget.empty:
    st.header("Council Budget")

    fig = px.bar(
        budget.sort_values("amount_kwacha"),
        x="amount_kwacha",
        y="indicator",
        color="year",
        orientation="h",
        text=budget["amount_kwacha"].apply(fmt_money),
        labels={"amount_kwacha": "Amount (Kwacha)", "indicator": "Indicator"},
        title="Budget Indicators (2024 - 2025)",
    )
    fig.update_traces(textposition="outside")
    st.plotly_chart(fig, use_container_width=True)

# ---------------------------------------------------------------------------
# Revenue & grants
# ---------------------------------------------------------------------------

if not revenue.empty:
    st.header("Revenue & Grants (2025)")

    by_type = (
        revenue.groupby("revenue_type", as_index=False)["amount_kwacha"]
        .sum()
        .sort_values("amount_kwacha", ascending=False)
    )
    fig = px.pie(
        by_type,
        names="revenue_type",
        values="amount_kwacha",
        title="Revenue by Type",
        hole=0.35,
    )
    st.plotly_chart(fig, use_container_width=True)

    fig2 = px.bar(
        revenue.sort_values("amount_kwacha"),
        x="amount_kwacha",
        y="revenue_source",
        color="revenue_type",
        orientation="h",
        text=revenue["amount_kwacha"].apply(fmt_money),
        labels={"amount_kwacha": "Amount (Kwacha)", "revenue_source": "Source"},
        title="Revenue & Grant Sources",
    )
    fig2.update_traces(textposition="outside")
    st.plotly_chart(fig2, use_container_width=True)

# ---------------------------------------------------------------------------
# Development programmes
# ---------------------------------------------------------------------------

if not programmes.empty:
    st.header("Development Programmes")

    prog_amounts = programmes.dropna(subset=["amount_kwacha"])

    # Treemap of funding by programme hierarchy.
    fig = px.treemap(
        prog_amounts,
        path=["category", "programme"],
        values="amount_kwacha",
        title="Programme Funding by Category",
        hover_data=["year", "beneficiaries_or_coverage"],
    )
    st.plotly_chart(fig, use_container_width=True)

    # Simple bar for funded programmes.
    fig2 = px.bar(
        prog_amounts.sort_values("amount_kwacha"),
        x="amount_kwacha",
        y="programme",
        color="category",
        orientation="h",
        text=prog_amounts["amount_kwacha"].apply(fmt_money),
        labels={"amount_kwacha": "Amount (Kwacha)", "programme": "Programme"},
        title="Programme Funding (programmes only)",
    )
    fig2.update_traces(textposition="outside")
    st.plotly_chart(fig2, use_container_width=True)

# ---------------------------------------------------------------------------
# Text insights (optional word cloud from text-mining script)
# ---------------------------------------------------------------------------

wc_path = OUTPUTS_DIR / "lufwanyama_wordcloud.png"
if wc_path.exists():
    st.header("Council Document Text Insights")
    st.image(str(wc_path), caption="Word cloud from council newsletters & reports")

freq_csv = OUTPUTS_DIR / "text_keyword_frequency.csv"
if freq_csv.exists():
    freq_df = pd.read_csv(freq_csv)
    fig = px.bar(
        freq_df[freq_df["frequency"] > 0].sort_values("frequency"),
        x="frequency",
        y="keyword",
        orientation="h",
        title="Keyword Frequency Across Council Documents",
        labels={"frequency": "Occurrences", "keyword": "Keyword"},
    )
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")
st.info(
    "Data lives in `data/final/` (pipe-separated CSVs). "
    "Run `python scripts/analyze_text_keywords.py` first to generate the "
    "word-cloud and keyword report shown above."
)
