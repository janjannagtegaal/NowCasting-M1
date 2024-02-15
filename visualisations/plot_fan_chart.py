import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import dates as mdates

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
    """
    # Filter the combined_actual_pce to start from the specified start_date
    start_date_dt = pd.to_datetime(start_date, format='%Y-%m-%d')
    combined_actual_pce = pd.concat([df_train['PCE'], C]).sort_index()
    combined_actual_pce = combined_actual_pce[combined_actual_pce.index >= start_date_dt]
    
    dates_for_plotting = combined_actual_pce.index  # Dates for plotting
    
    # Train model and calculate residuals for the training data
    pipeline, _ = train_and_predict(X_train, y_train, X_train.loc[df_train.index >= start_date_dt])
    y_train_pred = pipeline.predict(X_train.loc[df_train.index >= start_date_dt])
    residuals = y_train.loc[df_train.index >= start_date_dt] - y_train_pred
    prediction_uncertainty_std = np.std(residuals)

    # Plot settings
    plt.figure(figsize=(15, 6))
    
    # Actual PCE line
    plt.plot(dates_for_plotting, combined_actual_pce, color='DodgerBlue', linestyle='-', marker='o', linewidth=2, label='Actual PCE')
    
    # Predicted PCE line
    prediction_dates = dates_for_plotting[-len(predicted_pce):]
    plt.plot(prediction_dates, predicted_pce, color='#FF7F50', linestyle='--', marker='o', label='Predicted PCE')
    
    # Confidence interval or STD
    ci_lower = predicted_pce - 1.96 * prediction_uncertainty_std
    ci_upper = predicted_pce + 1.96 * prediction_uncertainty_std
    
    plt.fill_between(prediction_dates, ci_lower, ci_upper, color='#FF7F50', alpha=0.2, label='95% Confidence Interval')

    # Enhancements for clarity and aesthetics
    plt.title('Fan Chart: Actual vs. Predicted PCE with Uncertainty')
    plt.xlabel('Date')
    plt.ylabel('PCE')
    plt.legend(loc='upper left')
    plt.grid(True, which='both', linestyle='--', linewidth=0.5, alpha=0.5)
    
    # Clean up borders and ticks
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)
    plt.gca().spines['bottom'].set_color('grey')
    plt.gca().spines['bottom'].set_linestyle('--')
    plt.gca().spines['left'].set_color('grey')
    plt.gca().spines['left'].set_linestyle('--')
    

    
    #set x-axis labels to grey
    plt.gca().xaxis.label.set_color('grey')
    plt.gca().yaxis.label.set_color('grey')
    
    plt.gca().xaxis.set_major_locator(mdates.MonthLocator(bymonth=(3, 6, 9, 12)))
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    plt.gcf().autofmt_xdate()  # Improve the layout of dates on the x-axis
    
    #make x-axis dates grey
    plt.gca().xaxis.set_tick_params(color='grey')
    plt.gca().yaxis.set_tick_params(color='grey')

    plt.tight_layout()
    plt.show()
