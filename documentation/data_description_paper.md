# A Structured Dataset of Lufwanyama Town Council Development Projects, Budgets, Revenue and Grants

## Abstract

This dataset provides structured information relating to Lufwanyama Town Council in Zambia. The dataset was developed as part of the CSC 4792 Data Mining and Warehousing course at the University of Zambia. The objective was to collect, extract, clean and organize publicly available local government information into structured datasets suitable for data mining and exploratory analysis.

Information was collected from the official Lufwanyama Town Council website, including council web pages, newsletters, budgets, financial documents, reports, community engagement documents and Constituency Development Fund (CDF) publications. A total of 3 official web pages and 54 PDF documents were collected. PDF text was extracted programmatically and relevant financial and development information was identified.

The resulting datasets cover CDF projects, council budget allocations, government grants, local revenue and selected development programmes. The data can be used to examine patterns in public funding, development priorities, project distribution and local government resource allocation.

**Keywords:** Lufwanyama Town Council, Zambia, Data Mining, Data Warehousing, CDF, Local Government, Revenue, Development Projects, Public Finance

---

# 1. Specifications Table

| Item | Description |
|---|---|
| Subject area | Data Mining and Data Warehousing |
| Specific subject area | Local government development, public finance and CDF projects |
| Type of data | Structured tabular data |
| Data format | Pipe-separated CSV |
| Geographical coverage | Lufwanyama District, Zambia |
| Main data source | Official Lufwanyama Town Council publications |
| Web pages collected | 3 |
| PDF documents collected | 54 |
| Newsletter documents identified | 4 |
| Main datasets | CDF Projects, Budget, Revenue and Grants, Development Programmes |
| Data processing tools | Python, Pandas, NumPy, Requests, BeautifulSoup, PyPDF, Matplotlib |
| Analysis environment | Jupyter Notebook |
| Intended users | Students, researchers, data analysts, local government researchers and development researchers |
| Main output | Structured datasets suitable for exploratory analysis and data mining |

---

# 2. Background and Summary

Local government institutions generate large amounts of information through budgets, development projects, financial statements, public notices, community engagement activities and other administrative processes. Much of this information is published in web pages and PDF documents, making it difficult to analyse directly.

This project focuses on Lufwanyama Town Council in Zambia and applies data mining and data warehousing techniques to publicly available council information.

The main objective is to transform information contained in heterogeneous web pages and PDF documents into structured datasets that can be analysed using computational methods.

The project particularly focuses on information relating to:

- Constituency Development Fund projects
- Council budgets
- Government grants
- Local revenue
- Community development programmes
- Infrastructure projects
- Education
- Health
- Water and sanitation
- Roads and transport
- Agriculture
- Empowerment programmes

The dataset was developed from publicly available official council materials.

---

# 3. Data Collection

## 3.1 Source Identification

The primary source used for the dataset was the official Lufwanyama Town Council website.

The collection process identified relevant council pages and downloadable documents containing information related to CDF, budgets, financial statements, development projects, revenue and community programmes.

The main categories of documents collected included:

- CDF publications
- Council newsletters
- Approved budgets
- Financial statements
- Performance reports
- Community engagement documents
- Project publications
- Public notices
- Application forms
- Stakeholder meeting documents

## 3.2 Web Collection

Python was used to collect information from the council website.

The Requests library was used to retrieve web pages while BeautifulSoup was used to process HTML content and identify links to relevant documents.

The collection process resulted in:

- 3 web pages collected
- 54 PDF documents identified and saved

The original documents were retained in the `data/raw/` directory to support traceability and reproducibility.

---

# 4. PDF Text Extraction

The collected PDF documents were processed using Python.

The PyPDF library was used to read the documents and extract available text from individual pages.

The extracted text was saved separately under:

`data/cleaned/extracted_text/`

The extracted text was then examined for terms associated with the project objectives.

Examples of search terms included:

- CDF
- budget
- project
- revenue
- grant
- bursary
- loan
- procurement
- financial
- performance
- community
- ward
- contract
- road
- water
- health
- education

This process helped identify documents containing potentially useful information for the final datasets.

---

# 5. Data Description

The project produces four main datasets.

## 5.1 CDF Projects Dataset

The CDF projects dataset contains structured information relating to development projects.

The dataset includes fields such as:

- `project_id`
- `council`
- `country`
- `data_type`
- `category`
- `amount_kwacha`
- `raw_project_text`
- `source`

The project categories include:

- Education
- Health
- Water and Sanitation
- Roads and Transport
- Energy
- Housing
- Other

