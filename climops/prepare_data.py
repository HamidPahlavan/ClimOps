"""
This module is used to prepare data from the the 2015 Census,
2018 Yale Climate Opinion Maps (YCOM) and land area datasets,
such that they can be combined.
"""
import numpy as np
import pandas as pd

def scale_census_variables(census):
    """
    Function to scale Men, Women, Employed and Citizen
    variables in census by TotalPop to get a percentage.
    Input: dataframe of census data.
    Output: dataframe of census data scaled to population (%).
    """
    census.Men = 100*census.Men/census.TotalPop
    census.Women = 100*census.Women/census.TotalPop
    census.Citizen = 100*census.Citizen/census.TotalPop
    census.Employed = 100*census.Employed/census.TotalPop
    return census


def remove_census_not_in_ycom(census):
    """
    Function to remove data for Puerto Rico,
    which is not included in YCOM data.
    Input: dataframe of census data
    Output: dataframe of census data with Puerto
    Rico removed
    """
    census = census[census['State'] != 'Puerto Rico']
    return census


def remove_not_in_land_area(dframe):
    """
    Function to remove data for Puerto Rico,
    which is not included in YCOM data
    """
    removerows = np.array([81, 2412])
    dframe = dframe.drop(dframe.index[removerows])
    dframe = dframe.reset_index(drop=True)
    return dframe


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


def simplify_county_names(dframe):
    """
    Removes words 'county' and 'parish' and extra white space
    from county field of a dataframe
    """
    dframe['County'] = dframe['County'].str.replace('County', '')
    dframe['County'] = dframe['County'].str.replace('Parish', '')
    dframe['County'] = dframe['County'].str.strip()
    return dframe


def fix_ycom_county_names(ycom_county):
    """
    Function to fix county names to match census.
    Takes in Data frame of YCOM 2018 data. Returns data frame with
    names of counties separate from states with names in correct format.
    """
    # Separate the county name from the state nme
    county_state_sep = pd.DataFrame(ycom_county.GeoName.str.split(',').tolist())
    # Keep state name in separate column
    ycom_county['State'] = county_state_sep[1]
    # Keep county names in separate columns
    ycom_county['County'] = county_state_sep[0]
    # Remove words 'county' and 'parish' and extra white space
    ycom_county = simplify_county_names(ycom_county)
    return ycom_county


def remove_land_area_not_in_census(land_area_data):
    """
    Removing rows which are in land area but not census
    """
    removerows = np.array([92, 1654, 2418, 2917, 2922, 2950])
    land_area_data = land_area_data.drop(land_area_data.index[removerows])
    land_area_data = land_area_data.reset_index(drop=True)
    return land_area_data


def fix_land_area_county_names(land_area_data, census):
    """
    Function to fix land area county names to match census and ycom
    Takes in Data frame of land area data. Returns data frame with
    names of counties with names in correct format.
    """
    # Remove words 'county' and 'parish' and extra white space
    land_area_data = simplify_county_names(land_area_data)

    # Match county names to census
    land_area_data.loc[67:96, 'County'] = census.loc[67:96, 'County']
    land_area_data.loc[1141:1141, 'County'] = 'LaSalle'
    land_area_data.loc[1762:1762, 'County'] = 'Carson City'
    land_area_data.loc[1801:1801, 'County'] = 'Doña Ana'
    land_area_data.loc[2913:2951, 'County'] = census.loc[2913:2951, 'County']
    return land_area_data


def get_ycom_counties(ycom_df):
    """
    Function to clean data to obtain only counties in ycom data
    and fix names to match census.
    Takes in Data frame of YCOM 2018 data
    """
    ycom_county = select_geography(ycom_df, 'County')
    ycom_county = fix_ycom_county_names(ycom_county)
    return ycom_county


def fix_ycom_descriptions(ycom_meta):
    """
    Shortens all descriptions for YCOM variables.
    Then shortens the longest ones even more so they fit in Bokeh's dropdown boxes.
    """
    for yind in range(3, len(ycom_meta)):
        ycom_meta['VARIABLE DESCRIPTION'][yind] = (
            ycom_meta['VARIABLE DESCRIPTION'][yind][25:].capitalize())

    desc_p1 = ycom_meta['VARIABLE DESCRIPTION'][31][:117]
    desc_p2 = ycom_meta['VARIABLE DESCRIPTION'][23][139:]
    ycom_meta['VARIABLE DESCRIPTION'][31] = desc_p1 + desc_p2
    desc_p1 = ycom_meta['VARIABLE DESCRIPTION'][32][:116]
    desc_p2 = ycom_meta['VARIABLE DESCRIPTION'][23][138:]
    ycom_meta['VARIABLE DESCRIPTION'][32] = desc_p1 + desc_p2
    return ycom_meta


def select_land_area_county(land_area_data):
    """
    Selecting only county level data from land area data
    """
    land_area_county = land_area_data['Areaname']
    land_area_county = pd.DataFrame(land_area_county.str.split(',').tolist())[0]
    land_area_data = land_area_data[~land_area_county.str.isupper()]
    land_area_data['County'] = land_area_county
    land_area_data = land_area_data.reset_index(drop=True)
    return land_area_data


def add_missing_land_areas(land_area_data):
    """
    Adding land area values where missing
    Values just taken from wikipedia...
    #89 Skagway Municipality 452
    #92 Wrangell City and Borough 2,541
    #250 Broomfield 33.55
    """
    land_area_data.loc[89:89, 'LND110200D'] = 452.0
    land_area_data.loc[92:92, 'LND110200D'] = 2541.0
    land_area_data.loc[250:250, 'LND110200D'] = 33.55
    return land_area_data


def join_data(ycom_county, census, land_area_data):
    """
    Getting one dataframe from the three datasets
    """
    census['LogPopDensity'] = np.log10(census['TotalPop']/land_area_data['LND110200D'])
    data = pd.concat(([ycom_county, census]), axis=1)
    return data
