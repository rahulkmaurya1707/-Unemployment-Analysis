# Unemployment Analysis in India Using Python 📊

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)
[![Pandas](https://img.shields.io/badge/pandas-1.5%2B-150458.svg)](https://pandas.pydata.org/)
[![Streamlit](https://img.shields.io/badge/streamlit-1.20%2B-FF4B4B.svg)](https://streamlit.io/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

An end-to-end, data-driven Python project analyzing unemployment rate trends, regional labor disparities, rural vs. urban market dynamics, and the economic disruption caused by **COVID-19 lockdowns** in India (May 2019 – June 2020).

---

## 📌 Project Overview

Unemployment is a key macroeconomic indicator reflecting labor market health and economic stability. In March 2020, the onset of COVID-19 and subsequent nationwide lockdown measures created unprecedented disruptions across India's labor market.

This project performs comprehensive Exploratory Data Analysis (EDA) on an empirical dataset comprising **740 clean monthly observations across 28 Indian States and Union Territories**. It quantifies the exact magnitude of job losses, identifies regional high-risk areas, evaluates rural vs. urban resilience, and delivers an interactive Streamlit dashboard.

---

## 🎯 Objectives

1. **Dataset Inspection & Preprocessing:** Clean raw data, strip trailing whitespace, standardize column names, handle missing values, and convert dates to datetime format.
2. **Exploratory Data Analysis (EDA):** Compute statistical metrics (mean, median, standard deviation, interquartile range).
3. **Macro Economic Trend Analysis:** Track monthly unemployment rates and compute 3-month moving averages.
4. **COVID-19 Impact Quantification:** Compare Pre-COVID baseline (May 2019–Feb 2020) against COVID-19 period (Mar 2020–Jun 2020).
5. **Regional Leaderboard:** Rank 28 States and Union Territories by unemployment severity.
6. **Rural vs Urban Comparison:** Analyze structural labor market disparities between Rural and Urban areas.
7. **Correlation Modeling:** Evaluate relationships between Unemployment Rate, Employed Population, and Labour Participation Rate.
8. **Interactive Web Dashboard:** Build a modern, multi-tab Streamlit dashboard for real-time visualization and filtering.

---

## 🛠️ Technology Stack

- **Core Programming:** Python 3.x
- **Data Manipulation & Analysis:** Pandas, NumPy
- **Data Visualization:** Matplotlib, Seaborn, Plotly Express
- **Interactive Web App:** Streamlit
- **Environment:** Jupyter Notebook

---

## 📂 Project Directory Structure

```
unemployment-analysis/
│
├── data/
│   └── unemployment_dataset.csv          # Raw & Cleaned Dataset (740 records)
│
├── notebooks/
│   └── unemployment_analysis.ipynb       # Fully executed Jupyter Notebook with markdown & code
│
├── src/
│   ├── data_cleaning.py                  # Load, clean, and preprocess raw dataset
│   ├── analysis.py                       # Core statistical & COVID impact calculation functions
│   └── visualization.py                  # Generate and save high-res PNG visual charts
│
├── visualizations/                       # 14 High-resolution generated charts
│   ├── 01_unemployment_distribution.png
│   ├── 02_overall_unemployment_trend.png
│   ├── 03_monthly_unemployment_bar.png
│   ├── 04_covid_period_comparison.png
│   ├── 05_area_covid_comparison.png
│   ├── 06_regional_unemployment_all.png
│   ├── 07_top10_highest_unemployment_states.png
│   ├── 08_top10_lowest_unemployment_states.png
│   ├── 09_seasonal_regional_heatmap.png
│   ├── 10_correlation_heatmap.png
│   ├── 11_labour_participation_vs_unemployment.png
│   ├── 12_employment_trend_millions.png
│   ├── 13_rolling_average_trend.png
│   └── 14_mom_unemployment_change.png
│
├── reports/
│   └── analysis_report.md                # 15-Section Comprehensive Academic Report
│
├── app/
│   └── app.py                            # Interactive Streamlit Web Dashboard
│
├── requirements.txt                      # Project dependencies
├── README.md                             # GitHub Documentation
└── .gitignore                            # Git ignore configuration
```

---

## 📊 Empirical Key Findings Summary

All figures are empirically calculated from the actual dataset:

- **Overall Mean Unemployment Rate:** **11.79%** across all observations.
- **COVID-19 Shock:** Mean unemployment surged from **9.51%** Pre-COVID to **17.77%** during COVID (an **+86.91%** relative surge).
- **Peak Lockdown Months:** April 2020 recorded an average of **23.64%**, while May 2020 reached the peak of **24.88%**.
- **Employment Loss:** Mean employed population per region dropped by **12.71%** (a loss of ~950,000 workers per region/area observation).
- **Urban Disparity:** Urban areas suffered higher average unemployment (**13.17%**) than Rural areas (**10.32%**).
- **Highest Unemployment States:** Tripura (28.35%), Haryana (26.28%), Jharkhand (20.59%), Bihar (18.92%).
- **Lowest Unemployment States:** Meghalaya (4.80%), Odisha (5.66%), Assam (6.43%), Uttarakhand (6.58%).
- **Extreme Spikes:** Urban Puducherry recorded a peak unemployment rate of **76.74%** in April 2020, and Urban Jharkhand reached **70.17%** in May 2020.

---

## 💻 Installation & Setup Guide

### 1. Clone the Repository
```bash
git clone https://github.com/rahulkmaurya1707/-Unemployment-Analysis.git
cd unemployment-analysis
```

### 2. Create and Activate Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

---

## 🚀 How to Run the Project

### A. Run Data Cleaning & Visualization Pipeline
```bash
python src/data_cleaning.py
python src/analysis.py
python src/visualization.py
```

### B. Launch Interactive Streamlit Dashboard
```bash
streamlit run app/app.py
```
*Access dashboard in browser at:* `http://localhost:8501`

### C. Run Jupyter Notebook
```bash
jupyter notebook notebooks/unemployment_analysis.ipynb
```

---

## 📜 Academic Submission & Resume Bullet Points

### Resume Bullet Points (Ready to Use)
- **Engineered an end-to-end Unemployment Analysis System in Python** processing 740 monthly observations across 28 Indian States using Pandas and NumPy.
- **Quantified COVID-19 economic shock**, identifying an 86.9% surge in average unemployment rate (peaking at 24.88% in May 2020) and a 12.7% drop in employed population.
- **Designed 14 publication-quality visualizations** using Matplotlib and Seaborn to communicate regional disparities, urban-rural vulnerabilities, and rolling moving averages.
- **Developed an interactive multi-tab Streamlit dashboard** with dynamic filtering by state, date range, and rural/urban sector.

---

## 📄 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