The monetary values are represented in Zambian Kwacha.

---

## 5.2 Budget Dataset

The budget dataset contains selected council budget indicators and allocations.

The dataset includes:

- Council
- Year
- Indicator
- Category
- Amount in Kwacha
- Source

Examples of budget indicators include:

- Approved Council Budget
- CDF Programme
- CDF Community Projects
- Women and Youth Empowerment
- CDF Administration
- Secondary and Skills Bursaries
- Disaster Component
- CDF Allocation

---

## 5.3 Revenue and Grants Dataset

The revenue and grants dataset contains selected government funding and local revenue categories.

Government funding categories include:

- CDF
- LGEF
- Grant in Lieu of Rates
- Devolution
- Roads Grant
- Health Grant
- Cash for Work
- Community Development
- Agriculture Services
- Fisheries and Livestock
- Other Grants

Local revenue categories include:

- Local Taxes
- Fees and Charges
- Levies
- Permits
- Licences
- Other Income

The dataset contains the council, year, revenue source, revenue type and amount.

---

## 5.4 Development Programmes Dataset

The development programmes dataset contains selected council development activities.

Examples include:

- Cash for Work
- Farming Inputs
- Feeder Road Grading
- Borehole Drilling
- Road Infrastructure
- CDF Empowerment
- CDF Community Projects

Where available, the dataset records funding, geographical coverage and beneficiary information.

---

# 6. Data Preprocessing

Several preprocessing operations were applied to improve the quality and consistency of the structured data.

## 6.1 Duplicate Removal

Duplicate records were identified and removed from the CDF project dataset.

This reduces the possibility of counting the same project more than once.

## 6.2 Monetary Value Cleaning

Monetary values originally represented using the `K` currency symbol and comma separators were converted into numeric values.

For example:

`K540,195.89`

was converted into:

`540195.89`

This allows numerical calculations such as sums, averages and comparisons.

## 6.3 Missing Value Handling

Records where project amounts could not be converted into valid numerical values were excluded from the final CDF project analysis.

Some source documents contain scanned or image-based content from which automatic text extraction may not be possible.

## 6.4 Project Classification

Project descriptions were classified into broader development categories.

The classification was based on keywords appearing in the project descriptions.

For example:

- Classroom and school projects → Education
- Health posts and maternity projects → Health
- Boreholes and water projects → Water and Sanitation
- Roads and bridges → Roads and Transport
- Solar and electrification → Energy
- Staff houses → Housing

## 6.5 Unique Project Identifiers

A unique identifier was assigned to each structured CDF project.

The identifiers follow the format:

`LTC-CDF-001`

`LTC-CDF-002`

`LTC-CDF-003`

and so on.

---

# 7. Exploratory Data Analysis

Exploratory Data Analysis (EDA) was performed using Pandas and Matplotlib.

The analysis included:

- Number of projects
- Total project funding
- Average project cost
- Funding by project category
- Revenue and grant comparisons
- Development programme analysis

Grouping operations were used to determine the number of projects and total funding associated with each project category.

The analysis provides a basis for understanding the distribution of development resources across different sectors.

---

# 8. Data Visualization

Three major visualizations were generated.

## 8.1 CDF Projects by Category

A bar chart was produced to show the number of CDF projects associated with each development category.

This allows the distribution of projects across sectors such as education, health, water and sanitation, roads and energy to be compared.

## 8.2 CDF Funding by Category

A second bar chart was generated showing the total funding represented by each project category.

This provides an indication of which development sectors account for larger amounts of project funding.

## 8.3 Revenue and Grants

A third visualization was created to compare the different 2025 revenue and grant sources.

This provides a view of the relative contribution of government grants and locally generated revenue categories.

---

# 9. Data Quality and Validation

Several basic validation procedures were applied.

These included:

- Checking the number of collected documents
- Inspecting extracted text
- Searching documents for relevant keywords
- Identifying financial records
- Removing duplicate project records
- Checking monetary values
- Removing invalid project amounts
- Assigning unique project identifiers
- Checking missing values
- Reviewing project categories

The raw documents were retained to provide a reference point for the processed information.

---

# 10. Dataset Organization

The project follows the following directory structure:

```text
Lufwanyama_DataMining/
│
├── README.md
│
├── data/
│   ├── raw/
│   ├── cleaned/
│   │   └── extracted_text/
│   └── final/
│
├── documentation/
│   └── data_description_paper.md
│
├── notebooks/
│   └── lufwanyama_data_mining.ipynb
│
├── outputs/
│
└── scripts/
    └── collect_lufwanyama.py