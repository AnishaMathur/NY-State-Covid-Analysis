import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import geopandas as gpd
from shapely.geometry import Point, Polygon
from matplotlib.pyplot import figure

df = pd.read_csv('../data/raw_datasets/US_Daily_Covid_Deaths.csv')

df_NY = (df[df.Province_State == 'New York'])

df_NY = df_NY.rename(columns={"Admin2": "county"})

columns_to_drop = ['iso2','iso3','code3','FIPS','Province_State','Country_Region','Lat','Long_','Combined_Key','Population']

df_NY = df_NY.drop(columns_to_drop, axis=1)

df_deaths = df_NY.drop('UID',axis=1).melt(id_vars=['county'])

df_deaths = df_deaths.rename(columns={'variable': 'date'})

street_map = gpd.read_file('../data/raw_datasets/NYS_Civil_Boundaries.shp.zip',)

df_deaths = df_deaths.replace(to_replace='New York',value= 'New York, Bronx, Kings, Richmond, Queens')
df_deaths = df_deaths.replace(to_replace='Bronx',value= 'New York, Bronx, Kings, Richmond, Queens')
df_deaths = df_deaths.replace(to_replace='Kings',value= 'New York, Bronx, Kings, Richmond, Queens')
df_deaths = df_deaths.replace(to_replace='Richmond',value= 'New York, Bronx, Kings, Richmond, Queens')
df_deaths = df_deaths.replace(to_replace='Queens',value= 'New York, Bronx, Kings, Richmond, Queens')

df_deaths = df_deaths.replace(to_replace='St. Lawrence',value= 'St Lawrence')

df_deaths.drop(df_deaths.index[df_deaths['county'] == 'Unassigned'], inplace = True)

df_deaths.drop(df_deaths.index[df_deaths['county'] == 'Out of NY'], inplace = True)

df_deaths = df_deaths.rename(columns={'value': 'deaths'})


df_deaths = df_deaths.groupby(["county", "date"]).agg({"deaths": "sum"}).reset_index()

shape_popu = street_map[['NAME', 'COUNTY', 'POP2020']]

shape_popu_grouped = shape_popu.groupby('COUNTY')['POP2020'].sum().reset_index()

NY_deaths_by_population = pd.merge(df_deaths, shape_popu_grouped, left_on='county', right_on='COUNTY', how='left')

NY_deaths_by_population['deaths_by_pop'] = NY_deaths_by_population.apply(lambda x: x['deaths']/x['POP2020'], axis=1)

NY_deaths_by_population = NY_deaths_by_population.rename(columns={'deaths': 'cummulative_deaths'})

NY_deaths_by_population = NY_deaths_by_population.rename(columns={'deaths_by_pop': 'cummulative_deaths_by_population'})

NY_deaths_by_population['date'] = pd.to_datetime(NY_deaths_by_population['date'])

NY_deaths_by_population.to_parquet('../data/processed_datasets/countywise_cummulative_deaths.parquet.gzip', compression='gzip')


