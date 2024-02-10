import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter, YearLocator
from pandas.tseries.offsets import MonthBegin
import numpy as np
import seaborn as sns

####################################################################################################
# inspect for colinearity


def plot_correlation_circle_heatmap(
    dataset, correlations, top_n=20, fig_title="Correlation Circle Heatmap"
):
    """
    Plots a correlation circle heatmap for the top N indicators based on provided correlations.

    :param dataset: Pandas DataFrame containing the data.
    :param correlations: Pandas Series containing correlation values with index as indicators.
    :param top_n: Integer representing the top N indicators to plot.
    :param fig_title: String representing the title of the figure.
    """
    # Get the top N indicators (excluding 'PCE')
    top_indicators = correlations.head(top_n).index.drop("PCE")

    # Create a correlation matrix for the top N indicators
    correlation_matrix = dataset[top_indicators].corr()

    # Set up the matplotlib figure
    fig, ax = plt.subplots(figsize=(10, 10))

    # Generate a colormap
    cmap = sns.diverging_palette(20, 230, as_cmap=True)

    # Get the coordinates
    x_coords, y_coords = np.meshgrid(
        correlation_matrix.columns, correlation_matrix.index
    )

    # Get correlation values for size - scaled for visibility
    sizes = np.abs(correlation_matrix.values.flatten()) * 400

    # Get colors based on correlation values
    colors = [cmap(val) for val in correlation_matrix.values.flatten()]

    # Create the bubble heatmap
    for (x, y), size, color in zip( #,value
        np.c_[x_coords.ravel(), y_coords.ravel()], sizes, colors, #correlation_matrix.values.flatten()
    ):
        ax.scatter(x, y, s=size, c=[color])
        # Annotate correlation values
        #ax.text(x, y, f"{value:.2f}", ha='center', va='center', color='black', fontsize=6, rotation=45)


    # Improve layout
    ax.set_xticks(np.arange(len(correlation_matrix.columns)))
    ax.set_yticks(np.arange(len(correlation_matrix.index)))
    ax.set_xticklabels(correlation_matrix.columns)
    ax.set_yticklabels(correlation_matrix.index)
    plt.xticks(rotation=45, ha="right")
    plt.yticks(rotation=0)
    ax.set_title(fig_title, pad=20)

    # Adding a light grid
    ax.grid(True, which="both", linestyle="--", linewidth=0.5, color="gray", alpha=0.5)

    plt.show()


####################################################################################################