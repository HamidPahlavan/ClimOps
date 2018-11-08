# -*- coding: utf-8 -*-
"""
Created on Wed Nov  7 19:31:11 2018

@author: Hamid
"""
# import packages
import pandas as pd
import numpy as np

# loading datasets
ycom = pd.read_csv('YCOM_2018_Data.csv', encoding='latin-1')
census = pd.read_csv('us-census-demographic-data/acs2015_county_data.csv')

# Deselct Puerto Rico from census, since Ycom data doesn't cover this state.
census = census.iloc[:3142]

# selecting only the county rows and reseting the index.
ycom_county = ycom.loc[ycom['GeoType'] == 'County']
ycom_county = ycom_county.reset_index(drop=True)

# Separating the counties and states from 'GeoType' column and add those as
# separated columns to the 'ycom_county' dataframe.
county_state_sep = pd.DataFrame(ycom_county.GeoName.str.split(',').tolist())
ycom_county['State'] = county_state_sep[1]
ycom_county['County'] = county_state_sep[0]

# Dropping 'county' and 'Parish' words and the last whitespace
# from the counties.
ycom_county['County'] = ycom_county['County'].str.replace('County', '')
ycom_county['County'] = ycom_county['County'].str.replace('Parish', '')
ycom_county['County'] = ycom_county['County'].str.strip()

# test if the counties are the same and in order in two datasets.
if np.all(ycom_county['County'] == census['County']):
    print('Yaaaaay!')
