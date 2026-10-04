# Comprehensive Analysis Report: Unemployment Analysis in India Using Python

**Project Title:** Unemployment Analysis in India Using Python  
**Alternative Title:** Unemployment Trends and COVID-19 Impact Analysis Using Python  
**Time Horizon Analyzed:** May 31, 2019 – June 30, 2020 (14 Monthly Cycles)  
**Scope:** 28 States & Union Territories of India (Rural & Urban Breakdown)  
**Clean Observations:** 740 Valid Records  

---

## 1. Introduction

Unemployment is one of the most critical macroeconomic indicators used by policymakers, economists, and social scientists to evaluate economic health, labor force efficiency, and social welfare. In India, labor market dynamics are highly complex, influenced by regional economic structures, agrarian seasonality, urban industrial hubs, and informal sector dominance. 

The onset of the global COVID-19 pandemic in early 2020 and the subsequent implementation of nationwide lockdowns triggered an unprecedented economic shock. This report provides a quantitative, data-driven investigation into unemployment trends in India before and during the COVID-19 crisis using Python data science libraries (`pandas`, `numpy`, `matplotlib`, `seaborn`, `plotly`).

---

## 2. Problem Statement

Economic disruptions affect regions, sectors, and labor demographics unevenly. Without empirical data analysis, it is difficult to determine:
- How severe the unemployment spike was during the COVID-19 lockdown.
- Which Indian states and Union Territories suffered the most acute employment shocks.
- Whether urban or rural labor markets experienced greater vulnerability.
- How employment levels and labor force participation rates responded to lockdown measures.

This project addresses these questions by performing rigorous Exploratory Data Analysis (EDA) on empirical employment dataset.

---

## 3. Project Objectives

1. **Dataset Inspection & Preprocessing:** Clean raw data, strip whitespace, handle missing values, resolve duplicates, and parse dates into standardized datetime formats.
2. **Exploratory Data Analysis (EDA):** Compute central tendencies (mean, median), dispersion metrics (standard deviation, IQR), and range for key employment variables.
3. **Macro Economic Trend Analysis:** Track national monthly unemployment trends and evaluate rolling 3-month moving averages.
4. **COVID-19 Shock Quantification:** Compare Pre-COVID baseline metrics (May 2019 – Feb 2020) against COVID-19 lockdown metrics (Mar 2020 – Jun 2020).
5. **Regional Leaderboard & Geographical Analysis:** Rank 28 States and Union Territories by mean unemployment rate and identify high-volatility states.
6. **Rural vs Urban Sectoral Analysis:** Evaluate labor market disparities between Rural and Urban areas.
7. **Correlation & Volatility Modeling:** Measure Pearson correlation coefficients between Unemployment Rate, Employed Population, and Labour Participation Rate.
8. **Data-Driven Policy Insights:** Formulate actionable economic and social policy recommendations grounded in empirical data.

---

## 4. Dataset Description

The dataset was sourced from empirical monthly labor statistics across Indian States and UTs.

### Raw vs Cleaned Dataset Specifications
| Parameter | Value / Description |
| :--- | :--- |
| **Total Raw Rows** | 754 rows (including blank delimiter rows) |
| **Clean Non-Empty Rows** | 740 observations |
| **Time Frame** | May 31, 2019 to June 30, 2020 |
| **Number of Unique States/UTs** | 28 Regions |
| **Geographical Area Categorization** | Rural (359 obs) and Urban (381 obs) |
| **Sampling Frequency** | Monthly |

### Column Schema Mapping
| Column Name in Dataset | Cleaned Variable Name | Data Type | Description |
| :--- | :--- | :--- | :--- |
| `Region` | `Region` | String / Object | Name of the Indian State or Union Territory |
| `Date` | `Date` | Datetime64 | End of month survey observation date |
| `Frequency` | `Frequency` | String | Frequency of observation ("Monthly") |
| `Estimated Unemployment Rate (%)` | `Unemployment_Rate` | Float64 | Percentage of labor force actively seeking work |
| `Estimated Employed` | `Employed` | Float64 | Estimated absolute count of employed individuals |
| `Estimated Labour Participation Rate (%)` | `Labour_Participation_Rate` | Float64 | Percentage of working-age population in labor force |
| `Area` | `Area` | String | Geographical breakdown (`Rural` vs `Urban`) |

---

## 5. Data Cleaning & Preprocessing

