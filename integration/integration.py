# %% [markdown]
# # **Data Integration**
#
# *   Vaccination
# *   Cases
# *   Deaths
# *   Hospitalization
# *   Mobility

import pandas as pd
import warnings


def process_mobility():
    path = '../data/raw_datasets/google_mobility_data/'
    mobility_2020 = pd.read_csv(
        path+'2020_US_Region_Mobility_Report.csv', parse_dates=['date'])
    mobility_2021 = pd.read_csv(
        path+'2021_US_Region_Mobility_Report.csv', parse_dates=['date'])
    mobility_2022 = pd.read_csv(
        path+'2022_US_Region_Mobility_Report.csv', parse_dates=['date'])

    mobility_2020 = mobility_2020[mobility_2020['sub_region_1'] == 'New York']
    mobility_2021 = mobility_2021[mobility_2021['sub_region_1'] == 'New York']
    mobility_2022 = mobility_2022[mobility_2022['sub_region_1'] == 'New York']

    mobility_2020['sub_region_2'] = mobility_2020['sub_region_2'].str.replace(
        ' County', '')
    mobility_2021['sub_region_2'] = mobility_2021['sub_region_2'].str.replace(
        ' County', '')
    mobility_2022['sub_region_2'] = mobility_2022['sub_region_2'].str.replace(
        ' County', '')

    mobility_2020 = mobility_2020.dropna(axis=0, subset=['sub_region_2'])
    mobility_2021 = mobility_2021.dropna(axis=0, subset=['sub_region_2'])
    mobility_2022 = mobility_2022.dropna(axis=0, subset=['sub_region_2'])

    mobility_2020.loc[mobility_2020['sub_region_2'].isin(
        ['New York', 'Bronx', 'Kings', 'Queens', 'Richmond']), 'sub_region_2'] = 'New York, Bronx, Kings, Richmond, Queens'
    mobility_2021.loc[mobility_2021['sub_region_2'].isin(
        ['New York', 'Bronx', 'Kings', 'Queens', 'Richmond']), 'sub_region_2'] = 'New York, Bronx, Kings, Richmond, Queens'
    mobility_2022.loc[mobility_2022['sub_region_2'].isin(
        ['New York', 'Bronx', 'Kings', 'Queens', 'Richmond']), 'sub_region_2'] = 'New York, Bronx, Kings, Richmond, Queens'

    mobility_2020.loc[mobility_2020['sub_region_2'].isin(
        ['St. Lawrence']), 'sub_region_2'] = 'St Lawrence'
    mobility_2021.loc[mobility_2021['sub_region_2'].isin(
        ['St. Lawrence']), 'sub_region_2'] = 'St Lawrence'
    mobility_2022.loc[mobility_2022['sub_region_2'].isin(
        ['St. Lawrence']), 'sub_region_2'] = 'St Lawrence'

    mobility_2020 = mobility_2020.drop(
        ['metro_area', 'iso_3166_2_code', 'census_fips_code', 'place_id'], axis=1)
    mobility_2021 = mobility_2021.drop(
        ['metro_area', 'iso_3166_2_code', 'census_fips_code', 'place_id'], axis=1)
    mobility_2022 = mobility_2022.drop(
        ['metro_area', 'iso_3166_2_code', 'census_fips_code', 'place_id'], axis=1)

    counties_to_exclude = ['Washington', 'Hamilton',
                           'Greene', 'Tioga', 'Seneca', 'Ontario, Seneca']
    mobility_2020 = mobility_2020[~mobility_2020['sub_region_2'].isin(
        counties_to_exclude)]
    mobility_2021 = mobility_2021[~mobility_2021['sub_region_2'].isin(
        counties_to_exclude)]
    mobility_2022 = mobility_2022[~mobility_2022['sub_region_2'].isin(
        counties_to_exclude)]

    mobility_2020 = mobility_2020.groupby(['country_region_code', 'country_region', 'sub_region_1', 'sub_region_2', 'date'])['retail_and_recreation_percent_change_from_baseline', 'grocery_and_pharmacy_percent_change_from_baseline',
                                                                                                                             'parks_percent_change_from_baseline', 'transit_stations_percent_change_from_baseline', 'workplaces_percent_change_from_baseline', 'residential_percent_change_from_baseline'].mean()
    mobility_2021 = mobility_2021.groupby(['country_region_code', 'country_region', 'sub_region_1', 'sub_region_2', 'date'])['retail_and_recreation_percent_change_from_baseline', 'grocery_and_pharmacy_percent_change_from_baseline',
                                                                                                                             'parks_percent_change_from_baseline', 'transit_stations_percent_change_from_baseline', 'workplaces_percent_change_from_baseline', 'residential_percent_change_from_baseline'].mean()
    mobility_2022 = mobility_2022.groupby(['country_region_code', 'country_region', 'sub_region_1', 'sub_region_2', 'date'])['retail_and_recreation_percent_change_from_baseline', 'grocery_and_pharmacy_percent_change_from_baseline',
                                                                                                                             'parks_percent_change_from_baseline', 'transit_stations_percent_change_from_baseline', 'workplaces_percent_change_from_baseline', 'residential_percent_change_from_baseline'].mean()

    mobility_2020 = mobility_2020.reset_index()
    mobility_2021 = mobility_2021.reset_index()
    mobility_2022 = mobility_2022.reset_index()

    mobility_2020 = mobility_2020.set_index(['date', 'sub_region_2'])
    mobility_2021 = mobility_2021.set_index(['date', 'sub_region_2'])
    mobility_2022 = mobility_2022.set_index(['date', 'sub_region_2'])

    mobility_2020 = mobility_2020.fillna(method='ffill')
    mobility_2021 = mobility_2021.fillna(method='ffill')
    mobility_2022 = mobility_2022.fillna(method='ffill')

    mobility_2020 = mobility_2020.reset_index()
    mobility_2021 = mobility_2021.reset_index()
    mobility_2022 = mobility_2022.reset_index()

    mobility = mobility_2020.append(mobility_2021, ignore_index=True)
    mobility = mobility.append(mobility_2022, ignore_index=True)
    mobility.to_parquet(
        '../data/processed_datasets/mobility.parquet.gzip', compression='gzip')
    return mobility

