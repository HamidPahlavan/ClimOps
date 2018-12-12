"""
This module is used to create a heatmap of the correlation coefficients
between YCOM and census data, as well as a scatter plot which allows for
each relationship to be visualized in greater detail.
"""
from bokeh.models import BasicTicker, ColorBar, ColumnDataSource, CustomJS, LinearColorMapper
from bokeh.models.widgets import Select
from bokeh.plotting import figure
from bokeh.transform import transform

import bokeh.palettes
import numpy as np
import pandas as pd


def stack_stats(cors, regs, pval):
    """
    Prepare dataframe in the right shape for heatmap plotting.
    i.e. kinda vectorizes correlation coefficients and p values.
    then combines them into a single dataframe.
    inputs: cors, regs, pval
    output: combined stacked data (all_stack)
    """
    YCOM_LABEL = 'ycom'
    CENSUS_LABEL = 'census'
    
    cors.index.name = YCOM_LABEL 
    cors.columns.name = CENSUS_LABEL
    regs.index.name = YCOM_LABEL 
    regs.columns.name = CENSUS_LABEL
    pval.index.name = YCOM_LABEL 
    pval.columns.name = CENSUS_LABEL

    cors_stack = cors.stack().rename("R").reset_index()
    regs_stack = regs.stack().rename("b").reset_index()
    regs_stack.columns = [YCOM_LABEL , CENSUS_LABEL, 'b']
    pval_stack = pval.stack().rename("value").reset_index()
    pval_stack.columns = [YCOM_LABEL , CENSUS_LABEL, 'pval']
    all_stack = pd.concat([cors_stack, pval_stack['pval'], regs_stack['b']], axis=1)
    return all_stack


def get_varnames(dframe, datasource):
    """
    Getting YCOM and census variable names for hover over feature.
    inputs:
        datasource: string, either 'census' or 'ycom'
        dframe: stacked dataframe, i.e. all_stack
    output:
        nameseries: series of variable names
    """
    nameseries = list(dframe.loc[:][datasource].drop_duplicates())
    return nameseries


def create_heatmap_fig(dframe, vartype):
    """
    Generates heatmap of chosen statistic (R, b, pval).
    inputs:
        dframe: stacked dataframe, i.e. all_stack
        vartype: string, either 'R', 'b', 'pval'
            R = correlation coefficient
            b = regression coefficient
            p = p value
    output:
        heatmap_plot: figure
    """
    YCOM_LABEL = 'ycom'
    CENSUS_LABEL = 'census'
    
    # Getting census and ycom variable names for hover over feature
    census_vars = get_varnames(dframe, CENSUS_LABEL)
    ycom_vars = get_varnames(dframe, YCOM_LABEL)

    # Define a figure
    heatmap_plot = figure(
        plot_width=600,
        plot_height=400,
        title="",
        x_range=ycom_vars,
        y_range=census_vars,
        toolbar_location=None,
        tools="",
        x_axis_location="below",
        tooltips=[('Census', '@ycom'), ('YCOM', '@census'),
                  ('R', '@R'), ('b', '@b'), ('p', '@pval')])

    heatmap_plot.axis.major_label_text_font_size = "5pt"
    heatmap_plot.xaxis.major_label_orientation = 1.2

    # Assigning color scale
    if vartype == 'R':
        colors = bokeh.palettes.RdBu11
        mapper = LinearColorMapper(palette=colors, low=-1, high=1)
    elif vartype == 'b':
        colors = bokeh.palettes.RdBu11
        mapper = LinearColorMapper(palette=colors, low=-0.3, high=0.3)
    elif vartype == 'pval':
        colors = bokeh.palettes.RdBu11
        mapper = LinearColorMapper(palette=colors, low=0, high=1)

    # Create rectangle for heatmap
    heatmap_plot.rect(
        x=YCOM_LABEL,
        y=CENSUS_LABEL,
        width=1,
        height=1,
        source=ColumnDataSource(dframe),
        line_color=None,
        fill_color=transform(vartype, mapper))

    # Add legend
    color_bar = ColorBar(
        color_mapper=mapper,
        location=(0, 0),
        ticker=BasicTicker(desired_num_ticks=np.int(len(colors))))

    heatmap_plot.add_layout(color_bar, 'right')
    return heatmap_plot


def set_callback_census(source, xaxis):
    """
    Creates javascript callback allowing for scatter plot to automatically update
    when different census variables are selected
    """
    callback_census = CustomJS(args=dict(source=source, xaxis=xaxis), code="""
        // cb_obj is the callback object
        // cb_obj.value is the selected value.
        
        // create a new variable for the data of the column data source
        // this is linked to the plot
        var data = source.data;

        // allocate the selected column to the field for the x values
        data['x'] = data[cb_obj.value];

        // register the change - this is required to process the change in the x values
        source.change.emit();
        
        //update the x axis label
        xaxis.attributes.axis_label = cb_obj.value;
        xaxis.change.emit();
    """)
    return callback_census


def set_callback_ycom(source, yaxis, source_ycom_meta):
    """
    Creates javascript callback allowing for scatter plot to automatically update
    when different ycom variables are selected
    """
    callback_ycom = CustomJS(
        args=dict(source=source, yaxis=yaxis, source_ycom_meta=source_ycom_meta), code="""
        var data = source.data;
        var ycom_var_names = source_ycom_meta.data['YCOM VARIABLE NAME'];
        var ycom_var_descriptions = source_ycom_meta.data['VARIABLE DESCRIPTION'];
        var dropdown_description = cb_obj.value;
        var dropdown_name = cb_obj.value;
            
        //update the y axis label
        for (var i=0; i<ycom_var_descriptions.length; i++){
            if (ycom_var_descriptions[i] == dropdown_description)
            dropdown_name = ycom_var_names[i];
            yaxis.attributes.axis_label = dropdown_name + ' %';
            }
        yaxis.change.emit();
        
        // update y data
        data['y'] = data[dropdown_name];
        // register the change - this is required to process the change in the y values
        source.change.emit();
    """)
    return callback_ycom


def create_dropdown_census(n_census, callback_census):
    """
    Setting up dropdown menu for census and associating the callback to autoupdate
    inputs:
        n_census: list of dropdown options based on variable names
        callback_census: custom javascript describing callback behaviour
    """
    census_menu = Select(options=n_census, value='v', title='Census Variables')
    census_menu.callback = callback_census
    return census_menu


def create_dropdown_ycom(n_ycom_meta, callback_ycom):
    """
    Setting up dropdown menu for census and associating the callback to autoupdate
    inputs:
        n_ycom_meta: list of dropdown options based on ycom variable descriptions from metadata
        callback_ycom: custom javascript describing callback behaviour
    """
    ycom_menu = Select(options=n_ycom_meta, value='v', title='YCOM Variables')
    ycom_menu.callback = callback_ycom
    return ycom_menu
