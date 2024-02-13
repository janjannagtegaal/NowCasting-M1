# markdown_generator.py

import numpy as np

def generate_model_performance_markdown(mae, rmse,predicted_pce):
    markdown_content = f"""
<div style="color:#FF7F50">

##### Model Performance

</div>

The predicted PCE values for the model is {', '.join([f"{mse:.4f}" for mse in predicted_pce])}.

The Mean Absolute Error (MAE) and Root Mean Squared Error (RMSE) provide insights into the model's accuracy:

- **Mean Absolute Error (MAE): {mae:.4f}** suggests that, on average, the model's predictions are approximately {mae:.4f} units away from the actual PCE values. 
- **Root Mean Squared Error (RMSE): {rmse:.4f}** also reflects the model's prediction accuracy, accounting for the square root of the average squared differences between predicted and actual values. 
"""
    return markdown_content

####################################################################################################

import numpy as np

def generate_cv_performance_markdown(mse_scores, comparison_mse=None):
    average_mse = np.mean(mse_scores)
    markdown_content = f"""
<div style="color:#FF7F50">

##### Cross-Validation Performance

</div>

The cross-validation process provides an estimate of the model's prediction error across different temporal splits of the dataset. Here are the insights from the time series cross-validation:

- **Mean Squared Error (MSE) Scores for Each Fold:** {', '.join([f"{mse:.4f}" for mse in mse_scores])}
- **Average Mean Squared Error (Average MSE): {average_mse:.4f}** suggests that, on average, the squared difference between the model's predictions and the actual PCE values is approximately {average_mse:.4f}. This metric helps in understanding the average prediction error across all folds, providing insight into the model's overall performance.

"""

    # Improved Additional Analysis
    additional_analysis = """
<div style="color:#FF7F50">

##### Additional Analysis

</div>

"""
    if comparison_mse:
        difference = average_mse - comparison_mse
        comparison_analysis = f"- Compared to the previous model's MSE of {comparison_mse:.4f}, this model shows a {'reduction' if difference < 0 else 'increase'} in the average MSE by {abs(difference):.4f} units. This {'improvement' if difference < 0 else 'deterioration'} suggests {'better' if difference < 0 else 'worse'} predictive accuracy."
        additional_analysis += comparison_analysis + "\n"
    
    additional_insights = f"""
- Understanding the model's performance in the context of economic forecasting is crucial. A lower Average MSE means the model is potentially more reliable for predicting future PCE values, which can aid policymakers and economists in making informed decisions.
- It's important to identify which factors contribute most significantly to prediction errors. Analyzing feature importance and error patterns could reveal insights into economic trends or anomalies.
- Continuous improvement should involve refining the model by exploring additional features, incorporating external economic indicators, or testing more sophisticated forecasting techniques.
"""

    markdown_content += additional_analysis + additional_insights
    return markdown_content


from IPython.display import Markdown, display

def generate_markdown_conclusions(row,df):
    
    indicator_details = df.loc[row['Indicator']]
    
    md_text = f"""
<div style="color:#FF7F50">

---

**{row['Indicator']}**

</div>

- **Correlation with PCE**: {indicator_details['Correlation']:.3f}, indicating {"a strong" if abs(indicator_details['Correlation']) > 0.5 else "a weak"} relationship with PCE.
- **R²**: {row['R^2']:.3f}: This indicator explains approximately {row['R^2'] * 100:.1f}% of the variance in PCE, indicating {"a strong" if row['R^2'] > 0.5 else "a weaker"} linear relationship.
- **Coefficient**: {row['Coefficient']:.3f}: {"The coefficient is statistically significant, suggesting a meaningful impact on PCE." if row['P-Value'] < 0.05 else "The coefficient is not statistically significant, suggesting a less reliable impact on PCE."}
- **P-Value**: {row['P-Value']:.2e} : {"The relationship is statistically significant, strongly rejecting the null hypothesis of no association." if row['P-Value'] < 0.05 else "The relationship is not statistically significant, failing to reject the null hypothesis of no association."}
- **Stationarity**: {indicator_details['Conclusion']}, confirming the data {"does" if indicator_details['Conclusion'] == "Stationary" else "does not"} exhibit constant mean and variance over time.
- **Durbin-Watson**: {row['Durbin-Watson']:.3f}: {"There is minimal autocorrelation in the residuals, indicating independence of observations." if 1.5 < row['Durbin-Watson'] < 2.5 else "There may be autocorrelation in the residuals, which could affect the model's assumptions."}
- **Jarque-Bera (JB) Statistic and P-Value**: {row['JB Statistic']:.2f}, {row['JB P-Value']:.2e}: {"The residuals appear to be normally distributed, supporting the model's assumptions." if row['JB P-Value'] > 0.05 else "The residuals do not appear to be normally distributed, indicating potential issues with the model."}


"""
    display(Markdown(md_text))

    # - **VIF**: {indicator_details['VIF']:.2f}, suggesting {"significant" if indicator_details['VIF'] > 5 else "minimal"} multicollinearity.