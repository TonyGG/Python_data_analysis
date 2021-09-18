import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
rng = np.random.RandomState(0)
x = np.linspace(0, 10, 500)
y = np.cumsum(rng.randn(500, 6), 0)
sns.set()
plt.plot(x, y)
plt.legend('ABCDEF', ncol=2, loc='upper left')

from sklearn.datasets import load_boston
# Set the palette and style to be more minimal
sns.set(style='ticks', palette='Set2')

# Load data as explained in introductory lesson
boston_data = load_boston()
boston_df = pd.DataFrame(boston_data.data, columns=boston_data.feature_names)



# Create the histogram plot
sns.distplot(boston_df.NOX, kde=False)
# Remove excess chart lines and ticks for a nicer looking plot
sns.despine()