import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter, YearLocator
from pandas.tseries.offsets import MonthBegin
import numpy as np
import seaborn as sns

####################################################################################################
# Plot series with Extended Range and IQR and outliers


def analyze_and_plot(df, column):
    """
    Function to standardize datetime index, compute statistics, and plot data from the given DataFrame.

    Parameters:
    - df: DataFrame containing the data to analyze and plot.
    - column: The name of the column to analyze and plot.
    """

    def standardize_datetime_index(index):
        standardized_dates = []

        # Check if the index is a PeriodIndex and convert to Timestamp if necessary
        if isinstance(index, pd.PeriodIndex):
            return index.to_timestamp()

        # If the index is not a PeriodIndex, handle individual entries
        for date_str in index:
            if isinstance(date_str, pd.Period):
                # Convert Period to Timestamp
                standardized_date = date_str.to_timestamp()
            elif "Q" in str(date_str):
                # Handle quarterly data
                year, quarter = str(date_str).split("Q")
                month = (int(quarter) - 1) * 3 + 1
                standardized_date = pd.Timestamp(year=int(year), month=month, day=1)
            else:
                # For other formats, directly convert to datetime
                standardized_date = pd.to_datetime(date_str, errors="coerce")
            standardized_dates.append(standardized_date)

        return pd.to_datetime(standardized_dates)

    def plot_time_series_with_iqr_and_extended_range_subplot(df, ax, column):
        # Use the index as it is already in datetime format
        datetime_index = standardize_datetime_index(df.index)
        df.index = datetime_index

        # Calculate statistics
        median = df[column].median()
        std = df[column].std()
        Q1 = df[column].quantile(0.25)
        Q3 = df[column].quantile(0.75)
        IQR = Q3 - Q1
        lower_whisker = median - 2.698 * std
        upper_whisker = median + 2.698 * std

        # Plot the time series line graph
        ax.plot(
            datetime_index,
            df[column],
            marker="o",
            markersize=1.5,
            color="black",
            linewidth=1,
            label=column,
        )

        # Shade the IQR
        ax.fill_between(datetime_index, Q1, Q3, color="grey", alpha=0.4, label="IQR")

        # Shade the extended range
        ax.fill_between(
            datetime_index,
            lower_whisker,
            upper_whisker,
            color="lightgrey",
            alpha=0.3,
            label="Extended Range",
        )

        # Mark potential outliers
        outliers = df[column][
            (df[column] < lower_whisker) | (df[column] > upper_whisker)
        ]
        ax.scatter(outliers.index, outliers, color="red", zorder=5, label="Outliers")

        # Add median line
        ax.axhline(
            median, color="darkgreen", linestyle="--", linewidth=1.0, label="Median"
        )

        # Add upper and lower whiskers lines
        ax.axhline(
            upper_whisker,
            color="grey",
            linestyle="--",
            linewidth=1,
            label="Upper Whisker",
        )
        ax.axhline(
            lower_whisker,
            color="grey",
            linestyle="--",
            linewidth=1,
            label="Lower Whisker",
        )

        # Add labels and legend
        ax.set_xlabel("Time")
        ax.set_ylabel(column)
        ax.set_title(f"{column}")
        ax.legend(bbox_to_anchor=(1.05, 1), loc="upper left")
        ax.grid(False)
        
        #remove borders
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        
        #set bottom and left border to very light grey dashed
        ax.spines['bottom'].set_color('lightgrey')
        ax.spines['bottom'].set_linestyle('--')
        ax.spines['left'].set_color('lightgrey')
        ax.spines['left'].set_linestyle('--')
        

    # Calculate the rate of change for each column
    pce_real_growth = df.pct_change().dropna() * 100

    # Create a figure and axis
    fig, ax = plt.subplots(figsize=(15, 5))

    # Call the plotting function
    plot_time_series_with_iqr_and_extended_range_subplot(pce_real_growth, ax, column)

    ax.set_title(f"Rate of Change for {column}")
    plt.show()
