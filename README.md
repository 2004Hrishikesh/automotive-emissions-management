# Vehicle Emissions and Fuel Efficiency: Data Pipeline and Dashboard

Course project for Foundations of Data Science at VIT Vellore, taught by Prof. Kumar K. The project builds a pipeline for vehicle fuel-economy and emissions data: loading, quality assessment, cleaning and feature engineering. The results are shown in an interactive Plotly Dash dashboard.

![Dashboard preview](demo_visualization.png)

## Data

| Dataset | Rows | Source |
|---|---:|---|
| UCI Auto MPG | 398 | UCI Machine Learning Repository |
| Fuel economy | 1,000 | synthetic, follows the EPA schema |
| Vehicle listings | 2,000 | synthetic, follows a public Kaggle schema |

- **Download:** `download_datasets.py` fetches the UCI data.
- **Synthetic sets:** the same script generates the other two with a fixed random seed, so the pipeline can be tested on larger tables.

## Pipeline

All cleaning code is in `src/data_processing/data_cleaner.py`.

- **Quality report:** each dataset gets a report covering completeness, duplicates, data types and an overall score.
- **Auto MPG:**
  - missing horsepower values (`?`) are filled with the median
  - outliers are capped with the IQR rule
  - power-to-weight ratio, vehicle age and origin name are added
- **Fuel economy:**
  - invalid MPG rows are removed and fuel-type labels are standardized
  - missing CO2 values are filled with KNN imputation (k = 5) from the MPG and engine-size columns
  - efficiency bands are added
- **Vehicle listings:** types are fixed, duplicates are removed and unused columns are dropped.
- **Shared steps:** min-max normalization and categorical encoding are available for all datasets.

## Dashboard

`run_dashboard.py` starts the dashboard at http://localhost:8050. Its tabs are:

- dataset overview
- quality scores (gauge and radar charts)
- distributions
- a cleaning summary
- the pipeline architecture

## Usage

```bash
pip install -r requirements.txt
python download_datasets.py
python run_phase_ii_analysis.py
python run_dashboard.py
```

The notebooks in `notebooks/` cover the same steps with more charts and a Tableau export.

## Structure

```
src/data_processing/   data loading and cleaning
src/visualization/     Dash dashboard
data/raw, data/processed
notebooks/
```
