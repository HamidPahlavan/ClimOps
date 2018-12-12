# Climate Opinions (ClimOps)
Team: Robin Clancy, Rebeca de Buen, Hamid Pahlavan and Yakelyn R. Jauregui
>Course project for CSE 583 - Software Engineering for Data Scientists

Component Specification
=======================

### 1. Software Components:
**Data cleaning and merging** (clean_data.py): A module for cleaning and merging the data at the county level using pandas. This component has functions that prepare each data set to have matching counties and county names, and that facilitate the merge process. 
* *Inputs:* The raw data from the 2015 Census, Census Land Area Data, and 2018 Yale Climate Opinions Data.
* *Output:* A dataframe of the raw data merged at the county level.

**Estimate statistics** (calculate_statistics.py): A module that estimates correlations, pvalues and bivariate regression coefficients between all of the variables in the data set using scipy and outputs them into a dataframe that can be used in the visualization module.
* *Inputs:* A dataframe of the raw data merged at the county level.
* *Output:* A dataframe of pvalues, correlations and regression coefficients.

**Visualization** (plot_heatmap.py): A module that creates interactive heatmaps and scatterplots using bokeh from the dataframe created on the statistics 
* *Inputs:* A dataframe of pvalues, correlations and regression coefficients
* *Output:* Interactive html scatter plots and and heatmaps for each statistical metric. 

### 2. Interactions to accomplish use cases.
The interaction between components is summarized in the following diagram:
<img src="https://github.com/HamidPahlavan/project/blob/master/images/components.png" alt="logo" width="400" height="200" />


Two potential uses for this tool are:
- Visualize statistical relationships between climate opinions and demographic variables
- Visualize statistical relationships between climate opinions and reported transportation habits (for example)Drive, Carpool, Transit, Walk

For both use cases, the user can 
- Download the tool and use the provided interactive vizualizations
- use the link to the repo to view and explore plots.

```
