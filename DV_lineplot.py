# line plot. can be used to see time series data. or look at the correlation between two variables
import seaborn as sns  # importing seaborn functionality
from sklearn.datasets import load_boston
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
# it's easier to explore the correlation between two variables.
sns.heatmap(flights, annot=True, fmt="d", linewidths=.5, ax=ax, cmap='Blues')

flights = sns.load_dataset("flights")
# Subset the data to years >= 1956 to more easily fit on the plot
flights = flights[flights.year >= 1956]
# great to explor lower level time series group by year
# margin title make the lenth shorter
g = sns.FacetGrid(flights, row="year", margin_titles=True)
g.map(plt.plot, "passengers", color="steelblue")


# PairGrid
# This function plots pairwise relationships in a grid.
# You generally pass one parameter which is a dataframe consisting of the columns you wish to plot.
sns.set(style='ticks', palette='Set2')

# Load data as explained in introductory lesson
boston_data = load_boston()
boston_df = pd.DataFrame(boston_data.data, columns=boston_data.feature_names)

# Create and map the PairGrid
g = sns.PairGrid(boston_df[['CRIM', 'NOX', 'INDUS']])
g.map(plt.scatter);

# Remove excess chart lines and ticks for a nicer looking plot
sns.despine()
