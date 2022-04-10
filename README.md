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

## Install dependencies

```
pip3 install -r requirements.txt 
```
install git-lfs from [here](https://git-lfs.github.com/)

## Exploratory Data Analysis

Todo:

1. Folder restructuring [EDA Folder]
2. A link in Readme pointing to the Folder
3. Important Analysis plots/one-liner


### Hospital Distribution
Visualization of hospital distribution across the state of New York and population density
[Link to notebook](https://github.com/AnishaMathur/cmpt-733-term-project/blob/main/EDA/Hospitals.ipynb)

<img width="1187" alt="Screenshot 2022-04-08 at 2 00 45 PM" src="https://user-images.githubusercontent.com/29632821/162529572-92995319-1141-4ef0-a4c1-cb02fce5f75a.png">

### Dynamics of Deaths and Cases accross Covid Waves

### Corrleation of Mobility and Covid Cases



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
python3 NY_vaccination.py # will generate processed vaccination dataset
python3 integration.py # will combine all datasets and output a merged dataset
```

## Forecasting Hospital Overload

The ML model aims to predict the risk of hospital overload in future covid waves by analysing important features and historical data.
The code for running the model can be found in this [notebook](https://github.com/AnishaMathur/cmpt-733-term-project/blob/main/model/ML3.ipynb).

Comparison model predictions (on the left) and actual county-wise hospital overload 14 days in advance.
<img width="1115" alt="Screenshot 2022-04-08 at 5 13 34 PM" src="https://user-images.githubusercontent.com/29632821/162548545-09dd3096-b2f0-4bf0-bd8e-8e3bd207ded5.png">

## County-wise Analysis

A county-wise analysis of data of the state of New York, comparing regions that were the most impacted with regions that were the least impacted.

Todo:

1. Important graphs
2. Links to notebooks
3. one-liners

## Learning

## Repository Organization:
This repo is organized in the following way:

The ``data`` folder contains the raw and processed datasets.

The ``EDA`` folder contains the notebooks associated with the EDA performed.

The ``integration`` folder contains the scripts used for integrating the data sources.

The `` analysis`` folder contains notebooks for the county-wise analysis.

The ``model`` folder contains the notebook with the final version of the model.

The ``archive`` folder contains old versions of the notebooks.
