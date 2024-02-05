import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter, YearLocator
from pandas.tseries.offsets import MonthBegin
import numpy as np
import seaborn as sns

####################################################################################################
#Plot series with Extended Range and IQR and outliers

def analyze_and_plot(df,column):
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
                standardized_date = pd.to_datetime(date_str, errors='coerce')
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
        ax.plot(datetime_index, df[column], marker='o', markersize=3, color='black', linewidth=1, label=column)

        # Shade the IQR
        ax.fill_between(datetime_index, Q1, Q3, color='grey', alpha=0.4, label='IQR')
        
        # Shade the extended range
        ax.fill_between(datetime_index, lower_whisker, upper_whisker, color='lightgrey', alpha=0.3, label='Extended Range')
        
        # Mark potential outliers
        outliers = df[column][(df[column] < lower_whisker) | (df[column] > upper_whisker)]
        ax.scatter(outliers.index, outliers, color='red', zorder=5, label='Outliers')

        # Add median line
        ax.axhline(median, color='darkgreen', linestyle='--', linewidth=1.0, label='Median')
        
        # Add upper and lower whiskers lines
        ax.axhline(upper_whisker, color='grey', linestyle='--', linewidth=1, label='Upper Whisker')
        ax.axhline(lower_whisker, color='grey', linestyle='--', linewidth=1, label='Lower Whisker')

        # Add labels and legend
        ax.set_xlabel('Time')
        ax.set_ylabel(column)
        ax.set_title(f'{column}')
        ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        ax.grid(False)

    # Calculate the rate of change for each column
    pce_real_growth = df.pct_change().dropna() * 100

    # Create a figure and axis
    fig, ax = plt.subplots(figsize=(15, 5))

    # Call the plotting function
    plot_time_series_with_iqr_and_extended_range_subplot(pce_real_growth, ax, column)

    ax.set_title(f'Rate of Change for {column}')
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
    
    #add 'PCE' to the columns
    columns = np.append(columns,'PCE')
    
    # Define color and style
    colors = ['grey', 'dodgerblue', 'coral','black']
    
    # Plot
    plt.figure(figsize=(15, 6))
    for i, column in enumerate(columns):
        plt.plot(dataset.index, dataset[column], label=column, color=colors[i])

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
    plt.grid(True, which='both', linewidth=0.3)
    
    plt.show()
    
    pass

####################################################################################################
# #plot top correlated series with PCE

# def plot_top_correlations(top_cor,n = 15):
#     # Convert the Series to a DataFrame for plotting and sort by the absolute values
#     top_correlations_df = top_cor.head(n).reset_index()
#     top_correlations_df.columns = ['Indicator', 'Correlation']
#     top_correlations_df['AbsCorrelation'] = top_correlations_df['Correlation'].abs()
#     top_correlations_df = top_correlations_df.sort_values(by='AbsCorrelation', ascending=False)

#     # Set the color for each bar based on correlation value
#     colors = ['grey' if (x < max(top_correlations_df['AbsCorrelation'])) else 'red' for x in top_correlations_df['Correlation']]

#     # Initialize the matplotlib figure
#     f, ax = plt.subplots(figsize=(12, 6))

#     # Plot the correlations using the original Correlation values, not the absolute ones
#     sns.barplot(x="Correlation", y="Indicator", data=top_correlations_df,
#                 palette=colors, edgecolor=".2")

#     # Customize the aesthetics
#     sns.despine(left=True, bottom=True)
#     ax.set_xlabel('Correlation Coefficient')
#     ax.set_ylabel('')
#     ax.set_title('Top 15 Correlations to PCE', fontsize=16)
#     ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{x:.2f}'))

#     # Optional: Add value labels to each bar for direct reading
#     for i, v in enumerate(top_correlations_df['Correlation']):
#         ax.text(v if v > 0 else 0, i + .25, f'{v:.2f}', color='black', va='center', fontsize=9)

