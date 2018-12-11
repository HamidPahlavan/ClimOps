## This script includes unit tests for the module prepare_data.py
import unittest

import numpy as np
import pandas as pd

import prepare_data

class UnitTests(unittest.TestCase):

    def test_scale_census_variables(self):
        """
        Test function for scale_census_variables
        """
        census = pd.read_csv('../data/acs2015_county_data.csv')
        census_scaled = prepare_data.scale_census_variables(census)
        # Scaled variables are percenages so all values should
        # fall between 0 and 1. This test checks for correct
        # range of values for these columns.
        s_men = census_scaled.Men
        self.assertTrue(s_men.between(0, 1).count() == len(s_men))
        s_women = census_scaled.Women
        self.assertTrue(s_women.between(0, 1).count() == len(s_women))
        s_cit = census_scaled.Citizen
        self.assertTrue(s_cit.between(0, 1).count() == len(s_cit))
        s_emp = census_scaled.Employed
        self.assertTrue(s_emp.between(0, 1).count() == len(s_emp))


    def test_remove_census_not_in_ycom(self):
        """
        Test for function to remove data for Puerto Rico from census,
        which is not included in YCOM data.
        Input: dataframe of census data
        Output: dataframe of census data with Puerto
        Rico removed.
        """
        census = pd.read_csv('../data/acs2015_county_data.csv')
        census_remove_pr = prepare_data.remove_census_not_in_ycom(census)
        #check to se whether remaining dataset includes PR (remaining obs
        # should be 0).
        test_set = census_remove_pr[census_remove_pr['State'] == 'Puerto Rico']
        pr_obs = test_set.shape
        self.assertTrue(pr_obs[0] == 0)


    def test_select_geography(self):
        """
        test function for select_gegraphy
        Ensures filtering is done corectly
        """
        ycom = pd.read_csv('../data/YCOM_2018_Data.csv', encoding='latin-1')
        ycom_county = prepare_data.select_geography(ycom, 'County')
        self.assertTrue(ycom_county.GeoType.unique() == ['County'])
        ycom_state = prepare_data.select_geography(ycom, 'State')
        self.assertTrue(ycom_state.GeoType.unique() == ['State'])
        self.assertFalse(ycom_state.GeoType.unique() == ['County'])


    def test_fix_ycom_county_names(self):
        """
        test function for fix_ycom_county_names. Makes
        sure that renaming counties creates correct
        dataframe and we have the epected number of States and Counties
        once names are parsed.
        """
        ycom = pd.read_csv('../data/YCOM_2018_Data.csv', encoding='latin-1')
        ycom_county = prepare_data.select_geography(ycom, 'County')
        ycom_county_fixed = prepare_data.fix_ycom_county_names(ycom_county)
        self.assertEqual(len(ycom_county.columns), len(ycom_county_fixed.columns))
        # states should have 50 states + DC
        self.assertTrue(len(ycom_county['State'].unique()) == 51)
        # should
        self.assertTrue(len(ycom_county['County']) == 3142)

    def test_get_ycom_counties(self):
        """
        test function for get_ycom_counties.
        Makes sure correct number of states and counties are present.
        Makes sure only county level data is within ycom_county
        """
        ycom = pd.read_csv('../data/YCOM_2018_Data.csv', encoding='latin-1')
        ycom_county = prepare_data.get_ycom_counties(ycom)
        self.assertTrue(len(ycom_county['State'].unique()) == 51)
        self.assertTrue(len(ycom_county['County']) == 3142)
        self.assertTrue(ycom_county.GeoType.unique() == ['County'])


    def test_join_data(self):
        """
        Ensure counties are the same between datasets for join.
        """
        ycom = pd.read_csv('../data/YCOM_2018_Data.csv', encoding='latin-1')
        ycom = prepare_data.fix_ycom_county_names(ycom)
        ycom_county = prepare_data.get_ycom_counties(ycom)
        census = pd.read_csv('../data/acs2015_county_data.csv')
        census = prepare_data.remove_census_not_in_ycom(census)
        self.assertTrue(np.all(ycom_county['County'] == census['County']))
        #data = prepare_data.join_data(ycom_county, census)
        #self.assertTrue(data.shape ==(3142, (len(ycom_county.columns) +
                                    #len(census_county.columns))))


if __name__ == '__main__':
    unittest.main()
