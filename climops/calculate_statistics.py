"""
This module is used to generate correlation (R) and regression (b)
coefficients for relationships between the 2015 Census,
2018 Yale Climate Opinion Maps (YCOM) and land area datasets,
as well as p values for these relationships.
"""

import numpy as np
import pandas as pd
from scipy.stats import linregress

def calculate_stats_outputs(n_ycom, n_census, ycom_county, census):
    """
    Function to estimate regression coefficients correlation between YCOM data variables and US
    Census variables.
    Inputs: n_ycom, a full list of names for ycom variables,
            n_census, a full list of names for census variables
    Outputs: a matrix of correlation values between each variable each dataset
    """
    stats_outputs = np.zeros((len(n_ycom), len(n_census), 5))

    for yind, yvar in enumerate(n_ycom):
        for cind, cvar in enumerate(n_census):
            ycom_notnull = ycom_county[yvar][census[cvar].notnull()]
            census_notnull = census[cvar][census[cvar].notnull()]
            stats_outputs[yind, cind, 0:5] = linregress(ycom_notnull, census_notnull)
    return stats_outputs


def calculate_stats_outputs_standard(n_ycom, n_census, ycom_county, census):
    """
    Function to estimate regression coefficients between YCOM data variables and US
    Census variables on standardized variables
    standardized_column = (column - mean(column)) / std(column)
    Inputs: n_ycom, a full list of names for ycom variables,
            n_census, a full list of names for census variables
    Outputs: a matrix of correlation values between each variable each dataset
    """
    stats_outputs_standard = np.zeros((len(n_ycom), len(n_census), 5))
    for yind, yvar in enumerate(n_ycom):
        for cind, cvar in enumerate(n_census):
            ycom_notnull = ycom_county[yvar][census[cvar].notnull()]
            census_notnull = census[cvar][census[cvar].notnull()]

            #also doing calculations on standardized variables
            census_standard = (census_notnull - np.mean(census_notnull)) / np.std(census_notnull)
            stats_outputs_standard[yind, cind, 0:5] = linregress(ycom_notnull, census_standard)
    return stats_outputs_standard


def get_regs_df(stats_outputs_standard, n_census, n_ycom):
    """
    making dataframe of regression coefficients
    these are kinda standardized -they show what % change in an opinion is given
    a 1 standard deviation change in a census variable
    """
    regs = pd.DataFrame(stats_outputs_standard[:, :, 0], columns=n_census, index=n_ycom)
    return regs


def get_cors_df(stats_outputs, n_census, n_ycom):
    """
    making dataframe of correlation coefficients
    """
    cors = pd.DataFrame(stats_outputs[:, :, 2], columns=n_census, index=n_ycom)
    return cors


def get_pvalues_df(stats_outputs, n_census, n_ycom):
    """
    making dataframes of pvalues
    """
    pval = pd.DataFrame(stats_outputs[:, :, 3], columns=n_census, index=n_ycom)
    return pval
