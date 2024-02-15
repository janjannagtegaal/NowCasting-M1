
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
        height=600,  
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