The dataset underwent structured data cleaning pipelines:
1. **Column Name Standardization:** Leading and trailing whitespaces were removed from column headers.
2. **Missing Value Resolution:** Out of 754 raw entries, 14 empty/delimiter rows (`,,,,,,`) were removed, retaining 740 100% complete rows with zero missing values.
3. **Datatype Conversion:** `Date` column strings (formatted as `DD-MM-YYYY`) were converted into standard `datetime64[ns]` objects. Numeric columns were verified as `float64`.
4. **Text Normalization:** String values in `Region`, `Frequency`, and `Area` were stripped of extra spaces.
5. **Temporal Feature Extraction:** Engineered columns included `Year`, `Month`, `Month_Name`, `Year_Month`, and a binary indicator `COVID_Period` (`Pre-COVID` vs `COVID-19 Period`).

---

## 6. Exploratory Data Analysis (EDA)

### Summary Statistics of Key Indicators (740 Observations)

| Metric | Unemployment Rate (%) | Employed Population | Labour Participation Rate (%) |
| :--- | :---: | :---: | :---: |
| **Mean** | **11.79%** | **7,204,460** | **42.63%** |
| **Median** | **8.35%** | **4,744,179** | **41.16%** |
| **Standard Deviation** | **10.72%** | **8,087,988** | **8.11%** |
| **Minimum** | 0.00% | 49,420 | 13.33% |
| **25th Percentile (Q1)** | 4.66% | 1,190,405 | 38.06% |
| **75th Percentile (Q3)** | 15.89% | 11,275,490 | 45.51% |
| **Interquartile Range (IQR)**| 11.23% | 10,085,085 | 7.44% |
| **Maximum** | **76.74%** | **45,777,509** | **72.57%** |

*Key Statistical Observation:* The mean unemployment rate (11.79%) is significantly higher than the median (8.35%), indicating a **positively skewed distribution** driven by extreme COVID-19 lockdown spikes in April and May 2020.

---

## 7. Macroeconomic Unemployment Trends Over Time

### Monthly National Average Unemployment Rate

| Month-Year | Mean Unemployment Rate (%) | Median Unemployment Rate (%) | Standard Deviation | Status / Macro Event |
| :--- | :---: | :---: | :---: | :--- |
| **May 2019** | 8.87% | 6.87% | 7.32% | Baseline Pre-COVID |
| **Jun 2019** | 9.30% | 7.57% | 6.42% | Baseline Pre-COVID |
| **Jul 2019** | 9.03% | 7.16% | 6.84% | Baseline Pre-COVID |
| **Aug 2019** | 9.64% | 7.27% | 7.61% | Baseline Pre-COVID |
| **Sep 2019** | 9.05% | 6.24% | 7.52% | Baseline Pre-COVID |
| **Oct 2019** | 9.90% | 7.29% | 6.84% | Baseline Pre-COVID |
| **Nov 2019** | 9.87% | 6.94% | 7.71% | Baseline Pre-COVID |
| **Dec 2019** | 9.50% | 7.24% | 7.80% | Baseline Pre-COVID |
| **Jan 2020** | 9.95% | 6.79% | 8.16% | Pre-COVID |
| **Feb 2020** | 9.96% | 7.55% | 7.76% | Pre-COVID Baseline End |
| **Mar 2020** | **10.70%** | 8.53% | 7.50% | Initial COVID Onset |
| **Apr 2020** | **23.64%** | **18.32%** | **18.94%** | **Peak Lockdown Shock** |
| **May 2020** | **24.88%** | **20.54%** | **15.91%** | **Lockdown Peak Disruption** |
| **Jun 2020** | **11.90%** | 10.35% | 8.75% | Unlock Phase 1 Recovery |

---

## 8. COVID-19 Impact Analysis

To rigorously evaluate the COVID-19 economic disruption, the dataset was segmented into two distinct analytical windows:
- **Pre-COVID Baseline Period:** May 31, 2019 to February 29, 2020 (10 Months, 536 Observations)
- **COVID-19 Impact Period:** March 31, 2020 to June 30, 2020 (4 Months, 204 Observations)

### Quantitative Impact Summary

| Economic Metric | Pre-COVID Baseline | COVID-19 Period | Absolute Change | Relative Change (%) |
| :--- | :---: | :---: | :---: | :---: |
| **Mean Unemployment Rate (%)** | **9.51%** | **17.77%** | **+8.26% points** | **+86.91%** |
| **Median Unemployment Rate (%)** | **7.17%** | **14.29%** | **+7.12% points** | **+99.30%** |
| **Peak Single-Month Max Rate** | **34.69%** | **76.74%** | **+42.05% points** | **+121.22%** |
| **Mean Employed Population** | **7,466,028** | **6,517,203** | **-948,825** | **-12.71%** |
| **Mean Labour Participation Rate**| **43.89%** | **39.33%** | **-4.56% points** | **-10.38%** |

