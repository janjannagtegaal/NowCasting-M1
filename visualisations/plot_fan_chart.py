import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import make_pipeline

def train_and_predict(X_train, y_train, X_test,n_components=3):
    """
    Trains the model and makes predictions.
    """
    # Creating pipeline
    pipeline = make_pipeline(StandardScaler(), PCA(n_components), LinearRegression())
    
    # Fitting the model to the training data
    pipeline.fit(X_train, y_train)
    
    # Making predictions
    predicted_pce = pipeline.predict(X_test)
    
    return pipeline, predicted_pce

def plot_fan_chart(df_train, C, predicted_pce, X_train, y_train, start_date='2020-03-01'):
    """
    Creates a fan chart to visualize actual vs. predicted PCE with uncertainty, starting from a specified date.
    
    Args:
    - df_train: DataFrame containing the training data.
    - C: Series containing the test targets.
    - predicted_pce: The predicted PCE values for the test set.
    - cutoff_date: The cutoff date used to split the data (for reference).
    - start_date: The start date for the chart to display the data from.
    - format: The format of the cutoff_date and start_date strings.
    """
    # Ensure the indices are aligned by reindexing if necessary
    combined_actual_pce = pd.concat([df_train['PCE'], C]).sort_index()
    
    # Filter the combined_actual_pce to start from the specified start_date
    start_date_dt = pd.to_datetime(start_date, format='%Y-%m-%d')
    combined_actual_pce = combined_actual_pce[combined_actual_pce.index >= start_date_dt]
    
    # Prepare dates for plotting, ensuring they match the filtered combined_actual_pce index
    dates_for_plotting = combined_actual_pce.index

    # Recalculate residuals and prediction uncertainty based on the filtered data
    pipeline, _ = train_and_predict(X_train, y_train, X_train)
    y_train_pred = pipeline.predict(X_train.loc[df_train.index >= start_date_dt])
    residuals = y_train.loc[df_train.index >= start_date_dt] - y_train_pred
    prediction_uncertainty_std = np.std(residuals)
    
    plt.figure(figsize=(15, 6))
    plt.plot(dates_for_plotting, combined_actual_pce, 'green', label='Actual PCE')
    plt.plot(dates_for_plotting[-len(predicted_pce):], predicted_pce, 'b--', label='Predicted PCE')
    
    prediction_dates = dates_for_plotting[-len(predicted_pce):]

    for std_dev, color in zip([1, 2], ['skyblue', 'lightsteelblue']):
        plt.fill_between(prediction_dates, 
                         predicted_pce - prediction_uncertainty_std * std_dev, 
                         predicted_pce + prediction_uncertainty_std * std_dev, 
                         color=color, alpha=0.5, label=f'±{std_dev} STD')

    plt.title('Fan Chart: Actual vs. Predicted PCE with Uncertainty')
    plt.xlabel('Date')
    plt.ylabel('PCE')
    plt.legend()
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.tight_layout()
    plt.show()