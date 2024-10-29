# %% [markdown]
# # Health Data Dashboard + Statistical Analysis

# %%
# Import Library
import streamlit as st
import plotly.express as px
import pandas as pd
## import scipy.stats as stats
import matplotlib.pyplot as plt
import seaborn as sns
import os
import warnings
warnings.filterwarnings('ignore')

# %%
# Setting the title
st.set_page_config(page_title="Healthcare Data",  page_icon=":bar_chart", layout="wide")
st.title(":bar_chart: Healthcare Data Dashboard")
st.markdown('<style>div.block-container{padding-top:2rem;}</style>', unsafe_allow_html=True)

# %% [markdown]
# ### Load Data

# %%
# Load the csv file
file_path = "healthcare_dataset.csv"
df = pd.read_csv(file_path)

# %% [markdown]
# ### Data Cleaning

# %%

# Convert 'Date of Admission' to datetime
df['Date of Admission'] = pd.to_datetime(df['Date of Admission'], errors='coerce')

# Check for NaT values in 'Date of Admission' after conversion
nat_count = df['Date of Admission'].isna().sum()
if nat_count > 0:
    st.warning(f"There are {nat_count} invalid date entries in 'Date of Admission'.")

# Clean the DataFrame (remove rows where Name is NaN)
df_clean = df[df['Name'].notna()]

df_clean

# %% [markdown]
# ### Filter by Year

# %%
# Getting the unique years for the dropdown
df_clean['Year'] = df_clean['Date of Admission'].dt.year  # Extract the year
years = df_clean['Year'].unique()  # Get unique years
years.sort()  # Sort the years

# Include an "All Years" option
all_years_option = "All Years"
year_options = [all_years_option] + years.tolist()  # Add "All Years" to the list

# Create a dropdown to select a year
selected_year = st.selectbox("Select Year", year_options)

# Filter the DataFrame based on the selected year
if selected_year == all_years_option:
    df_clean_filtered = df_clean.copy()  # No filtering, show all data
else:
    df_clean_filtered = df_clean[df_clean['Year'] == int(selected_year)].copy()

# Display the filtered DataFrame
st.write(f"Filtered Data for Year: {selected_year}", df_clean_filtered)

# %% [markdown]
# ### Second Row

# %%
# Add total number of Patient, Doctor, Hospital, Billing amount and Insurance Provider
st.header('Patient Overview')
total_patients = df_clean_filtered['Name'].nunique()
total_bill = df_clean_filtered['Billing Amount'].sum()
total_hospital = df_clean_filtered['Hospital'].nunique()
total_doctor = df_clean_filtered['Doctor'].nunique()
total_insurance = df_clean_filtered["Insurance Provider"].nunique()

col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Total Patients", total_patients)  # Corrected
col2.metric("Total Billing Amount", f"${total_bill:,.2f}")  # Formatted billing amount
col3.metric("Total Hospitals", total_hospital)
col4.metric("Total Doctors", total_doctor)
col5.metric("Total Insurance Providers", total_insurance)

col1, col2, col3 = st.columns(3)
# ---- Plot 1: Patient Distribution by Gender (Pie Chart) ----
with col1:
    st.subheader('Patient Distribution by Gender')
    gender_count = df_clean_filtered['Gender'].value_counts()
    fig_gender_pie = px.pie(values=gender_count.values, 
                            names=gender_count.index, 
                            hole=0.4,
                            color_discrete_sequence=px.colors.qualitative.Set2)
    st.plotly_chart(fig_gender_pie)

# ---- Plot 2: Total Patients by Age Group (Bar Chart) ----
with col2:
    st.subheader('Total Patients by Age Group')
    # Define age bins and group patients by age
    bins = [0, 18, 35, 50, 65, 80, 100]
    labels = ['0-18', '19-35', '36-50', '51-65', '66-80', '81-100']
    df_clean_filtered['Age Group'] = pd.cut(df_clean_filtered['Age'], bins=bins, labels=labels, right=False)
    
    # Count the number of patients in each age group
    age_group_count = df_clean_filtered['Age Group'].value_counts().sort_index()
    
    fig_age = px.bar(age_group_count, 
                     x=age_group_count.index, 
                     y=age_group_count.values, 
                     labels={'x': 'Age Group', 'y': 'Count'},
                     title="Patients by Age Group",
                    color_discrete_sequence=px.colors.qualitative.Set1_r)
    st.plotly_chart(fig_age)
    
    # ---- Plot 3: Total Billing Amount by Year (Bar Chart) ----
