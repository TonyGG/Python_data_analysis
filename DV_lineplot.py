# line plot. can be used to see time series data. or look at the correlation between two variables
import seaborn as sns  # importing seaborn functionality
import pandas as pd
import matplotlib.pyplot as plt

flights_long = sns.load_dataset("flights")  # importing dataset
type(flights_long)
# filtering the dataset to obtain the January records for all years
flights_long = flights_long[flights_long.month == 'Jan']


# plotting a line graph
plot = sns.lineplot(flights_long.year, flights_long.passengers)

# Load dataset
flights_long = sns.load_dataset("flights")
# Pivot the dataset from long to wide format
flights = flights_long.pivot("month", "year", "passengers")
# Create a larger figure size to plot on
f, ax = plt.subplots(figsize=(12, 6))
# Create the heat map
# heatmap need the column and index. the heatmap is exactly a colored projection of the dataframe.
sns.heatmap(flights, annot=True, fmt="d", linewidths=.5, ax=ax, cmap='Blues')

