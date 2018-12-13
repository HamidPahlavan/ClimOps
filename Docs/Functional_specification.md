# Climate Opinions (ClimOps)
Team: Robin Clancy, Rebeca de Buen, Hamid Pahlavan and Yakelyn R. Jauregui
>Course project for CSE 583 - Software Engineering for Data Scientists

Funtional Specification
=======================

1. Background:
This project will create a data set that allows researchers to explore whether a relationship exists between beliefs about climate change, demographic characteristics and transportation behaviors in the United States.

The final product would allow the user to explore (through basic statistics and visualizations) questions such as:
- Do race, ethnicity, socioeconomic status (education and income), and gender is related to climate change perceptions?
- Do people’s beliefs about climate change have a relationship with their transportation behavior (for example, do people who believe that climate change is happening and caused by humans drive less/ use more public transit/ carpool?

User profile
============
General public. But specially useful for academic researchers or policy makers. This product will allow them to explore relationships about climate beliefs and demographic data in a easy and efficient way. Users not familiar with python or bash should be able to view the product.   

Data sources
============
This project combines the following data sets:
 - The 2018 Yale Climate Opinions Map Data:
	Measures of public opinion about different aspects of global warming. This data is structured as​ % ‘Yes’ responses to each question in the survey ​at state, congressional district, and county levels.
>   Source: http://climatecommunication.yale.edu/visualizations-data/ycom-us-2018/?est=happening&type=value&geo=county
 - The 2015 United States Census:
	Provides information on a wide range of social, economic, demographic, and housing characteristics. Topics covered include income, employment, health insurance, the age distribution, and education, among many others. The data is organized by states as well as counties.
>   Source:https://www.census.gov/
 - Land area data:
        Closely associated with the 2015 Census data. Including this allows for population density to be calculated.

Use Cases
=========

1. Reveal statistical relationships between all climate opinions and demographic variables
	- What information does user provide?
		- Select which statistical parameter is to be viewed

	- What responses does the system provide?
		- Heat map of correlation/regression/significance values

2. Reveal relationship between a specific climate opinion and demographic
variable (chosen by the user)
	- What information does user provide?
		- Select opinion of interest and demographic variable of interest from dropdown boxes.

	- What responses does the system provide?
		- Scatter plot of these variables

