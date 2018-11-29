"""
This module uses data from the Yale Climate Opinions Maps 2018 (YCOM)
and the 2015 Census to create a joint data set matching Climate opinions
to Census data at the County Level.
"""
import pandas as pd
import numpy as np

def get_data(filepath):
    """
    Function to read in data and return a dataframe.
    Takes in a string that is a filepath to csv file
    Returns a dataframe
    """
    dataFrame = pd.read_csv(filepath, encoding='latin-1')
    return dataFrame


def select_geography(ycom_df, geography):
    """
    Helper function for get_ycom_counties
    Takes in Data frame of YCOM 2018 data and filters
    the rows of data within the given geography:
    'National', 'State', 'County', 'cd115', 'CBSA'
    """
    # selecting only the county rows and reseting the index.
    ycom_county = ycom_df.loc[ycom_df['GeoType'] == geography]
    ycom_county = ycom_county.reset_index(drop=True)
    return ycom_county

def fix_ycom_county_names(ycom_county):
    """
    Function to fix county names to match census.
    Takes in Data frame of YCOM 2018 data. Returns data frame with
    names of counties separate from states with names in correct format
    and fixing names with special characters.
    """
    # Separate the county name from the state nme
    county_state_sep = pd.DataFrame(ycom_county.GeoName.str.split(',').tolist())
    #keep state name in separate column
    ycom_county['State'] = county_state_sep[1]
    #Keep county names in separate columns
    ycom_county['County'] = county_state_sep[0]
    #Remove the words county, parish
    ycom_county['County'] = ycom_county['County'].str.replace('County', '')
    ycom_county['County'] = ycom_county['County'].str.replace('Parish', '')
    #remove any extra spaces
    ycom_county['County'] = ycom_county['County'].str.strip()
    #fix name with special character
    ycom_county.iloc[1802,60] = 'Dona Ana'
    return ycom_county

def get_ycom_counties(ycom_df):
    """
    Function to clean data to obtain only counties in ycom data
    and fix names to match census.
    Takes in Data frame of YCOM 2018 data
    """
    ycom_county= select_geography(ycom_df, 'County')
    ycom_county= fix_ycom_county_names(ycom_county)
    return ycom_county

def get_census_counties(census_df):
    """
    Filter out counties not included in the YCOM DATA
    [all areas in the Puerto Rico Territory]
    """
    census = census_df[census_df['State'] != 'Puerto Rico']
    #fix name with special character
    census.iloc[1802,2] = 'Dona Ana'
    return census


def join_data(ycom_county, census_county):
    """
    getting one dataframe from the two datasets
    """

    data = pd.concat(([ycom_county,census_county]),axis = 1)
    return data
