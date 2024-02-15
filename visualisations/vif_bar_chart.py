import pandas as pd
import plotly.express as px

def vif_bar_chart(vif_data):
    
    vif_data_sorted = vif_data.sort_values("VIF", ascending=False)
    # Create the bar chart
    fig = px.bar(
        vif_data_sorted,
        x="VIF",
        y="feature",
        orientation="h",
        height=1000,
        title="VIF Scores of Economic Indicators",
    )

    # Update layout to include a log scale for x-axis and to sort y-axis in ascending order
    fig.update_layout(
        yaxis={"categoryorder": "total ascending"},
        xaxis_title="VIF Score (log scale)",
        xaxis_type="log",
    )

    # Color the bars based on the VIF score threshold
    fig.update_traces(
        marker_color=vif_data_sorted["VIF"].apply(
            lambda x: "crimson" if x > 10 else "dodgerblue"
        )
    )

    #set vertical grids to light grey and thin dashed line
    fig.update_layout(xaxis_showgrid=True, xaxis_gridcolor='lightgrey', xaxis_gridwidth=0.5)

    #set chart area background color to white
    fig.update_layout(plot_bgcolor='white')

    # Add a vertical line to indicate the VIF threshold of 10
    fig.add_shape(
        type="line",
        x0=10,
        y0=-1,
        x1=10,
        y1=len(vif_data_sorted),
        line=dict(color="green", width=2),
    )

    fig.show()