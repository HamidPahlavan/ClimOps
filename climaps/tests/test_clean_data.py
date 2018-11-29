## This script includes unit tests for the module clean_data.py
import unittest
from clean_data import *

class UnitTests(unittest.TestCase):

    def test_select_geography(self):
        ycom = get_data('YCOM_2018_Data.csv')
        ycom_county = select_geography(ycom, 'County')
        self.assertTrue(ycom_county.GeoType.unique() == ['County'])

        ycom_state = select_geography(ycom, 'State')
        self.assertTrue(ycom_state.GeoType.unique() == ['State'])

        self.assertFalse(ycom_state.GeoType.unique() == ['County'])

    def test_fix_ycom_county_names(self):
        ycom = get_data('YCOM_2018_Data.csv')
        ycom_county = select_geography(ycom, 'County')
        ycom_county_fixed = fix_ycom_county_names(ycom_county)
        #self.assertTrue(cols.extend(['State', 'County']), cols_fixed))

        self.assertEqual(len(ycom_county.columns), len(ycom_county_fixed.columns))
        # states should have 50 states + DC
        self.assertTrue(len(ycom_county['State'].unique())== 51)

        self.assertTrue(len(ycom_county['County']) == 3142)

    def test_get_ycom_counties(self):
        ycom = get_data('YCOM_2018_Data.csv')
        ycom_county = get_ycom_counties(ycom)
        self.assertTrue(len(ycom_county['State'].unique())== 51)
        self.assertTrue(len(ycom_county['County']) == 3142)
        self.assertTrue(ycom_county.GeoType.unique() == ['County'])

    def test_get_census_data(self):
        census = get_data('us-census-demographic-data/acs2015_county_data.csv')
        census_county = get_census_counties(census)
        self.assertTrue(len(census_county['County']) == 3142)
        self.assertTrue(len(census_county['State'].unique())== 51)

    def test_join_data(self):
        ycom = get_data('YCOM_2018_Data.csv')
        ycom_county = get_ycom_counties(ycom)
        census = get_data('us-census-demographic-data/acs2015_county_data.csv')
        census_county = get_census_counties(census)
        self.assertTrue(np.all(ycom_county['County'] == census_county['County']))
        data = join_data(ycom_county, census_county)
        self.assertTrue(data.shape ==(3142, (len(ycom_county.columns) +
                                    len(census_county.columns))))


if __name__ == '__main__':
    unittest.main()
