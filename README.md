# Climate Opinions (ClimOps)

<img src="https://github.com/HamidPahlavan/project/blob/master/images/logo.png" alt="logo" width="400" height="200" />

>source:https://www.mediamatters.org/blog

Team: Robin Clancy, Rebeca de Buen, Hamid Pahlavan and Yakelyn R. Jauregui
>Course project for CSE 583 - Software Engineering for Data Scientists



Project description
===================
This project will create a data set that allows researchers to explore whether there is a correlation between beliefs about climate change, 
and demographic characteristics and transportation behaviors reported in the United States Census.
The final product would allow the user to explore (through basic statistics and visualizations) questions such as:
  - Are race, ethnicity, socioeconomic status (education and income), and gender correlated with climate change perceptions?
  - Do people’s beliefs about climate change have a correlation with their transportation behavior 
  (for example, do people who believe that climate change is happening and caused by humans drive less/ own less cars/ use more public transit/ bike more)?.
The goal is to create an easy way to visualize potential relationships between these data sets to see if any of these may worth exploring further.

Sources of data
===========================
This project combines the following data sets:
 - The 2018 Yale Climate Opinions Map Data
 - The 2015 United States Census 

Organization of the Project
===========================
The project has the following structure:
```
├── ClimOps
   ├── climops
   │   ├── calculate_statistics.py
   │   ├── plot_heatmap.py
   │   ├── prepare_data.py
   │   ├── heatmap.html
   │   ├── scatter.html
   │   ├── tests
   │   │   ├── __init__.py
   │   │   └── test_clean_data.py
   │   └── version.py
   ├── data
   │   ├── LND01.xls
   │   ├── YCOM_2018_Data.csv
   │   ├── YCOM_2018_Metadata.csv
   │   └── acs2015_county_data.csv
   ├── Docs
   │   ├── Component_specification.md
   │   ├── Functional_specification.md
   │   └── climops.html
   ├── images
   │   └── logo.png
   ├── LICENSE
   ├── README.md
   ├── requirements.txt
   ├── environment.yml
   └── setup.py

```

Installation
============

First, get ClimOps on your own computer by using the following git command:

```
git clone https://github.com/HamidPahlavan/climops.git
```

Next, to install the package you will need to go into the climops directory and run the setup.py file:
```
pip install -r requirements.txt 
```




