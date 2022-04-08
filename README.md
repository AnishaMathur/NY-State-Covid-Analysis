# Covid Analysis for New York State

install git-lfs from [here](https://git-lfs.github.com/)

## Introduction

This project showcases COVID analysis for the state of New York. We draw from different data sources like vaccinations, cases, deaths, hospitalizations to provide insights to public health authorities to prepare better for what is to come.

## Data Sources

| Dataset                             |                   Source                   |
| ----------------------------------- | :----------------------------------------: |
| Global Covid Data Set               |         https://ourworldindata.org         |
| U.S Hospitalization Data            |           https://healthdata.gov           |
| New York State Hospitalization Data |         https://health.data.ny.gov         |
| New York State Vaccination Data     |         https://health.data.ny.gov         |
| New York State Geographic Data      |             https://gis.ny.gov             |
| US Region Mobility Data             |    https://google.com/covid19/mobility/    |
| County Wise Cases And Deaths        | https://github.com/CSSEGISandData/COVID-19 |

## Exploratory Data Analysis

Todo:

1. Folder restructuring [EDA Folder]
2. A link in Readme pointing to the Folder
3. Important Analysis plots/one-liner

## Data Integrations

Todo:

1. Folder restructuring [Integration Folder]
2. A link in Readme pointing to the Folder
3. Final dataset generation is included in this
4. scripts to run those python tasks.

[Link to folder](https://github.com/AnishaMathur/cmpt-733-term-project/tree/main/integration)

Run below integration commands to generate datasets for the model and visualization

```
cd integration
python3 NY_hospitals_cleanup.py # will generate processed hospital dataset
python3 integration.py # will combine all datasets and output a merged dataset
```

## Forecasting Hospital Overload

The ML model aims to predict the risk of hospital overload in future covid waves by analysing important features and historical data.

Todo:

```
#steps to run the model
```

Link to notebook

## County-wise Analysis

A county-wise analysis of data of the state of New York, comparing regions that were the most impacted with regions that were the least impacted.

Todo:

1. Important graphs
2. Links to notebooks
3. one-liners

## Learning
