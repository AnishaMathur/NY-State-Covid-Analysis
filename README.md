## Introduction

This project showcases COVID analysis for the state of New York. We draw from different data sources like vaccinations, cases, deaths, hospitalizations and mobility data to provide insights to public health authorities to prepare better for what is to come.

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

### Hospital Distribution
Visualization of hospital distribution across the state of New York and population density
[Link to notebook](https://github.com/AnishaMathur/cmpt-733-term-project/blob/main/EDA/Hospitals.ipynb)

<img width="1187" alt="Screenshot 2022-04-08 at 2 00 45 PM" src="https://user-images.githubusercontent.com/29632821/162529572-92995319-1141-4ef0-a4c1-cb02fce5f75a.png">

### Dynamics of Deaths and Cases accross Covid Waves
During the first wave, number of deaths due to Covid was higher in counties with higher population,over the course of Pandemic, the deaths were more among the least densely populated counties and in subsequent waves, death rate was higher in less populated county.
[Link to notebook](https://github.com/AnishaMathur/cmpt-733-term-project/blob/main/analysis/Deeper%20analysis%20of%20coutywise%20deaths.ipynb)

<img width="1023" alt="Screen Shot 2022-04-09 at 11 15 37 PM" src="https://user-images.githubusercontent.com/65904510/162605111-66be53db-7591-420f-9fb9-7b5d81ccce79.png">

### Vaccination Trends
Vaccination trend for US and Canada for the whole duration of COVID-19 shows that even though US started administering vaccines before Canada, at the moment, Canada has a higher percentage of vaccinated population. [Link to notebook](https://github.com/AnishaMathur/cmpt-733-term-project/blob/main/EDA/EDA_Vaccination.ipynb)

![global_vaccination](https://user-images.githubusercontent.com/24526992/162610790-0c4094eb-37e8-4b3b-bbaf-fb525294c59f.png)

## Data Integrations

[Link to folder](https://github.com/AnishaMathur/cmpt-733-term-project/tree/main/integration)

Run below integration commands to generate datasets for the model and visualization

```
cd integration
python3 NY_hospitals_cleanup.py # will generate processed hospital dataset
python3 NY_vaccination.py # will generate processed vaccination dataset
python3 NY_daily_cases.py # will generate processed daily cases dataset
python3 NY_daily_deaths.py # will generate processed daily deaths dataset
python3 integration.py # will combine all the above datasets and output a merged dataset
```

## Forecasting Hospital Overload

The ML model aims to predict the risk of hospital overload in future covid waves by analysing important features and historical data.
The code for running the model can be found in this [notebook](https://github.com/AnishaMathur/cmpt-733-term-project/blob/main/model/ML3_v3.ipynb).

Comparison model predictions (on the left) and actual county-wise hospital overload 14 days in advance.
<img width="1223" alt="Screen Shot 2022-04-10 at 10 15 39 PM" src="https://user-images.githubusercontent.com/42242797/162765209-d7d030fe-f444-4ceb-80ff-39a97a7cb991.png">


## County-wise Analysis

A county-wise analysis of data of the state of New York, comparing regions that were the most impacted with regions that were the least impacted.

The effect of Vaccination on number of cases, deaths and hospitalizations varies for each county. There isn't any fixed pattern that we can observe. This can be visualised for various waves from the graphs plotted in this [notebook](https://github.com/AnishaMathur/cmpt-733-term-project/blob/main/analysis/visualisation.ipynb).

The below plots depict the state of New York's third wave. We can observe how each county reacts to vaccination (bottom left plot), in terms of case count (top left plot), death count (top right corner) and hospitalization count (bottom right corner).
![vaccine_map](https://user-images.githubusercontent.com/24526992/162612179-6506398e-95d3-4bca-ad1c-2a0c351dc7c8.png)

Examples of some of the counties' trends are as listed below:

|                 | St. Lawrence | Jefferson |	Allegany|
|:---------------:|:------------:|:---------:|:---------:               
| Vaccination     |	High         |	Low      |	Medium  |
| Cases           |	High         |	Medium   |	High    |
| Deaths          |	Low          |	High     |	Low     |
| Hospitalization |	Medium       |	Low      |	Medium  |

## Repository Structure:
This repo is organized in the following way:

The ``data`` folder contains the raw and processed datasets.

The ``EDA`` folder contains the notebooks associated with the EDA performed.

The ``integration`` folder contains the scripts used for integrating the data sources.

The ``analysis`` folder contains notebooks for the county-wise analysis.

The ``model`` folder contains the notebook with the final version of the model.

The ``notebooks`` folder contains other notebooks used.

The ``archive`` folder contains old versions of the notebooks.
