# Can the Poor Afford to Breathe?  
**Quantifying Global Climate Inequity through Emissions, Poverty, and Fiscal Capacity**

## Overview

This project explores a pressing global question:  
**Who pays the price for climate change—and who can afford to respond?**

Despite contributing the least to global emissions, many low-income countries face disproportionately severe consequences from climate change. At the same time, these countries often lack the government revenue and fiscal capacity to adapt, protect, or rebuild. This project brings together multiple global datasets to analyze this imbalance and propose a simple yet powerful framework for **climate fairness assessment**.

The core output is a **Climate Fairness Index (CFI)**—a composite metric integrating:
- Per-capita CO₂ emissions
- Share of population in extreme poverty
- Government revenue gap (capacity to finance response)

By comparing these dimensions across countries, we highlight patterns of **structural inequity** that have deep implications for climate policy, aid allocation, and sustainable development.

---

## Objectives

1. **Visualize global disparities** in climate responsibility (emissions) and vulnerability (poverty, revenue gap)
2. **Quantify inequity** using a custom Climate Fairness Index
3. **Cluster countries** into action-oriented groups for aid prioritization and policy insights
4. **Develop interactive visual outputs** to support public communication and policy advocacy

---

## Key Questions

- Which countries emit the least CO₂ but have the highest poverty and lowest fiscal capacity?
- Are high-emitting nations better equipped financially to manage climate adaptation?
- Can we define and visualize *climate injustice* using open, interpretable data?
- How can a data-driven fairness index guide equitable global responses?

---

## Datasets Used

| Dataset | Source | Description |
|--------|--------|-------------|
| **CO₂ Emissions per Capita** | Our World in Data | Measures the average carbon output per individual by country |
| **Extreme Poverty Share** | World Bank | % of population living on less than $2.15/day |
| **Government Revenue Gap** | IMF / World Bank | % difference between current and required government revenue to fund public services |
| **Fertility Rate (Optional)** | UN / OWID | Included to assess population growth and its interaction with resource strain |

---

## Methodology

### 1. Data Cleaning & Preprocessing
- Harmonized country names across all datasets
- Filtered to countries with full data across indicators
- Normalized variables (Min-Max and Z-score) to ensure comparability

### 2. Climate Fairness Index (CFI)
**Formula (normalized):**
CFI = (Poverty % * Revenue Gap %) / CO₂ per capita
- High CFI → Low emissions, high poverty, high revenue gap → *High need, low responsibility*
- Low CFI → High emissions, low poverty, strong revenue → *High responsibility, low vulnerability*

We also computed **rankings**, **deciles**, and **index scores** for visualization.

### 3. Clustering
- Applied k-means clustering to group countries into:
  - **Climate Justice Priorities** (high need, low emissions)
  - **High-Responsibility Economies** (high emissions, low poverty)
  - **Transitional Economies**
  - **Outliers / Special Cases**

### 4. Visualization
- Choropleth map with interactive filters
- Bubble plots with labeled clusters
- Index dashboard with downloadable CSV outputs

---

## Tools & Technologies

- **Python**: `pandas`, `numpy`, `scikit-learn`, `matplotlib`, `seaborn`, `plotly`, `folium`
- **R (optional)**: `tidyverse`, `ggplot2`, `cluster`, `leaflet`
- **Jupyter Notebooks**: For reproducible analysis
- **GitHub Projects**: For workflow and milestone tracking
- **Visual Outputs**: High-resolution charts and exportable data files

---

## Results & Key Insights

- Countries like **Chad, Niger, and the DRC** score among the **highest in CFI**, yet their CO₂ contributions are near zero
- **High-emission, low-poverty countries** (e.g., USA, Australia, Canada) rank among the **lowest in fairness**, indicating a mismatch in responsibility and resilience
- The **Climate Fairness Index** correlates strongly with development aid gaps, suggesting potential use in policy modeling

---

## Limitations

- Some countries lack recent data across all indicators
- Revenue gap estimates rely on IMF projections and may understate informal economies
- Index weighting is simple (multiplicative); alternative models could improve sensitivity

---

## Future Work

- Incorporate **climate risk data** (e.g., natural disaster exposure)
- Extend to **time-series analysis** (trends from 1990–2020)
- Build a **Shiny or Dash app** to allow users to explore the index dynamically
- Publish a **policy brief or blog post** summarizing findings for a general audience

---

## Contributing

This project welcomes collaboration from researchers, data scientists, and policy professionals.  
Feel free to open issues, suggest features, or fork the repo for your own use.

---


## Contact

Created by **Emily Pullen**  
MSc Data Science & Statistics | Toronto, Canada  


