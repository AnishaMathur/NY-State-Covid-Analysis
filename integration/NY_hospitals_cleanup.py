# Import Packages
import pandas as pd
import matplotlib.pyplot as plt
from dataprep.eda import plot
import sys
import numpy as np
import geopandas as gpd
from shapely.geometry import Point, Polygon

# Load Hospital Dataset
dataset_name = 'New_York_State_Statewide_COVID-19_Hospitalizations_and_Beds.csv'
maps_data_path = '../data/raw_datasets/NYS_Civil_Boundaries.shp.zip'
# Columns to keep
keep_columns = ['As of Date', 'Facility Name', 'Facility County',
                'Patients Age 55 to 64 Years', 'Patients Age 65 to 74 Years', 'Patients Age 75 to 84 Years',
                'Patients Currently Hospitalized', 'Patients Newly Admitted', 'Patients Positive After Admission',
                'Patients Currently in ICU', 'Patients Currently ICU Intubated', 'Total Beds', 'Number of Beds Available', 'Number of ICU Beds', 'Number of ICU Beds Available', 'POP2020']

# functions


def make_upper(row):
    return row['COUNTY'].upper()


# Group Counties into a single one [NEW YORK, BRONX, KINGS, RICHMOND, QUEENS] --> 'NEW YORK, BRONX, KINGS, RICHMOND, QUEENS'
# in order to make the county columns similar to maps dataset
def group_counties(row):
    if row['Facility County'] in ['NEW YORK', 'BRONX', 'KINGS', 'RICHMOND', 'QUEENS']:
        return 'NEW YORK, BRONX, KINGS, RICHMOND, QUEENS'
    elif row['Facility County'] == 'ST.LAWRENCE':
        return 'ST LAWRENCE'
    else:
        return row['Facility County']


def map_staffed_beds_column(row):
    if row['As of Date'] <= pd.Timestamp('05-19-2021'):
        return row['Total Staffed Beds']
    else:
        return row['Total Staffed Acute Care Beds']


def map_bed_availability_column(row):
    if row['As of Date'] <= pd.Timestamp('05-19-2021'):
        return row['Total Staffed Beds Currently Available']
    else:
        return row['Total Staffed Acute Care Beds'] - row['Total Staffed Acute Care Beds Occupied']


def map_ICU_beds_column(row):
    if row['As of Date'] <= pd.Timestamp('05-19-2021'):
        return row['Total Staffed ICU Beds']
    else:
        return row['Total Staffed ICU Beds 1']


def map_ICU_bed_availability_column(row):
    if row['As of Date'] <= pd.Timestamp('05-19-2021'):
        return row['Total Staffed ICU Beds Currently Available']
    else:
        return row['Total Staffed ICU Beds 1'] - row['Total Staffed ICU Beds Currently Occupied']


