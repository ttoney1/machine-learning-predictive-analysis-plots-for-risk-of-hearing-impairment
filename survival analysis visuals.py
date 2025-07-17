# Below is the Python code for one cohort, TED (Thyroid Eye Disease). The code creates a 
# helper function by using the input variables of time, event (1 for event, 0 for censored), 
# and predictor variable (e.g. gender) to apply routine steps across different predictor 
# columns to reduce repetitive lines of code. The same code was used apply to different 
# cohorts across several time-to-event datasets. 

# Predictor variables (covariates) hypothesized to influence time-to-event in the 
# study are gender, age group, and insurance. 
# Dependent variables are time (date) and event (hearing loss).

%python
# Import libraries
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import pandas as pd
import numpy as np

from lifelines import KaplanMeierFitter
from lifelines.utils import median_survival_times
from lifelines.statistics import pairwise_logrank_test
# Load the telco silver table
mkscev_1a_75_co_ry = spark.table('p24_rd_021.mkscev_model_1a_75_co_ry_v2').toPandas() #same dataset that I shared with you(TED_CO_KM) but this one has more columns which were not necessary for the KM curves. 

%python
# # Import the KaplanMeierFitter class
# from lifelines import KaplanMeierFitter

# Initialize the KaplanMeierFitter
kmf = KaplanMeierFitter()

# Extract the columns from the DataFrame
CO = mkscev_1a_75_co_ry['co_year']
C = mkscev_1a_75_co_ry['co_01'].astype(float)

# Fit the KaplanMeierFitter model
kmf.fit(CO)

%python
# Helper function for plotting Kaplan-Meier curves at the covariate level
def plot_km(col):
  ax = plt.subplot(111)
  for r in sorted(mkscev_1a_75_co_ry[col].unique()):
    ix = mkscev_1a_75_co_ry[col] == r
    kmf.fit(CO[ix], C[ix],label=r)
    kmf.survival_function_ = 1 - kmf.survival_function_
    kmf.plot(ax=ax)
    ax.set_ylim(0.0, 0.2) # Set y-axis scale from 0 to 1 
    ax.set_xlabel('Time (years)') # Set x-axis label 
    ax.set_ylabel('Failure probability (%)') # Set y-axis label

     # Set y-axis to display percentages
  ax.yaxis.set_major_formatter(mticker.PercentFormatter(1.0))

  ax.legend(loc='upper left') # Place legend at the bottom left corner

  # Add the title outside the plot
  # plt.suptitle('Figure 5: Plot of Kaplan-Meier curve with the risk of hearing impairment (composite outcome) among TED patients by gender.', y=1.05)
    
# Helper function for printing out Log-rank test results
def print_logrank(col):
  log_rank = pairwise_logrank_test(mkscev_1a_75_co_ry['co_year'], mkscev_1a_75_co_ry[col], mkscev_1a_75_co_ry['co_01'])
  return log_rank.summary
  
   %python
plot_km('gender')
plot_km('age_grp')
plot_km('insurance')

