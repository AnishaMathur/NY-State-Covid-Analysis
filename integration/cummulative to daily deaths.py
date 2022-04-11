import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import geopandas as gpd
from shapely.geometry import Point, Polygon
import matplotlib.animation as ani
from matplotlib.pyplot import figure
import geopandas as gpd
from shapely.geometry import Point, Polygon

df_cummulative = pd.read_parquet('../data/processed_datasets/countywise_cummulative_deaths.parquet.gzip')

df_cummulative.sort_values(by='date', inplace=True)

df_transform = df_cummulative

df_transform.sort_values(["county", "date"],
               axis = 0, ascending = True,
               inplace = True)

df_transform.set_index(['county','date'], inplace=True)

df_daily = df_transform.groupby(level=0)['cummulative_deaths'].diff()

df_daily = df_daily.reset_index()

df_daily = df_daily.rename(columns={'cummulative_deaths': 'daily_deaths'})

df_daily['daily_deaths'] = df_daily['daily_deaths'].replace(np.nan, 0)

df_daily[df_daily['daily_deaths']<0] #mis-reported data

df_daily['daily_deaths'] = df_daily['daily_deaths'].apply(lambda x : x if x > 0 else 0)

df_daily.to_parquet('../data/processed_datasets/countywise_daily_deaths.parquet.gzip', compression='gzip')


