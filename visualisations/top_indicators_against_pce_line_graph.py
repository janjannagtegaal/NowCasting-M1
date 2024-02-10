import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter, YearLocator
from pandas.tseries.offsets import MonthBegin
import numpy as np
import seaborn as sns

# plot top correlated features vs PCE in a subplot layout
import numpy as np
import matplotlib.pyplot as plt

def top_indicators_against_pce_line_graph(df, top_correlations, top_n=10):
    """
    Plots line graphs of the top N correlated features against PCE.

    :param df: Pandas DataFrame containing the data.
    :param top_correlations: Pandas Series containing correlation values with index as indicators.
    :param top_n: Integer representing the number of top features to plot.
    """
    # Extract the top correlated features excluding 'PCE'
    top_features = [feature for feature in top_correlations.index[:top_n + 1] if feature != "PCE"]
    actual_top_n = len(top_features)  # Actual number of top features to plot

    # Calculate the grid size for subplots (assuming 2 columns)
    n_rows = int(np.ceil(actual_top_n / 2))

    # Setup the figure and subplots dynamically based on actual_top_n
    fig, axs = plt.subplots(n_rows, 2, figsize=(20, n_rows * 3.5))
    fig.subplots_adjust(hspace=0.4, wspace=0.3,top=0.9)

    # Handle single subplot case differently to ensure axs is always a list of AxesSubplot
    if n_rows == 1 and top_n == 1:
        axs = [axs]
    elif n_rows == 1:
        axs = axs.flatten()
    else:
        axs = axs.flatten()

    # Plot each feature in its subplot against PCE
    for i, feature in enumerate(top_features[:actual_top_n]):
        axs[i].plot(df.index[-80:], df[feature][-80:], label=f"{feature} vs. PCE", color="#FF7F50", linewidth=1)
        axs[i].plot(df.index[-80:], df["PCE"][-80:], label="PCE", color="dodgerblue", linewidth=1,alpha=0.9)
        axs[i].set_title(f"{feature} vs. PCE", fontsize=10)
        axs[i].set_xlabel("Date", fontsize=8,color='grey')
        axs[i].set_ylabel("Value", fontsize=8,color='grey')
        ## set no border for legend and decrease font, and set color to grey
        axs[i].legend(frameon=False, fontsize=8, loc='lower left', labelcolor='grey')
        axs[i].set_xticks(axs[i].get_xticks()[::12]) # Show every 20th tick to avoid crowding
        tick_labels = [label.get_text()[:4] for label in axs[i].get_xticklabels()]
        axs[i].set_xticklabels(tick_labels, fontsize=8,color='grey')
        axs[i].tick_params(axis='y', labelsize=8, labelcolor='grey')
        axs[i].tick_params(axis='x', labelsize=8, labelcolor='grey')
        
        #remove borders
        axs[i].spines['top'].set_visible(False)
        axs[i].spines['right'].set_visible(False)
        
        #set bottom and left border to very light grey dashed
        axs[i].spines['bottom'].set_color('lightgrey')
        axs[i].spines['bottom'].set_linestyle('--')
        axs[i].spines['left'].set_color('lightgrey')
        axs[i].spines['left'].set_linestyle('--')
        
        #no grid
        axs[i].grid(False)

        

    # Hide unused subplots
    for j in range(actual_top_n, len(axs)):
        fig.delaxes(axs[j])

    # Add an overall title
    #fig.suptitle("Top Correlations Against PCE", fontsize=16, y=0.95)

    # Show the plot
    plt.show()
