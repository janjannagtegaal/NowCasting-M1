# markdown_generator.py

def generate_model_performance_markdown(mae, rmse):
    markdown_content = f"""
<div style="color:#00BFFF">

##### Model Performance

</div>

The Mean Absolute Error (MAE) and Root Mean Squared Error (RMSE) provide insights into the model's accuracy:

- **Mean Absolute Error (MAE): {mae:.4f}** suggests that, on average, the model's predictions are approximately {mae:.4f} units away from the actual PCE values. 
- **Root Mean Squared Error (RMSE): {rmse:.4f}** also reflects the model's prediction accuracy, accounting for the square root of the average squared differences between predicted and actual values. 
"""
    return markdown_content
