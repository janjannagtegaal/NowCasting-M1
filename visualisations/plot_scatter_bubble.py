import plotly.express as px


def plot_scatter_bubble(comparison_df):
# Now let's create the bubble chart with groups
    fig = px.scatter(
        comparison_df,
        x="Correlation",
        y="R_squared",
        size="R_squared",  # Bubble sizes based on the R_squared values
        color="group",  # Color based on the group
        hover_name="description",  # Show the description on hover
        title="Bubble Chart of R^2 Values vs. Correlation Coefficients",
        size_max=20,  # Maximum bubble size
    )

    # Update layout for a cleaner look and add a legend
    fig.update_layout(
        xaxis_title="Correlation Coefficient",
        yaxis_title="R-Squared Value",
        xaxis=dict(showgrid=True),  # Show gridlines for better precision
        yaxis=dict(showgrid=True),  # Show gridlines for better precision
        plot_bgcolor="white",  # Set background to white for a clean look
        hovermode="closest",  # Show the closest point to the mouse
        legend_title_text="Group",  # Legend title
    )

    # decrease chart width
    fig.update_layout(
        autosize=False,
        width=1000,
        height=800,
    )

    # Show the figure
    fig.show()