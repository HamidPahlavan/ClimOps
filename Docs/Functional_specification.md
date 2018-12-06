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
General public. But specially useful for academic researchers or policy makers. This product will allow them to explore relationships about climate beliefs and demographic data in a easy and efficient way.   

Data sources
============
This project combines the following data sets:
 - The 2018 Yale Climate Opinions Map Data:
	Measures of public opinion about different aspects of global warming. This data is structured as​ % ‘Yes’ responses to each question in the survey ​at state, congressional district, and county levels.
>   Source: http://climatecommunication.yale.edu/visualizations-data/ycom-us-2018/?est=happening&type=value&geo=county
 - The 2015 United States Census:
	Provides information on a wide range of social, economic, demographic, and housing characteristics. Topics covered include income, employment, health insurance, the age distribution, and education, among many others. The data is organized by states as well as counties.
>   Source:https://www.census.gov/

Use Cases
=========

1. Reveal relationship between a specific climate opinion and demographic
variable (choose by the user)
	- What information does user provide?
		- Select opinion of interest and demographic variable of interest from dropdown boxes ideally.
		- Perhaps some options for how the analysis is done (e.g. control for certain variables?)

	- What responses does the system provide?
		- Some correlation/regression/significance values
		- Maps of correlation/regression/significance where analysis is
performed individually for each state.



