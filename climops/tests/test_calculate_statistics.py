"""
Test module for functions in estimate statistics
"""

import unittest
import prepare_data
import pandas as pd
import numpy as np

import calculate_statistics
import prepare_data
  
def prep_census_data():
    """
    Helper function to prep census data to use in tests.
    """
    # Loading census data
    census = pd.read_csv('../data/acs2015_county_data.csv')
     # Scaling Men, Women, Employed and Citizen by TotalPop to get a percentage
    census = prepare_data.scale_census_variables(census)
     # Removing counties not in ycom data (i.e. puerto rico)
    census = prepare_data.remove_census_not_in_ycom(census)
    # Removing counties not in land area data
    census = prepare_data.remove_not_in_land_area(census)
    return census

def prep_ycom_data():
    """
    Helper function to prep ycom data for tests
    """
    # Loading ycom data
    ycom = pd.read_csv('../data/YCOM_2018_Data.csv', encoding='latin-1')
    ycom_meta = pd.read_csv('../data/YCOM_2018_Metadata.csv', encoding='latin-1')
    # Get county level data matching census county names
    ycom_county = prepare_data.get_ycom_counties(ycom)
    # Removing counties not in land area data
    ycom_county = prepare_data.remove_not_in_land_area(ycom_county)
    return ycom_county

def check_within_range(df, x, y):
    """
    Helper function to check if all values in a dataframe
     are within given range (values inclusive)  x lower bound, y upperbound
    """
    out_of_range = 0
    for col in df.columns:
     within_range = df[col].between(x, y,inclusive=True).count()
     if within_range != len(df[col]):
        out_of_range += 1
    if out_of_range == 0:
        return True
    else:
        return False


class UnitTests(unittest.TestCase): 


    def test_calculate_stats_outputs_standard(self):
        """
        Tests for calculate_stats_outputs_standard to check that
        output dataframe is of correct dimensions.
        """
        census = prep_census_data()
        # Getting list of census variables
        n_census = list(census)[3:]
        ycom_county = prep_ycom_data()
        # Getting list of YCOM variables
        n_ycom = list(ycom_county)[3:-2]
        stats_outputs_standard = calculate_statistics.calculate_stats_outputs_standard(n_ycom, 
                                                                                       n_census, 
                                                                                       ycom_county, 
                                                                                       census)
        self.assertEqual =(stats_outputs_standard.shape ,(len(n_ycom), len(n_census), 5))


    def test_calculate_stats_outputs(self):
                """
        Tests for calculate_stats_outputs to check that
        output dataframe is of correct dimensions.
        """

        census = prep_census_data()
        # Getting list of census variables
        n_census = list(census)[3:]
        ycom_county = prep_ycom_data()
        # Getting list of YCOM variables
        n_ycom = list(ycom_county)[3:-2]
        stats_outputs = calculate_statistics.calculate_stats_outputs(n_ycom, n_census, 
                                                                     ycom_county, census)
        self.assertEqual =(stats_outputs.shape ,(len(n_ycom), len(n_census), 5))

    def test_get_cors_df(self):
        """
        test function for test_get_cors_df to make sure results
        are within expected range(between -1 and 1)
        """
        census = prep_census_data()
        # Getting list of census variables
        n_census = list(census)[3:]
        ycom_county = prep_ycom_data()
        # Getting list of YCOM variables
        n_ycom = list(ycom_county)[3:-2]
        stats_outputs = calculate_statistics.calculate_stats_outputs(n_ycom, n_census, 
                                                                     ycom_county, census)
        cors = calculate_statistics.get_cors_df(stats_outputs, n_census, n_ycom)

        return check_within_range(cors, -1, 1)



    def test_get_pvalues_df(self):
                """
        test function for test_get_pvalues_df to make sure results
        are within expected range(between 0 and 1)
        """
        census = prep_census_data()
        # Getting list of census variables
        n_census = list(census)[3:]
        ycom_county = prep_ycom_data()
        # Getting list of YCOM variables
        n_ycom = list(ycom_county)[3:-2]
        stats_outputs = calculate_statistics.calculate_stats_outputs(n_ycom, n_census, 
                                                                     ycom_county, census)
        pvalues = calculate_statistics.get_pvalues_df(stats_outputs, n_census, n_ycom)

        return check_within_range(pvalues, 0, 1)





if __name__ == '__main__':
    unittest.main()