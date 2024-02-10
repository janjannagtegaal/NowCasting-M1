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
        palette={True: "skyblue", False: "salmon"},
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

    # Annotate bars with the percentage of the correlation
    for p in ax.patches:
        width = p.get_width()
        plt.text(
            p.get_width(),
            p.get_y() + p.get_height() / 2.0 + 0.2,
            "{:1.2f}".format(width),
            ha="center",
            va="center",
        )

    plt.show()

    pass