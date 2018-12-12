"""
This script serves as the primary means for creating
heatmap and scatter plot outputs from the YCOM and census
data. Running this script loads and prepares the raw data,
performs regression calculations, plots the results and
saves these plots.

Creates output files:
    "heatmap.html"
    "scatter.html"

Example:
    To run use:
        $ python create_heatmap.py
"""

# Third party imports
from bokeh.io import output_file, show
from bokeh.layouts import column
from bokeh.models.widgets import Panel, Tabs
from bokeh.models import ColumnDataSource, LinearAxis
from bokeh.plotting import figure, save
import pandas as pd

# Local imports
import calculate_statistics
import plot_heatmap
import prepare_data

output_file("heatmap.html")

# Preparing census data
# Loading census data
CENSUS = pd.read_csv('../climops/data/acs2015_county_data.csv')
# Scaling Men, Women, Employed and Citizen by TotalPop to get a percentage
CENSUS = prepare_data.scale_census_variables(CENSUS)
# Removing counties not in ycom data (i.e. puerto rico)
CENSUS = prepare_data.remove_census_not_in_ycom(CENSUS)
# Removing counties not in land area data
CENSUS = prepare_data.remove_not_in_land_area(CENSUS)
# Getting list of census variables
N_CENSUS = list(CENSUS)[3:]

# Preparing YCOM data
# Loading ycom data
YCOM = pd.read_csv('../climops/data/YCOM_2018_Data.csv', encoding='latin-1')
YCOM_META = pd.read_csv('../climops/data/YCOM_2018_Metadata.csv', encoding='latin-1')
# Get county level data matching census county names
YCOM_COUNTY = prepare_data.get_ycom_counties(YCOM)
# Removing counties not in land area data
YCOM_COUNTY = prepare_data.remove_not_in_land_area(YCOM_COUNTY)
# Getting list of YCOM variables
N_YCOM = list(YCOM_COUNTY)[3:-2]
# Editing and getting list of YCOM variable descriptions
YCOM_META = prepare_data.fix_ycom_descriptions(YCOM_META)
N_YCOM_META = list(YCOM_META['VARIABLE DESCRIPTION'])[3:]

# Preparing land area data
# Loading land_area_data
LAND_AREA_DATA = pd.read_excel('../climops/data/LND01.xls')
# Selecting only counties
LAND_AREA_DATA = prepare_data.select_land_area_county(LAND_AREA_DATA)
# Removing rows which are in land area but not census
LAND_AREA_DATA = prepare_data.remove_land_area_not_in_census(LAND_AREA_DATA)
# Fixing land area data county names so that they match those in census data
LAND_AREA_DATA = prepare_data.fix_land_area_county_names(LAND_AREA_DATA, CENSUS)
# Adding land area values where missing
LAND_AREA_DATA = prepare_data.add_missing_land_areas(LAND_AREA_DATA)

# Getting one dataframe from the three datasets
N_CENSUS.append('LogPopDensity')
COMBINED_DATA = prepare_data.join_data(YCOM_COUNTY, CENSUS, LAND_AREA_DATA)

# Generate correlation (R), regression (b) and pvalues for relationships between variables
STATS_OUTPUTS = calculate_statistics.calculate_stats_outputs(N_YCOM, N_CENSUS, YCOM_COUNTY, CENSUS)
STATS_OUTPUTS_STANDARD = calculate_statistics.calculate_stats_outputs_standard(
    N_YCOM, N_CENSUS, YCOM_COUNTY, CENSUS)

# Making dataframe of regression coefficients
REGS = pd.DataFrame(STATS_OUTPUTS_STANDARD[:, :, 0], columns=N_CENSUS, index=N_YCOM)
#making dataframe of correlation coefficients
CORS = pd.DataFrame(STATS_OUTPUTS[:, :, 2], columns=N_CENSUS, index=N_YCOM)
#making dataframes of pvalues
PVAL = pd.DataFrame(STATS_OUTPUTS[:, :, 3], columns=N_CENSUS, index=N_YCOM)

# Prepare dataframe in the right format for heatmap
ALL_STACK = plot_heatmap.stack_stats(CORS, REGS, PVAL)

# Create and plot heatmap of either
# 'R' (correlation), 'b' (regression) or 'pval' (p value) statistics
HEATMAP_PLOT_R = plot_heatmap.create_heatmap_fig(ALL_STACK, 'R')
TAB1 = Panel(child=HEATMAP_PLOT_R, title='Correlation')
HEATMAP_PLOT_B = plot_heatmap.create_heatmap_fig(ALL_STACK, 'b')
TAB2 = Panel(child=HEATMAP_PLOT_B, title='Regression')
HEATMAP_PLOT_P = plot_heatmap.create_heatmap_fig(ALL_STACK, 'pval')
TAB3 = Panel(child=HEATMAP_PLOT_P, title='p value')
TABS = Tabs(tabs=[TAB1, TAB2, TAB3])
show(TABS)
save(obj=TABS, filename='heatmap.html')

# Interactive scatter plots
output_file("scatter.html")
# Creating extra columns which are going to be filled with whatever data is chosen from dropdown
COMBINED_DATA['x'] = 99
COMBINED_DATA['y'] = 99
# Setting sources for scatter plots
# (Taking every other data point because otherwise too much memory is used)
SOURCE = ColumnDataSource(COMBINED_DATA[1::2])
SOURCE_YCOM_META = ColumnDataSource(YCOM_META)
# Generating scatter plot
SCATTER_PLOT = figure(plot_width=350, plot_height=350)
SCATTER_PLOT.scatter('x', 'y', source=SOURCE)
# Adding some axes that can have their labels dynamically updated
SCATTER_PLOT.xaxis.visible = None
SCATTER_PLOT.yaxis.visible = None
XAXIS = LinearAxis(axis_label="Census Variable")
YAXIS = LinearAxis(axis_label="YCOM Variable")
SCATTER_PLOT.add_layout(XAXIS, 'below')
SCATTER_PLOT.add_layout(YAXIS, 'left')
# Creating javascript callbacks allowing for scatter plot to automatically update
CALLBACK_CENSUS = plot_heatmap.set_callback_census(SOURCE, XAXIS)
CALLBACK_YCOM = plot_heatmap.set_callback_ycom(SOURCE, YAXIS, SOURCE_YCOM_META)
# Setting up dropdowns
CENSUS_MENU = plot_heatmap.create_dropdown_census(N_CENSUS, CALLBACK_CENSUS)
YCOM_MENU = plot_heatmap.create_dropdown_ycom(N_YCOM_META, CALLBACK_YCOM)
# Plotting scatter
LAYOUT_SCATTER = column(CENSUS_MENU, YCOM_MENU, SCATTER_PLOT)
show(LAYOUT_SCATTER)
save(obj=LAYOUT_SCATTER, filename='scatter.html')
