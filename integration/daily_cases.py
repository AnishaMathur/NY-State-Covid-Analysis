
import pandas as pd
import numpy as np
import geopandas as gpd

columns_to_drop = ['iso2', 'iso3', 'code3', 'FIPS',
                   'Province_State', 'Country_Region', 'Lat', 'Long_', 'Combined_Key']

street_map = gpd.read_file(
    '../data/raw_datasets/NYS_Civil_Boundaries.shp.zip',)


def clean_daily_cases():
    df = pd.read_csv('../data/raw_datasets/US_Daily_Covid_Cases.csv')
    df = (df[df.Province_State == 'New York'])
    # print(df.head())

    df = df.drop(columns_to_drop, axis=1)

    df = df.rename(columns={"Admin2": "county"})

    df_cases = df.drop('UID', axis=1).melt(id_vars=['county'])

    df_cases = df_cases.rename(columns={'variable': 'date'})

    df_cases = df_cases.replace(to_replace='St. Lawrence', value='St Lawrence')

    df_cases.drop(df_cases.index[df_cases['county']
                  == 'Unassigned'], inplace=True)

    df_cases.drop(df_cases.index[df_cases['county']
                  == 'Out of NY'], inplace=True)

    df_cases = df_cases.replace(to_replace='New York',
                                value='New York, Bronx, Kings, Richmond, Queens')
    df_cases = df_cases.replace(
        to_replace='Bronx', value='New York, Bronx, Kings, Richmond, Queens')
    df_cases = df_cases.replace(
        to_replace='Kings', value='New York, Bronx, Kings, Richmond, Queens')
    df_cases = df_cases.replace(to_replace='Richmond',
                                value='New York, Bronx, Kings, Richmond, Queens')
    df_cases = df_cases.replace(
        to_replace='Queens', value='New York, Bronx, Kings, Richmond, Queens')

    df_cases = df_cases.rename(columns={'value': 'cases'})

    df_cases = df_cases.groupby(["county", "date"]).agg(
        {"cases": "sum"}).reset_index()

    shape_popu = street_map[['NAME', 'COUNTY', 'POP2020']]

    shape_popu_grouped = shape_popu.groupby(
        'COUNTY')['POP2020'].sum().reset_index()

    NY_cases_by_population = pd.merge(
        df_cases, shape_popu_grouped, left_on='county', right_on='COUNTY', how='left')

    NY_cases_by_population['cases_by_pop'] = NY_cases_by_population.apply(
        lambda x: x['cases']/x['POP2020'], axis=1)

    to_drop = ['COUNTY', 'POP2020']
    NY_cases_by_population = NY_cases_by_population.drop(to_drop, axis=1)

    NY_cases_by_population = NY_cases_by_population.rename(
        columns={'cases': 'daily_cases_cummulative'})

    NY_cases_by_population = NY_cases_by_population.rename(
        columns={'cases_by_pop': 'daily_cases_by_population_cummulative'})

    NY_cases_by_population['date'] = pd.to_datetime(
        NY_cases_by_population['date'])

    NY_cases_by_population.sort_values(by='date', inplace=True)

    df_cummulative = NY_cases_by_population

    df_cummulative.sort_values(by='date', inplace=True)

    df_transform = df_cummulative

    df_transform.sort_values(["county", "date"],
                             axis=0, ascending=True,
                             inplace=True)

    df_transform.set_index(['county', 'date'], inplace=True)

    df_daily = df_transform.groupby(level=0)['daily_cases_cummulative'].diff()

    df_daily = df_daily.reset_index()

    df_daily = df_daily.rename(
        columns={'daily_cases_cummulative': 'daily_cases'})

    df_daily['daily_cases'] = df_daily['daily_cases'].replace(np.nan, 0)

    df_daily[df_daily['daily_cases'] < 0]  # as mis-reported data

    df_daily['daily_cases'] = df_daily['daily_cases'].apply(
        lambda x: x if x > 0 else 0)

    df_daily.to_parquet(
        '../data/processed_datasets/countywise_daily_cases.parquet.gzip', compression='gzip')


if __name__ == "__main__":
    clean_daily_cases()
