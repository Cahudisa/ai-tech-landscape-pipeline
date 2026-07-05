# AI Tech Landscape Pipeline 🤖

> End-to-end data pipeline analyzing the companies leading the AI race: NVIDIA, AMD, Microsoft, Google, Meta, IBM and more.

## 🚀 Live Demo
**[View the interactive app](https://ai-tech-landscape-pipeline-ygdiezmxksbsv4x4z74hkw.streamlit.app/)**

---

## 📌 Business Questions Answered
- Which Big Tech company grew the most since the AI boom (2010–2024)?
- Who had the best and worst single year return?
- How has NVIDIA vs AMD vs INTEL stock evolved historically?
- Which AI companies generate the most revenue?
- Do the highest-earning AI companies treat their employees the best?

---

## 🏗️ Architecture

```
Raw CSV (Kaggle)
      │
      ▼
 Bronze Layer        → Raw ingestion, no transformations
      │
      ▼
 Silver Layer        → Cleaning, type casting, standardization
      │
      ▼
  Gold Layer         → Business metrics ready for visualization
      │
      ▼
 Streamlit App       → Interactive web dashboard (public)
 Power BI Dashboard  → Business intelligence report
```

---

## 📊 Data Sources

| Dataset | Source |
|---|---|
| Big Tech Stock Prices (14 companies) | [Kaggle — evangower](https://www.kaggle.com/datasets/evangower/big-tech-stock-prices) |
| GPU Companies Stock Prices (AMD, NVIDIA, INTEL, ASUS, MSI) | [Kaggle — kapturovalexander](https://www.kaggle.com/datasets/kapturovalexander/nvidia-amd-intel-asus-msi-share-prices) |
| AI Companies Metrics (100 companies) | [Kaggle — raniritu](https://www.kaggle.com/datasets/raniritu/ai-companies) |

> Raw CSV files are not included in this repo. Download them manually from the links above and place them in `data/bronze/`.

---

## 🛠️ Stack

| Layer | Tools |
|---|---|
| Ingestion | Python, Pandas |
| Storage | Parquet (Bronze → Silver → Gold) |
| Transformation | Pandas, Regex |
| Orchestration | Jupyter Notebooks |
| Visualization | Streamlit, Plotly |
| Business Intelligence | Power BI — see [`/powerbi`](./powerbi/) folder |
| Version Control | Git, GitHub |

---

## 📁 Project Structure

```
ai-tech-landscape-pipeline/
│
├── data/
│   ├── bronze/          ← Raw CSV files (not tracked by Git)
│   ├── silver/          ← Cleaned Parquet files (not tracked by Git)
│   └── gold/            ← Business metrics Parquet files
│
├── notebooks/
│   ├── 01_bronze_ingest.ipynb
│   ├── 02_silver_transform.ipynb
│   └── 03_gold_metrics.ipynb
│
├── powerbi/
│   └── AI_Tech_Landscape_Dashboard.pbix  ← Power BI report
│
├── app.py               ← Streamlit web app
├── requirements.txt
└── README.md
```

---

## ⚙️ How to Run Locally

```bash
# 1. Clone the repo
git clone https://github.com/Cahudisa/ai-tech-landscape-pipeline.git
cd ai-tech-landscape-pipeline

# 2. Create and activate virtual environment
python -m venv venv
venv\Scripts\activate       # Windows
source venv/bin/activate    # Mac/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Download datasets from Kaggle and place CSV files in data/bronze/

# 5. Run notebooks in order
# 01_bronze_ingest.ipynb → 02_silver_transform.ipynb → 03_gold_metrics.ipynb

# 6. Launch the app
streamlit run app.py
```

---

## 👤 Author
**Carlos Díaz** — Data Engineer  
[GitHub](https://github.com/Cahudisa)