#     plt.show()
    
    
####################################################################################################
#plot top n and bottom n correlated series with PCE

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
    correlations_combined = pd.concat([top_positive_correlations, top_negative_correlations]).reset_index()
    correlations_combined.columns = ['Indicator', 'Correlation']
    correlations_combined['Positive'] = correlations_combined['Correlation'] > 0

    # Create figure and axis for the plot
    plt.figure(figsize=(10, 8))
    ax = sns.barplot(x='Correlation', y='Indicator', hue='Positive', dodge=False,
                     palette={True: 'skyblue', False: 'salmon'}, data=correlations_combined)

    # Customize plot appearance
    plt.axvline(x=0, color='grey', linestyle='--')
    plt.xlabel('Correlation with PCE')
    plt.ylabel('Indicator')
    plt.title('Top and Bottom Correlated Indicators with PCE')
    plt.legend(title='Positive Correlation', loc='lower right', labels=['Yes', 'No'])
    plt.legend().remove()  # Remove the legend if it's not necessary
    plt.grid(axis='x', color='grey', linestyle='--', linewidth=0.5)

    # Annotate bars with the percentage of the correlation
    for p in ax.patches:
        width = p.get_width()
        plt.text(p.get_width(), p.get_y() + p.get_height() / 2. + 0.2,
                 '{:1.2f}'.format(width),
                 ha='center', va='center')

    plt.show()
    
    pass

####################################################################################################
#plot top correlated features vs PCE in a subplot layout


def top_indicators_against_pce_line_graph(df,top_correlations):

    # Extract the top correlated features excluding 'PCE'
    top_features = [feature for feature in top_correlations.index[:12] if feature != 'PCE']

    # Setup the figure and subplots
    fig, axs = plt.subplots(6, 2, figsize=(25, 20))  # Adjust figsize as needed
    fig.subplots_adjust(hspace=0.4, wspace=0.3)  # Adjust spacing as needed

    # Flatten the axes array for easy iteration
    axs = axs.flatten()

    # Plot each feature in its subplot against PCE
    for i, feature in enumerate(top_features):
        # Plotting feature against PCE
        axs[i].plot(df.index[-80:], df[feature][-80:], label=f'{feature} vs. PCE',color='black')
        axs[i].plot(df.index[-80:], df['PCE'][-80:], label='PCE', color='red',alpha=0.5)
        axs[i].set_title(f'{feature} vs. PCE')
        axs[i].set_xlabel('Date') 
        axs[i].set_ylabel('Value')
        axs[i].legend()

    # Ensure we only use the subplots needed for the top features
    for j in range(i + 1, 10):
        fig.delaxes(axs[j])

    # Add an overall title
    fig.suptitle('Top Correlations Against PCE since 2000', fontsize=16)

    # Show the plot
    plt.show()

    
#     pass

####################################################################################################
# inspect for colinearity


def plot_correlation_circle_heatmap(dataset, correlations, top_n=20, fig_title='Correlation Circle Heatmap'):
    """
    Plots a correlation circle heatmap for the top N indicators based on provided correlations.

    :param dataset: Pandas DataFrame containing the data.
    :param correlations: Pandas Series containing correlation values with index as indicators.
    :param top_n: Integer representing the top N indicators to plot.
    :param fig_title: String representing the title of the figure.
    """
    # Get the top N indicators (excluding 'PCE')
    top_indicators = correlations.head(top_n).index.drop('PCE')

    # Create a correlation matrix for the top N indicators
    correlation_matrix = dataset[top_indicators].corr()

    # Set up the matplotlib figure
    fig, ax = plt.subplots(figsize=(10, 10))

    # Generate a colormap
    cmap = sns.diverging_palette(20, 230, as_cmap=True)

    # Get the coordinates
    x_coords, y_coords = np.meshgrid(correlation_matrix.columns, correlation_matrix.index)

    # Get correlation values for size - scaled for visibility
    sizes = np.abs(correlation_matrix.values.flatten()) * 400

    # Get colors based on correlation values
    colors = [cmap(val) for val in correlation_matrix.values.flatten()]

    # Create the bubble heatmap
    for (x, y), size, color in zip(np.c_[x_coords.ravel(), y_coords.ravel()], sizes, colors):
        ax.scatter(x, y, s=size, c=[color])

    # Improve layout
    ax.set_xticks(np.arange(len(correlation_matrix.columns)))
    ax.set_yticks(np.arange(len(correlation_matrix.index)))
    ax.set_xticklabels(correlation_matrix.columns)
    ax.set_yticklabels(correlation_matrix.index)
    plt.xticks(rotation=45, ha='right')
    plt.yticks(rotation=0)
    ax.set_title(fig_title, pad=20)
    
    # Adding a light grid
    ax.grid(True, which='both', linestyle='--', linewidth=0.5, color='gray', alpha=0.5)


    plt.show()