### Key COVID-19 Insights
1. **Surge in Unemployment:** National average unemployment almost doubled during the lockdown window, jumping by **+86.91%**.
2. **Severe Job Contraction:** On average, states lost **~950,000 employed workers** during the 4-month lockdown window, representing a **12.71% decline in overall employment**.
3. **Labor Force Withdrawal:** Labour Participation Rate dropped by **4.56 percentage points** (from 43.89% to 39.33%), showing that millions of discouraged workers temporarily withdrew from the active labor search.

---

## 9. Regional & State-Level Performance Analysis

Unemployment rates varied dramatically across India's 28 States and Union Territories.

### State Unemployment Ranking Table (Overall Period Means)

| Rank | State / Union Territory | Mean Unemployment Rate (%) | Max Unemployment Rate (%) | Pre-COVID Mean (%) | COVID Period Mean (%) |
| :---: | :--- | :---: | :---: | :---: | :---: |
| **1** | **Tripura** | **28.35%** | 43.64% | 28.33% | 28.41% |
| **2** | **Haryana** | **26.28%** | 46.89% | 22.37% | 36.08% |
| **3** | **Jharkhand** | **20.59%** | 70.17% | 13.06% | 39.38% |
| **4** | **Bihar** | **18.92%** | 58.77% | 13.43% | 32.64% |
| **5** | **Himachal Pradesh** | **18.54%** | 50.00% | 18.99% | 17.42% |
| **6** | Delhi | 16.50% | 45.78% | 13.88% | 23.03% |
| **7** | Jammu & Kashmir | 16.19% | 24.06% | 16.89% | 14.42% |
| **8** | Chandigarh | 15.99% | 22.05% | 16.33% | 14.33% |
| **9** | Rajasthan | 14.06% | 35.53% | 12.56% | 17.81% |
| **10**| Uttar Pradesh | 12.55% | 32.06% | 10.37% | 18.01% |
| ... | ... | ... | ... | ... | ... |
| **24**| Gujarat | 6.66% | 25.94% | 5.22% | 10.27% |
| **25**| Uttarakhand | 6.58% | 17.36% | 5.86% | 8.38% |
| **26**| **Assam** | **6.43%** | 11.17% | 6.42% | 6.45% |
| **27**| **Odisha** | **5.66%** | 24.48% | 3.52% | 10.99% |
| **28**| **Meghalaya** | **4.80%** | 17.39% | 3.78% | 7.35% |

### Top 5 States with Extreme Lockdown Spikes (April–May 2020)
1. **Puducherry:** Reached **76.74%** in Urban areas (April 2020) and **75.00%** in Urban areas (May 2020).
2. **Jharkhand:** Reached **70.17%** in Urban areas (May 2020) and **61.48%** (April 2020).
3. **Bihar:** Reached **58.77%** in Urban areas (April 2020) and **47.26%** in Rural areas (May 2020).
4. **Tamil Nadu:** Reached **53.19%** in Rural areas (April 2020) and **45.55%** in Urban areas.
5. **Himachal Pradesh:** Reached **50.00%** in Urban areas (May 2020).

---

## 10. Rural vs Urban Sectoral Analysis

Comparing Rural and Urban observations reveals clear structural differences during economic shocks.

| Sector / Area | Mean Unemployment Rate (%) | Median Unemployment Rate (%) | Std Deviation (%) | Mean Employed Population | Mean Labour Participation (%) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Rural** | **10.32%** | **6.76%** | 10.04% | 10,192,852 | 44.46% |
| **Urban** | **13.17%** | **9.97%** | 11.17% | 4,388,626 | 40.90% |

### Analytical Insights:
- **Urban Vulnerability:** Urban areas experienced significantly higher mean unemployment (**13.17%**) than rural areas (**10.32%**). Urban industries, service sectors, hospitality, retail, and construction were severely halted during lockdowns.
- **Rural Resilience:** Rural areas benefited from agriculture, which was classified as an essential service, as well as rural safety nets like MGNREGA.

---

## 11. Correlation & Econometric Analysis

Pearson correlation matrix calculated across numerical indicators:

