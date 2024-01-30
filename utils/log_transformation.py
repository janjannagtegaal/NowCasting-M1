import numpy as np

def log_transform(column, transformation_code):
    """
    Applies the specified transformation to a Pandas Series.
    Transformation Codes from FRED suggested Description:
    1. No Transformation, 2. First Difference, 3. Second Difference,
    4. Log Transformation, 5. Log First Difference, 6. Log Second Difference,
    7. Exact Percent Change
    """
    # Assume the data is quarterly if the index ends with 'Q1', 'Q2', 'Q3', or 'Q4'
    mult = 4 if any(column.index.str.endswith(('Q1', 'Q2', 'Q3', 'Q4'))) else 1

    if transformation_code == 1:
        # No transformation
        return column
    elif transformation_code == 2:
        # First Difference
        return column.diff()
    elif transformation_code == 3:
        # Second Difference
        return column.diff().diff()
    elif transformation_code == 4:
        # Log Transformation
        return np.log(column)
    elif transformation_code == 5:
        # Log First Difference
        return np.log(column).diff() * 100 * mult
    elif transformation_code == 6:
        # Log Second Difference
        return np.log(column).diff().diff() * 100 * mult
    elif transformation_code == 7:
        # Exact Percent Change
        return ((column / column.shift(1))**mult - 1.0) * 100
    else:
        raise ValueError("Invalid transformation code")

# Apply log transformations using original column names according to FRED guidelines
# joined_log_transform = joined_dataset[:,1:].apply(lambda col: log_transform(col, transform_info[col.name][0]))
# joined_log_transform

# # Create an empty DataFrame to store the transformed data
# fred_log_transform = pd.DataFrame(index=joined_dataset.index)

# # Iterate through each column in fred_quarterly_rate_of_change
# for column_name in joined_dataset.columns:
#     # Fetch the transformation code for the current column from transform_info
#     transformation_code = transform_info.at[0, column_name]

#     # Apply the transformation using the transform function
#     transformed_column = log_transform(joined_dataset[column_name], transformation_code)

#     # Store the transformed column in the new DataFrame
#     fred_log_transform[column_name] = transformed_column

# fred_log_transform.head()