with col3:
    st.subheader('Total Billing Amount by Year')
    
    # Extract the year from 'Date of Admission'
    df_clean_filtered['Year of Admission'] = pd.to_datetime(df_clean_filtered['Date of Admission']).dt.year
    
    # Group by year and sum the billing amounts
    billing_by_year = df_clean_filtered.groupby('Year of Admission')['Billing Amount'].sum().reset_index()
    
    fig_billing = px.line(billing_by_year, 
                         x='Year of Admission', 
                         y='Billing Amount', 
                         labels={'Year of Admission': 'Year', 'Billing Amount': 'Total Billing Amount'},
                         title="Total Billing Amount by Year",
                         color_discrete_sequence=px.colors.qualitative.Set1)
    st.plotly_chart(fig_billing)

# %% [markdown]
# ### Third Row

# %%
# Create three columns for the second set of plots
col1, col2, col3 = st.columns(3)

# ---- Plot 1: Total Patients by Medical Condition (Bar Chart) ----
with col1:
    # st.subheader('Total Patients by Medical Condition')
    condition_count = df_clean_filtered['Medical Condition'].value_counts()
    
    fig_condition = px.bar(condition_count, 
                           x=condition_count.index, 
                           y=condition_count.values, 
                           labels={'x': 'Medical Condition', 'y': 'Count'},
                           title="Patients by Medical Condition",
                           color_discrete_sequence=px.colors.qualitative.Set2)
    st.plotly_chart(fig_condition)
    # ---- Plot 2: Total Patients by Admission Type (Bar Chart) ----
with col2:
    # st.subheader('Total Patients by Admission Type')
    admission_count = df_clean_filtered['Admission Type'].value_counts()
    
    fig_admission = px.bar(admission_count, 
                           x=admission_count.index, 
                           y=admission_count.values, 
                           labels={'x': 'Admission Type', 'y': 'Count'},
                           title="Patients by Admission Type",
                           color_discrete_sequence=px.colors.qualitative.Set3)
    st.plotly_chart(fig_admission)

# ---- Plot 3: Total Billing Amount by Insurance Provider (Donut Chart) ----
with col3:
    # st.subheader('Total Billing Amount by Insurance Provider')
    
    # Group by Insurance Provider and sum the billing amounts
    billing_by_insurance = df_clean_filtered.groupby('Insurance Provider')['Billing Amount'].sum().reset_index()
    
    fig_donut = px.pie(billing_by_insurance, 
                       names='Insurance Provider', 
                       values='Billing Amount', 
                       hole=0.4,  # This makes it a donut chart
                       title="Total Billing Amount by Insurance Provider",
                       color_discrete_sequence=px.colors.qualitative.Pastel)
    
    st.plotly_chart(fig_donut)

# %% [markdown]
# ### Statistical analysis 

# %%
# Chi sq test on Gender and Admission Type
# Create a contingency table
contingency_table = pd.crosstab(df_clean['Gender'], df_clean['Admission Type'])

# Perform chi-square test
chi2, p, dof, expected = stats.chi2_contingency(contingency_table)

# %% [markdown]
# ### Chi-Square Test Results
# 
# **Chi-Square Statistic (χ²)**: 10.02  **p-value**: 0.0067  
# 
# Since the p-value is below the significance level of 0.05, we reject the null hypothesis. This result indicates a statistically significant association between **Gender** and **Admission type** in this dataset, suggesting that these two variables are likely dependent on each other.

# %%
# Check Normality - Shapiro-Wilk Test for each hospital group (only if there are 3 or more samples)
normality_results = {}
for hospital in df_clean['Hospital'].unique():
    group_data = df_clean[df_clean['Hospital'] == hospital]['Billing Amount']
    if len(group_data) >= 3:
        stat, p_value = stats.shapiro(group_data)
        normality_results[hospital] = {'Statistic': stat, 'p-value': p_value}
        print(f"Hospital: {hospital}, Shapiro-Wilk Test Statistic: {stat:.4f}, p-value: {p_value:.4f}")
    else:
        print(f"Hospital: {hospital} has less than 3 records; skipping normality test.")