def county_wise_features(all_data, output_df):
    subset = all_data[['As of Date', 'Facility Name', 'Facility County', 'Total Beds',
                       'Number of Beds Available', 'Number of ICU Beds', 'Number of ICU Beds Available']]
    grouped = subset.groupby(by=['As of Date', 'Facility County']).sum()
    grouped.rename(columns={
        "Total Beds": 'Total Beds By County',
        "Number of Beds Available": 'Number of Beds Available By County',
        "Number of ICU Beds": 'Number of ICU Beds By County',
        "Number of ICU Beds Available": 'Number of ICU Beds Available By County',
    }, inplace=True)
    joined = output_df.join(grouped, how="left", on=[
        'As of Date', 'Facility County'])

    for col in ['Total Beds By County', 'Number of ICU Beds By County']:
        joined[col+' per thousand ppl'] = joined[col]/(joined['POP2020']/1000)

    copied = joined.copy()
    x = copied.sort_values(by=['Facility Name', 'As of Date']).set_index(
        ['Facility Name', 'As of Date'], drop=True)

    to_drop = ['JAVITS CENTER HOSPITAL', 'MAIMONIDES CROWN HEIGHTS', 'MERCY HOSPITAL-ORCHARD PARK DIVISION', 'MOUNT SINAI SAMARITANS PURSE', 'NYC H+H - BILLIE JEAN KING TENNIS CENTER',
               'NYC H+H ROOSEVELT ISLAND MEDICAL CENTER', 'NYP - RYAN LARKIN FIELD HOSPITAL', 'SOUTH NASSAU COMMUNITIES HOSPITAL OFF-CAMPUS EMERGENCY DEPARTMENT', 'USNS COMFORT HOSPITAL']
    copied = copied[~copied['Facility Name'].isin(to_drop)]
    x = copied.sort_values(by=['Facility Name', 'As of Date']).set_index(
        ['Facility Name', 'As of Date'], drop=True)
    y = x.groupby(level=0).ffill()

    check_missing_dates(y.reset_index(), 'As of Date')
    subset = fill_missing_dates(y.reset_index(), '2021-11-24', '2021-11-25')
    subset = fill_missing_dates(
        subset.reset_index(), '2021-12-24', '2021-12-25')
    check_missing_dates(subset.reset_index(), 'As of Date')
    return subset


def check_missing_dates(df, dateCol):
    subset = df.copy()
    subset = subset.set_index(dateCol)
    subset.index = pd.to_datetime(subset.index)
    print(pd.date_range(
        start="2020-03-26", end="2022-03-01").difference(subset.index))


def fill_missing_dates(subset, prev_date, actual_date):
    modify = subset[subset['As of Date'].isin([prev_date])].copy()
    modify['As of Date'] = pd.to_datetime(actual_date)
    subset = subset.append(modify)
    subset.sort_values(by=['As of Date', 'Facility Name'],
                       ascending=True, inplace=True)
    subset = subset.set_index(['As of Date', 'Facility Name'])
    return subset


if __name__ == "__main__":

    all_data = pd.read_csv('../data/raw_datasets/' +
                           dataset_name, parse_dates=['As of Date'])

    # Adding population information for each county in the dataset.
    # Load maps data from New York State
    street_map = gpd.read_file(maps_data_path)
    street_map['Facility County'] = street_map.apply(
        lambda x: make_upper(x), axis=1)
    # Need to groupby county and sum the populations to include city and town
    street_map_grouped = street_map.groupby('Facility County').sum()['POP2020']

    all_data['Facility County'] = all_data.apply(
        lambda x: group_counties(x), axis=1)

    all_data = pd.merge(all_data, street_map_grouped,
                        how="left", on=["Facility County"])
    all_data['Patients Currently Hospitalized_by_pop'] = all_data['Patients Currently Hospitalized'] / \
        all_data['POP2020'] * 100
    all_data['Patients Currently in ICU_by_pop'] = all_data['Patients Currently in ICU'] / \
        all_data['POP2020'] * 100

    # Mapping Column From May 19th onwards Staffed Beds
    all_data['Total Beds'] = all_data.apply(
        lambda x: map_staffed_beds_column(x), axis=1)
    # Mapping Column From May 19th onwards Staffed Beds Occupied
    all_data['Number of Beds Available'] = all_data.apply(
        lambda x: map_bed_availability_column(x), axis=1)
    # Mapping Column From May 19th onwards ICU Beds
    all_data['Number of ICU Beds'] = all_data.apply(
        lambda x: map_ICU_beds_column(x), axis=1)
    # Mapping Column From May 19th onwards ICU Beds
    all_data['Number of ICU Beds Available'] = all_data.apply(
        lambda x: map_ICU_bed_availability_column(x), axis=1)

    output_df = all_data[keep_columns]
    subset = county_wise_features(all_data, output_df)
    subset.to_parquet(
        '../data/processed_datasets/NY_hospitals_beds_final_df.parquet', compression='gzip')
