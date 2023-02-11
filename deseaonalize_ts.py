'''
In this script, we first load the time series data into a Pandas DataFrame. We then apply the seasonal decomposition function, specifying a model of 'additive' (i.e., assuming that the seasonal component has a constant amplitude throughout the time series) and a period of 12 (assuming that the data has a yearly seasonal pattern). The resulting decomposition object contains separate arrays for the trend, seasonal, and residual components.
We then extract the deseasonalized data by subtracting the seasonal component from the original data. Finally, we save the deseasonalized data to a new file using the to_csv method. Note that you may need to adjust the parameters of the seasonal decomposition function (e.g., the model or period) to best fit your specific data.
'''
import pandas as pd
from statsmodels.tsa.seasonal import seasonal_decompose

# load time series data
data = pd.read_csv('time_series_data.csv', index_col=0, parse_dates=True)

# perform seasonal decomposition
decomp = seasonal_decompose(data, model='additive', period=12)

# extract deseasonalized data (trend + residual)
deseasonalized = data - decomp.seasonal

# save deseasonalized data to a new file
deseasonalized.to_csv('deseasonalized_data.csv')