# Check Homogeneity of Variances - Levene's Test (only if there are multiple groups with enough data)
valid_groups = [df_clean[df_clean['Hospital'] == hospital]['Billing Amount'] for hospital in df_clean['Hospital'].unique() if len(df_clean[df_clean['Hospital'] == hospital]) >= 3]
if len(valid_groups) > 1:
    stat, p_value = stats.levene(*valid_groups)
    print(f"\nLevene's Test for Homogeneity of Variances: Statistic={stat:.4f}, p-value={p_value:.4f}")
else:
    print("Not enough data for multiple groups; skipping Levene's test.")


# %% [markdown]
# #### Statistic: 0.8809, p-value: 0.9999
# 
# #### Homogeneity of Variances:
# The p-value of 0.9999 is much greater than the commonly used alpha level of 0.05. This indicates that we fail to reject the null hypothesis of equal variances. Thus, there is no significant evidence to suggest that the variances among the different hospital groups are different.
# ### Conclusion:
# The assumption of homogeneity of variances holds true for the data. This is an important requirement for performing ANOVA. Since this assumption is satisfied, can proceed with ANOVA testing.

# %%
# Analyze billing amount and hospital
# Group billing amounts by hospital
billing_by_hospital = [df_clean[df_clean['Hospital'] == hospital]['Billing Amount'] for hospital in df_clean['Hospital'].unique()]

# Perform one-way ANOVA
f_val, p_val = stats.f_oneway(*billing_by_hospital)

f_val, p_val

# %% [markdown]
# ### One-way ANOVA
# **f-value**: 1.57
# **p-value**: 2.49E-236
# 
# Since the p-value is 2.49E-236 way below the sinificance level of 0.05, the null hypothesis is rejected. The result indicates a statistlically significant association between **Hospital** and **Billing Amount** in the dataset, suggesting that they are likely dependent on each other.
# 

# %%
# Check Normality - Shapiro-Wilk Test for each Medical Condition group (only if there are 3 or more samples)
normality_results = {}
for Condition in df_clean['Medical Condition'].unique():
    group_data = df_clean[df_clean['Medical Condition'] == Condition]['Age']
    if len(group_data) >= 3:
        stat, p_value = stats.shapiro(group_data)
        normality_results[Condition] = {'Statistic': stat, 'p-value': p_value}
        print(f"Medical Condition: {Condition}, Shapiro-Wilk Test Statistic: {stat:.4f}, p-value: {p_value:.4f}")
    else:
        print(f"Medical Condition: {Condition} has less than 3 records; skipping normality test.")

# Check Homogeneity of Variances - Levene's Test (only if there are multiple groups with enough data)
valid_groups = [df_clean[df_clean['Medical Condition'] == hospital]['Age'] for hospital in df_clean['Medical Condition'].unique() if len(df_clean[df_clean['Medical Condition'] == Condition]) >= 3]
if len(valid_groups) > 1:
    stat, p_value = stats.levene(*valid_groups)
    print(f"\nLevene's Test for Homogeneity of Variances: Statistic={stat:.4f}, p-value={p_value:.4f}")
else:
    print("Not enough data for multiple groups; skipping Levene's test.")


# %% [markdown]
# ### Shapiro-Wilk Test Results:
# Normality: The p-values for all medical conditions are 0.0000, which is significantly less than the alpha level of 0.05. 
# This indicates that we reject the null hypothesis of normality for all groups. Thus, the age distributions for these medical conditions are not normally distributed.
# 
# ### Levene's Test Results:
# Statistic: 1.3972
# p-value: 0.2217
# 
# Homogeneity of Variances: The p-value of 0.2217 is greater than 0.05, which indicates that we fail to reject the null hypothesis of equal variances. Therefore, there is no significant evidence to suggest that the variances of age among the different medical conditions are different.

# %%
# Perform Kruskal-Wallis H test if normality is violated
kruskal_result = stats.kruskal(*valid_groups)
print(f"Kruskal-Wallis H Test Result: H-Statistic={kruskal_result.statistic:.4f}, p-value={kruskal_result.pvalue:.4f}")


# %% [markdown]
# ### Kruskal-Wallis H Test Results:
# H-Statistic: 3.1141
# 
# p-value: 0.6824
# 
# Null Hypothesis: The null hypothesis for the Kruskal-Wallis test states that there are no differences in the distributions of age among the different medical conditions.
# p-value: The p-value of 0.6824 is much greater than the alpha level of 0.05. Therefore, we fail to reject the null hypothesis.
# 
# ### Conclusion:
# There is no statistically significant difference in age distributions among the various medical conditions in your dataset. This means that, based on the data, the ages of patients with different medical conditions are likely similar.


