# Health Data Dashboard + Statistical Analysis

## Overview
This project is a comprehensive health data dashboard built using Streamlit and Plotly. It allows users to visualize various healthcare metrics, including patient demographics, billing amounts, and medical conditions. The dashboard also includes statistical analysis to identify significant relationships between different variables in the dataset.

## Features
- **Dynamic Data Visualization**: Interactive charts and graphs to explore patient data by year, gender, age group, medical condition, and more.
- **Statistical Analysis**: Includes chi-square tests, ANOVA, and Kruskal-Wallis tests to assess relationships and differences in the dataset.
- **User-Friendly Interface**: Easy-to-navigate dashboard layout for improved user experience.

## Technologies Used
- [Python](https://www.python.org/)
- [Streamlit](https://streamlit.io/)
- [Plotly](https://plotly.com/python/)
- [Pandas](https://pandas.pydata.org/)
- [Scipy](https://www.scipy.org/)
- [Matplotlib](https://matplotlib.org/)
- [Seaborn](https://seaborn.pydata.org/)

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/health-data-dashboard.git
   cd health-data-dashboard
Data Description

### The dataset used in this project includes the following columns:

Name: Name of the patient.
Date of Admission: Date the patient was admitted.
Gender: Gender of the patient.
Age: Age of the patient.
Medical Condition: The medical condition diagnosed.
Admission Type: Type of admission (e.g., emergency, elective).
Billing Amount: Total billing amount for the patient.
Hospital: The hospital where the patient was treated.
Insurance Provider: The insurance provider for the patient.

## Statistical Analysis

Chi-Square Test: Analyzed the relationship between Gender and Admission Type.
ANOVA: Assessed differences in billing amounts across different hospitals.
Kruskal-Wallis H Test: Evaluated age distributions among various medical conditions when normality assumptions were violated.

## Acknowledgments

Thanks to the contributors and resources available for Streamlit, Plotly, and other libraries used in this project.