| Variable | Unemployment Rate (%) | Employed Population | Labour Participation Rate (%) |
| :--- | :---: | :---: | :---: |
| **Unemployment Rate (%)** | **1.0000** | -0.2229 | +0.0026 |
| **Employed Population** | -0.2229 | **1.0000** | +0.0113 |
| **Labour Participation Rate (%)** | +0.0026 | +0.0113 | **1.0000** |

### Correlation Insights:
1. **Unemployment Rate vs Employed Population ($r = -0.223$):** Moderate negative correlation. As unemployment spikes, absolute employment contracts.
2. **Unemployment Rate vs Labour Participation Rate ($r = +0.0026$):** Near zero correlation across the national aggregate, demonstrating that labor participation is influenced by structural demographic factors rather than short-term unemployment fluctuations alone.

---

## 12. Key Findings Summary

Below are the direct data-backed answers to the 10 core analytical questions:

1. **Overall Trend:** Unemployment remained stable around 8.8%–9.9% in 2019, spiked massively to 23.6% in April 2020 and 24.9% in May 2020 due to COVID-19 lockdowns, before sharply recovering to 11.9% in June 2020.
2. **Highest Unemployment Period:** **May 2020** recorded the highest monthly average (24.88%), closely followed by **April 2020** (23.64%).
3. **Lowest Unemployment Period:** **May 2019** recorded the lowest monthly average (8.87%).
4. **COVID-19 Impact:** COVID-19 caused national mean unemployment to surge by **+86.91%** (from 9.51% to 17.77%) and caused a **12.71% drop** in mean employed population.
5. **Highest Unemployment States:** **Tripura** (28.35%), **Haryana** (26.28%), **Jharkhand** (20.59%), and **Bihar** (18.92%).
6. **Lowest Unemployment States:** **Meghalaya** (4.80%), **Odisha** (5.66%), **Assam** (6.43%), and **Uttarakhand** (6.58%).
7. **Seasonal Patterns:** Minor pre-COVID fluctuations occurred in August and October (harvest/festival cycles), but seasonal variations were completely dwarfed by the COVID-19 shock.
8. **Largest Changes:** **April 2020** registered the largest month-over-month increase (**+12.94 percentage points** relative to March), while **June 2020** registered the largest recovery drop (**-12.97 percentage points** relative to May).
9. **Labour Participation Relationship:** Showed a neutral correlation ($r = +0.0026$) with unemployment rate, but average participation dipped by 4.56% during lockdowns.
10. **Major Structural Pattern:** Urban labor markets experienced greater volatility and higher baseline unemployment than rural labor markets during macroeconomic shocks.

---

## 13. Data-Informed Policy & Social Insights

*(Note: Presented as empirical data-informed suggestions rather than definitive economic policy claims.)*

1. **Targeted State Safety Nets:** States with persistently high baseline unemployment (e.g., Haryana, Tripura, Jharkhand, Bihar) require structural job creation initiatives and industrial diversification.
2. **Urban Emergency Employment Schemes:** While Rural India benefits from MGNREGA during crises, Urban areas lacked a corresponding formal safety net, leading to urban unemployment reaching 13.17%. Establishing an Urban Employment Guarantee Scheme could mitigate future lockdown shocks.
3. **Seasonal & Essential Worker Protection:** Protecting informal and migrant workers through portable social security benefits would cushion sharp employment drops during disruptions.
4. **Labor Force Re-engagement:** Programs targeting discouraged workers who exited the labor force during COVID-19 (re-engaging the 4.56% LPR drop) are vital for economic recovery.

---

## 14. Project Limitations

1. **Time Horizon Constraint:** The dataset spans 14 months (May 2019 – June 2020). Multi-year seasonality modeling (e.g., 5-year ARIMA decomposition) requires multi-year datasets.
2. **Frequency Resolution:** Monthly aggregated data captures macro trends but smooths over week-to-week employment volatility.
3. **Observational Nature:** Correlations identified in this dataset do not imply strict econometric causality without control variables for fiscal stimulus, trade policy, or healthcare interventions.

---

## 15. Conclusion

This project successfully delivered a complete, data-driven analysis of unemployment in India using Python. By inspecting empirical data rather than assuming structures, we mapped out the macroeconomic shock of COVID-19, identified regional disparities, and quantified urban-rural differences. The resulting codebase, visualizations, Streamlit dashboard, and documentation provide a robust foundation for academic submission, technical interviews, and resume representation.
