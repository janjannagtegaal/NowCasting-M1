import matplotlib.pyplot as plt
import seaborn as sns


def plot_top_correlations_barchart(r2_values_sorted,top_n=20):
    """
    Plot a bar chart of the top N variables with the highest R^2 values.
    """
    # Extract the top N variables and their corresponding R^2 values
    top_vars = list(r2_values_sorted.keys())[:top_n]
    top_r2_values = list(r2_values_sorted.values())[:top_n]

    # Create a bar plot to visualize the R^2 values
    plt.figure(figsize=(12, 6))
    sns.set(style="whitegrid")
    ax = sns.barplot(x=top_r2_values, y=top_vars, palette="coolwarm")

    # Customize the plot appearance
    ax.set(xlim=(0, 1), xlabel="R^2 Value", ylabel="Independent Variables")
    plt.title(f"Top {top_n} Variables with Highest Predictive Power for PCE")
    plt.gca().invert_yaxis()  # Invert the y-axis to display the highest value at the top

    # Display the R^2 values on the bars
    for i, v in enumerate(top_r2_values):
        ax.text(v + 0.02, i, f"{v:.2f}", color="black", va="center")

    # Show the plot
    plt.show()
