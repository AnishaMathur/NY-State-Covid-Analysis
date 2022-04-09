import pandas as pd
from dataprep.eda import plot
import geopandas as gpd


path = '../data'

# load the actual datasets
df_NY = pd.read_csv(
    path+'/raw_datasets/New_York_State_Statewide_COVID-19_Vaccination_Data_by_County.csv', parse_dates=['Report as of'])
street_map = gpd.read_file(
    path + '/raw_datasets/NYS_Civil_Boundaries.shp.zip',)

# select the required columns
NY_population = street_map[['NAME', 'COUNTY', 'POP2020']]
NY_population_grouped = NY_population.groupby(
    'COUNTY')['POP2020'].sum().reset_index()

# data preprocessing

# make names of counties consistent across all datasets
df_NY.loc[df_NY['County'].isin(['New York', 'Bronx', 'Kings', 'Queens', 'Richmond']),
          'County'] = 'New York, Bronx, Kings, Richmond, Queens'
df_NY.loc[df_NY['County'].isin(['St. Lawrence']), 'County'] = 'St Lawrence'

# join county population to vaccination dataset
NY_vaccine_by_population = pd.merge(
    df_NY, NY_population_grouped, left_on='County', right_on='COUNTY', how='left')

# create vaccination categories
NY_vaccine_by_population = NY_vaccine_by_population.rename(
    columns={'First Dose': 'Partially Vaccinated', 'Series Complete': 'Fully Vaccinated'})
NY_vaccine_by_population['Non Vaccinated'] = NY_vaccine_by_population['POP2020'] - \
    NY_vaccine_by_population['Partially Vaccinated']
NY_vaccine_by_population = NY_vaccine_by_population.drop(
    ['COUNTY'], axis=1)

# calculate vaccination per population
NY_vaccine_by_population['Partially Vaccinated per Population'] = NY_vaccine_by_population['Partially Vaccinated'] / \
    NY_vaccine_by_population['POP2020']
NY_vaccine_by_population['Fully Vaccinated per Population'] = NY_vaccine_by_population['Fully Vaccinated'] / \
    NY_vaccine_by_population['POP2020']
NY_vaccine_by_population['Non Vaccinated per Population'] = NY_vaccine_by_population['Non Vaccinated'] / \
    NY_vaccine_by_population['POP2020']

# save processed dataset as a parquet file
NY_vaccine_by_population.to_parquet(
    path + '/processed_datasets/vaccination.parquet.gzip', compression='gzip')
