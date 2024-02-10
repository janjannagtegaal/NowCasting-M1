import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter, YearLocator
from pandas.tseries.offsets import MonthBegin
import numpy as np
import seaborn as sns

####################################################################################################
# plot top n and bottom n correlated series with PCE


def plot_correlations(correlation_series, top_n=10, bottom_n=10):
    """
    Plot the top and bottom N correlated indicators with PCE.

    Parameters:
    - correlation_series: pd.Series with correlation values indexed by indicator names.
    - top_n: Number of top positively correlated indicators to display.
    - bottom_n: Number of bottom negatively correlated indicators to display.
    """
    # Extract top and bottom N correlated indicators
    top_positive_correlations = correlation_series.head(top_n)
    top_negative_correlations = correlation_series.tail(bottom_n)

    # Combine and prepare data for plotting
    correlations_combined = pd.concat(
        [top_positive_correlations, top_negative_correlations]
    ).reset_index()
    correlations_combined.columns = ["Indicator", "Correlation"]
    correlations_combined["Positive"] = correlations_combined["Correlation"] > 0

    # Create figure and axis for the plot
    plt.figure(figsize=(10, 8))
    ax = sns.barplot(
        x="Correlation",
        y="Indicator",
        hue="Positive",
        dodge=False,
        palette={True: "dodgerblue", False: "#FF7F50"},
        alpha=1,
        data=correlations_combined,
    )

    # Customize plot appearance
    plt.axvline(x=0, color="grey", linestyle="--")
    plt.xlabel("Correlation with PCE")
    plt.ylabel("Indicator")
    plt.title("Top and Bottom Correlated Indicators with PCE")
    plt.legend(title="Positive Correlation", loc="lower right", labels=["Yes", "No"])
    plt.legend().remove()  # Remove the legend if it's not necessary
    plt.grid(axis="x", color="grey", linestyle="--", linewidth=0.5)
    
    # remove the right and top spines
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    
    # make the left and bottom spines light grey and --
    ax.spines['left'].set_color('grey')
    ax.spines['left'].set_linestyle('--')
    ax.spines['bottom'].set_color('grey')
    ax.spines['bottom'].set_linestyle('--')

    # Annotate bars with the percentage of the correlation
    for p in ax.patches:
        width = p.get_width()
        offset = 0.01  # Adjust offset value for better visibility

        # Determine the text position based on the direction of the bar
        text_position = width + offset if width > 0 else width - offset

        # Position the text to the right of the bar if positive, left if negative
        ha = 'left' if width > 0 else 'right'

        plt.text(
            text_position,
            p.get_y() + p.get_height() / 2.0,
            "{:1.2f}".format(width),
            ha=ha,  # Horizontal alignment
            va='center',
            color="grey",
            fontsize='small'
        )


    plt.show()
