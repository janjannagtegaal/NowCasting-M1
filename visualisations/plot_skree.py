import matplotlib.pyplot as plt
import numpy as np

def plot_skree(pca):

    #  'pca.explained_variance_ratio_' is  PCA explained variance ratio array
    explained_variance_ratio = pca.explained_variance_ratio_

    # Calculate the cumulative variance explained
    cumulative_variance = np.cumsum(explained_variance_ratio)

    # Set up the figure and axes for the plot
    plt.figure(figsize=(10, 4))

    # Create the bar plot for the individual explained variances
    plt.bar(range(1, len(explained_variance_ratio) + 1), explained_variance_ratio, alpha=0.9, color='dodgerblue', label='Individual Explained Variance')

    # Add a line plot for the cumulative explained variance
    plt.plot(range(1, len(cumulative_variance) + 1), cumulative_variance, marker='o', linestyle='-', color='coral', label='Cumulative Explained Variance')

    # Title and labels
    plt.title('Scree Plot with Cumulative Explained Variance')
    plt.xlabel('Principal Component Number')
    plt.ylabel('Variance Explained (%)')

    # Set the ticks for x-axis
    plt.xticks(range(1, len(explained_variance_ratio) + 1))

    # add line across y-axis at 95% variance
    plt.axhline(y=0.95, color='black', linewidth=0.5,linestyle='--', label='95% Variance Explained')

    # Customize the grid and borders
    plt.grid(color='lightgrey', linestyle='--', linewidth=0.5)
    ax = plt.gca()
    ax.spines['top'].set_color('lightgrey')
    ax.spines['right'].set_color('lightgrey')
    ax.spines['left'].set_color('lightgrey')
    ax.spines['bottom'].set_color('lightgrey')
    ax.spines['top'].set_linestyle('--')
    ax.spines['right'].set_linestyle('--')
    ax.spines['left'].set_linestyle('--')
    ax.spines['bottom'].set_linestyle('--')
    ax.spines['top'].set_linewidth(0.5)
    ax.spines['right'].set_linewidth(0.5)
    ax.spines['left'].set_linewidth(0.5)
    ax.spines['bottom'].set_linewidth(0.5)

    # Add a legend to explain the lines
    plt.legend()

    # Show the plot
    plt.show()