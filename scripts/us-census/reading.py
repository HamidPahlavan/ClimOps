# import packages

import numpy as np
import pandas as pd
import ggplot
import matplotlib.pyplot as plt
import seaborn as sns
%matplotlib inline

# load dataset
df = pd.read_csv('../us-census-demographic-data/acs2015_county_data.csv')
df.head()

list(df)

