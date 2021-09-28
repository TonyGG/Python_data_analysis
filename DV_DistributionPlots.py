"""Distribution plots"""
from sklearn.datasets import load_boston
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
# Set the palette and style to be more minimal
sns.set(style='ticks', palette='Set2')

# Load data as explained in introductory lesson
# note: load data from sklearn is not pd.dataframe by default.
# need to use pd.DataFrame to covert
boston_data = load_boston()
boston_df = pd.DataFrame(boston_data.data, columns=boston_data.feature_names)

# Create the histogram plot
sns.distplot(boston_df.NOX, kde=False)
# Remove excess chart lines and ticks for a nicer looking plot
sns.despine()

# Create the histogram plot with more bins
sns.distplot(boston_df.NOX, bins=100, kde=False)
# Remove excess chart lines and ticks for a nicer looking plot
sns.despine()
# kde is to add reference line to the histogram. easier to see the data distribution
sns.distplot(boston_df.NOX, kde=True)
# Remove excess chart lines and ticks for a nicer looking plot
sns.despine()

'''
Boxplot note:
median (Q2/50th Percentile): the middle value of the dataset.
first quartile (Q1/25th Percentile): the middle number between the smallest number (not the “minimum”) and the median of the dataset.
third quartile (Q3/75th Percentile): the middle value between the median and the highest value (not the “maximum”) of the dataset.
interquartile range (IQR): 25th to the 75th percentile.
whiskers (shown in blue)
outliers (shown as green circles)
“maximum”: Q3 + 1.5*IQR
“minimum”: Q1 -1.5*IQR
'''
# Create the box plot
sns.boxplot(boston_df.NOX)
# Remove excess chart lines and ticks for a nicer looking plot
sns.despine()

# Create the violin plot
# the outer shape of violin plot represents the distribution. tells the high and low probability
sns.violinplot(boston_df['INDUS'], orient="v")
# Remove excess chart lines and ticks for a nicer looking plot
sns.despine()

# Create the joint plot
# joint plot shows both correlation between two variables and variable data distribtuion
sns.jointplot(boston_df.CRIM, boston_df.NOX, kind="hex")
# Remove excess chart lines and ticks for a nicer looking plot
sns.despine()