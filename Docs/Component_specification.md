# Climate Opinions (ClimOps)
Team: Robin Clancy, Rebeca de Buen, Hamid Pahlavan and Yakelyn R. Jauregui
>Course project for CSE 583 - Software Engineering for Data Scientists

Funtional Specification
=======================

1. Background:
This project will create a data set that allows researchers to explore whether a relationship exists between beliefs about climate change, demographic characteristics and transportation behaviors (for example walking, cycling, driving behaviors, use of transit types and number of cars owned) in the United States.

The final product would allow the user to explore (through basic statistics and visualizations) questions such as:
- Do race, ethnicity, socioeconomic status (education and income), and gender is related to climate change perceptions?
- Do people’s beliefs about climate change have a relationship with their transportation behavior (for example, do people who believe that climate change is happening and caused by humans drive less/ own less cars/ use more public transit/ bike more?
- How public opinion about global warming changed relative to 2014 and we want to see if this change is related to other data ( e.g., census)

User profile
============
General public. But specially useful for academic researchers or policy makers; this product will allow them to explore relationships about climate beliefs and demographic data in a easy  


Sources of data
===========================
This project combines the following data sets:
 - The 2018 Yale Climate Opinions Map Data
 - The 2015 United States Census 

Organization of the Project
===========================
The project has the following structure:
```
climaps/
├── LICENSE
├── README.md
├── climaps
│   ├── __init__.py
│   ├── clean_data.py
│   ├── tests
│   │   ├── __init__.py
│   │   └── test_clean_data.py
│   └── version.py
├── data
│   ├── YCOM_2018_Data.csv
│   ├── acs2015_census_tract_data.csv
│   └── acs2015_county_data.csv
├── Docs
│   ├── Component specification.pdf
│   ├── Functional specification.pdf
│   └── final_presentation.pdf
├── examples
│   └── README.md
├── images
│   └── logo.png
├── requirements.txt
├── environment.yml
├── setup.py
└── issues
```
