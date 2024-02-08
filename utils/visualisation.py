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

    # Calculate the rate of change for each column
    pce_real_growth = df.pct_change().dropna() * 100

    # Create a figure and axis
    fig, ax = plt.subplots(figsize=(15, 5))

    # Call the plotting function
    plot_time_series_with_iqr_and_extended_range_subplot(pce_real_growth, ax, column)

    ax.set_title(f"Rate of Change for {column}")
    plt.show()
    pass


####################################################################################################
# plot economic series for multiple columns over time


def plot_dataset(dataset, title):

    def convert_index_to_datetime(index):
        """Convert 'YYYYQX' format to datetime, or return the input if it's already a datetime."""

        if isinstance(index, pd.Timestamp):
            return index  # Return the input directly if it's already a Timestamp

        year = int(index[:4])
        quarter = int(index[5])
        month = (quarter - 1) * 3 + 1  # Convert quarter to month

        return pd.Timestamp(year=year, month=month, day=1)

    # Convert index to datetime
    dataset.index = pd.to_datetime(dataset.index.map(convert_index_to_datetime))

    # Select random columns
    randint = np.random.randint(0, len(dataset.columns), 3)
    columns = dataset.columns[randint]

    # add 'PCE' to the columns
    columns = np.append(columns, "PCE")

    # Define color and style
    colors = ["grey", "dodgerblue", "coral", "black"]

    # Plot
    plt.figure(figsize=(15, 5))
    for i, column in enumerate(columns):
        plt.plot(dataset.index, dataset[column], label=column, color=colors[i],linewidth=1)

    # Enhance the chart
    plt.title(title)
    plt.xlabel("Date")
    plt.ylabel("Value")
    plt.legend()

    # Adjust x-axis to show every 10 years
    ax = plt.gca()  # Get current axis
    ax.xaxis.set_major_locator(YearLocator(10))  # Set major ticks to every 10 years
    ax.xaxis.set_major_formatter(DateFormatter("%Y"))  # Format tick labels as year only

    plt.xticks(rotation=45)
    plt.grid(True, which="both", linewidth=0.3)

    plt.show()

    pass

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


####################################################################################################
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
        axs[i].plot(df.index[-80:], df[feature][-80:], label=f"{feature} vs. PCE", color="black", linewidth=1)
        axs[i].plot(df.index[-80:], df["PCE"][-80:], label="PCE", color="red", linewidth=1,alpha=0.5)
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
    fig.suptitle("Top Correlations Against PCE", fontsize=16, y=0.95)

    # Show the plot
    plt.show()
    pass

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

def lollipop(data, threshold=10):
    # Filtering VIF values above threshold
    df_filtered = data[data["VIF"] > threshold]

    # Creating the flipped lollipop chart
    plt.figure(figsize=(8, 10))

    plt.hlines(
        y=df_filtered["feature"],
        xmin=0,
        xmax=df_filtered["VIF"],
        color="dodgerblue",
        alpha=0.4,
        zorder=3,
    )
    plt.scatter(
        df_filtered["VIF"],
        df_filtered["feature"],
        color="red",
        s=30,
        label=f"VIF > {threshold}",
        zorder=5,
    )

    # Adding text labels for each value, adjusting for flipped axes
    for i, row in df_filtered.iterrows():
        plt.text(
            row["VIF"],
            row["feature"],
            f" {row['VIF']:.2f}",
            va="center",
            ha="right",
            backgroundcolor="white",
            fontsize=8,
        )

    plt.xlabel("VIF Value")
    plt.title("Variance Inflation Factor (VIF): Indicators with highest Colinearity")
    plt.grid(axis="x", linestyle="--", linewidth=0.7, color="lightgrey", zorder=0)
    plt.tight_layout()

    # Hide the top, right, and bottom frame lines
    plt.gca().spines["top"].set_visible(False)
    plt.gca().spines["right"].set_visible(False)
    plt.gca().spines["bottom"].set_visible(False)

    # Show the plot
    plt.show()
    
    pass


####################################################################################################

import plotly.express as px

def plot_indicator_boxplot(long_data):
    """
    Generates a box plot of indicators, categorized by economic groups.

    Parameters:
    - long_data: DataFrame containing the long-form data for indicators and groups.

    The plot visualizes the distribution of indicator values, colored by their respective groups,
    and applies various customizations for readability and presentation.
    """
    # Filter out any groups that don't have any data to avoid plotting issues
    filtered_groups = long_data.dropna(subset=["Value"])["Group"].unique()

    # Generate box plot
    fig = px.box(
        long_data.dropna(subset=["Value"]),
        x="Value",
        y="Indicator",
        color="Group",
        category_orders={"Group": filtered_groups},
        title="Box Plot with Group as Legend"
    )

    # Update layout
    fig.update_layout(
        yaxis_title="",
        xaxis_title="Value",
        legend_title="Group",
        height=600,  # You can adjust the height of the plot as needed
        margin=dict(l=20, r=20, t=40, b=20)
    )

    # Place title in the middle
    fig.update_layout(title_x=0.5)

    # Make background white
    fig.update_layout(plot_bgcolor="white")

    # Optionally, set range of x-axis
    # fig.update_xaxes(range=[-30, 30])

    # Increase height of the chart
    fig.update_layout(
        autosize=False,
        width=1000,
        height=800
    )

    # Remove outliers
    fig.update_traces(boxpoints=False)

    fig.show()