# **Merge Data**


def merge_all_datasets(mobility):
    path = '../data/processed_datasets/'

    vaccine = pd.read_parquet(path+'vaccination.parquet.gzip')
    cases = pd.read_parquet(path+'countywise_daily_cases.parquet.gzip')
    deaths = pd.read_parquet(path+'countywise_daily_deaths.parquet.gzip')
    hospitalization = pd.read_parquet(
        path+'NY_hospitals_beds_final_df.parquet')

    counties_to_keep = hospitalization['Facility County'].unique()
    counties_to_keep = list(
        map(str.capitalize, map(str.lower, counties_to_keep)))
    vaccine = vaccine.rename(columns={"Report as of": "date"})
    vaccine = vaccine[vaccine['County'].str.capitalize().isin(
        counties_to_keep)]
    vaccine.head()

    cases = cases[cases['county'].str.capitalize().isin(counties_to_keep)]
    cases.head()

    deaths = deaths[deaths['county'].str.capitalize().isin(counties_to_keep)]
    deaths.head()

    hospitalization = hospitalization.reset_index()
    hospitalization['Facility County'] = hospitalization['Facility County'].str.title()
    hospitalization = hospitalization.rename(
        columns={'As of Date': 'date', 'Facility County': 'county'})
    hospitalization = hospitalization.drop(['POP2020'], axis=1)
    hospitalization = hospitalization.drop_duplicates()

    vaccine = vaccine[(vaccine['date'] < '2022-02-28') &
                      (vaccine['date'] > '2020-03-25')]
    cases = cases[(cases['date'] < '2022-02-28') &
                  (cases['date'] > '2020-03-25')]
    deaths = deaths[(deaths['date'] < '2022-02-28') &
                    (deaths['date'] > '2020-03-25')]
    hospitalization = hospitalization[(
        hospitalization['date'] < '2022-02-28') & (hospitalization['date'] > '2020-03-25')]
    mobility = mobility[(mobility['date'] < '2022-02-28') &
                        (mobility['date'] > '2020-03-25')]

    final_df = pd.merge(cases, deaths, how='left', left_on=[
                        'county', 'date'], right_on=['county', 'date'])
    temp_vaccine = vaccine[['County', 'POP2020']]
    temp_vaccine = temp_vaccine.drop_duplicates()
    final_df = pd.merge(final_df, temp_vaccine, how='left',
                        left_on=['county'], right_on=['County'])

    final_df = final_df.drop(['County'], axis=1)
    vaccine_2 = vaccine.drop(['POP2020'], axis=1)
    final_df = pd.merge(final_df, vaccine_2, how='left', left_on=[
                        'county', 'date'], right_on=['County', 'date'])
    final_df = final_df.drop(['Region', 'County'], axis=1)

    final_df['Partially Vaccinated'] = final_df['Partially Vaccinated'].fillna(
        0)
    final_df['Fully Vaccinated'] = final_df['Fully Vaccinated'].fillna(0)
    final_df['Non Vaccinated'] = final_df['Non Vaccinated'].fillna(0)

    final_df['Partially Vaccinated'] = final_df['Partially Vaccinated'].fillna(
        0)
    final_df['Fully Vaccinated'] = final_df['Fully Vaccinated'].fillna(0)
    final_df['Non Vaccinated'] = final_df['Non Vaccinated'].fillna(0)
    final_df['Partially Vaccinated per Population'] = final_df['Partially Vaccinated per Population'].fillna(
        0)
    final_df['Fully Vaccinated per Population'] = final_df['Fully Vaccinated per Population'].fillna(
        0)
    final_df['Non Vaccinated per Population'] = final_df['Non Vaccinated per Population'].fillna(
        0)

    final_df = pd.merge(final_df, hospitalization, how='inner', left_on=[
        'date', 'county'], right_on=['date', 'county'])
    final_df = pd.merge(final_df, mobility, left_on=['date', 'county'], right_on=[
        'date', 'sub_region_2'], how='left')
    final_df = final_df.drop(
        ['sub_region_2', 'sub_region_1', 'country_region', 'country_region_code'], axis=1)

    x = final_df.set_index(['county', 'date']).sort_values(
        by=['county', 'date']).groupby(level=0).ffill()
    x = x.reset_index().sort_values(by=['date']).reset_index()
    # check_missing_dates(x, 'date')
    x.to_parquet(
        '../data/processed_datasets/final_dataset_v3.parquet', compression='gzip')


def check_missing_dates(df, dateCol):
    subset = df.copy()
    subset = subset.set_index(dateCol)
    subset.index = pd.to_datetime(subset.index)
    print(pd.date_range(
        start="2020-03-26", end="2022-03-01").difference(subset.index))


if __name__ == "__main__":
    warnings.filterwarnings('ignore')
    mobility = process_mobility()
    merge_all_datasets(mobility)
