<div style="color:#00BFFF">

### Log Transformation on joined dataset for comparability

**Rationale:** 

Logarithmic transformation is used to stabilize the variance in data that exhibits exponential growth or large fluctuations. This is especially crucial for datasets like FRED's, where certain indicators can show significant variability over time. Given the information from the FRED database and their suggested transformation types, it seems reasonable to align with their expertise and apply these transformations to the dataset. This approach will save time and ensure that the data is treated consistently with established economic analysis practices.

**Transformation Types (as per FRED):**

1. **No Transformation (1)**: The data is used as is, without any modification.
   
2. **First Difference (∆x_t) (2)**: The change from one period to the next, useful for highlighting trends.
   
3. **Second Difference (∆^2x_t) (3)**: The change in the first difference, often used to capture acceleration or deceleration in a series.
   
4. **Natural Log (log(x_t)) (4)**: Useful for stabilizing variance and making exponential growth trends linear.
   
5. **First Difference of Log (∆ log(x_t)) (5)**: Commonly used to convert data into a stationary series, representing percentage change.
   
6. **Second Difference of Log (∆^2 log(x_t)) (6)**: The change in the first difference of the log, similar to the second difference but for logged data.
   
7. **Percentage Change from Prior Period (∆(x_t/x_t_−_1 − 1.0)) (7)**: This calculates the percentage change from the previous period, emphasizing relative changes.

**Approach:**

- **Apply Transformations:** Apply FRED Transformations and use the transformation codes provided in the `fred_indicator_mappings` dataset to transform the corresponding series in `pce_joined_dataset`.
- This approach should streamline our analysis process and align with the methodology with FRED's established practices. 
- Additionally, it ensures that the data is treated in a manner that is suitable for economic analysis.
-  **FRED Logarithmic Key Mapping:** We will map the transformation codes in the FREDmd_defn dataset to our dataset's indicators and then perform the necessary transformations.







#  transformation function to handle the time column and a special case for PCE
def modified_log_transform(column, time_column, transformation_code=4, column_name=None):
    """
    Applies the specified transformation to a Pandas Series, considering the time column and special cases.
    """
    # Special instruction for the PCE column
    if column_name in ("PCE",'Primary_Sector_Index', 'Secondary_Sector_Index', 'Tertiary_Sector_Index', 'Public_Sector_Index'):
        transformation_code = 5  #6 # according to FREDs guidelines

    # Check if the data is quarterly based on the time column
    mult = 4 if any(time_column.str.endswith(('Q1', 'Q2', 'Q3', 'Q4'))) else 1

    if transformation_code == 1:
        # No transformation -> Mathematical Equation: x(t)
        # It leaves the data in its original form, without any alteration.
        return column
    
    elif transformation_code == 2:
        # First Difference -> Mathematical Equation: x(t) - x(t-1)
        # It measures the absolute change from one period to the next, helping to detrend the data.
        return column.diff()
    
    elif transformation_code == 3:
        # Second Difference -> Mathematical Equation: (x(t) - x(t-1)) - (x(t-1) - x(t-2))
        # It measures the change in the first difference, capturing the acceleration or deceleration in the data's movement.
        return column.diff().diff()
    
    elif transformation_code == 4:
        # Log Transformation -> Mathematical Equation: ln(x(t))
        # It stabilizes the variance across the data series and can help make a skewed distribution more normal.
        return np.log(column)
    
    elif transformation_code == 5:
        # Log First Difference -> Mathematical Equation: 100 * (ln(x(t)) - ln(x(t-1)))
        # It measures the growth rate from one period to the next and multiplies by 100 for percentage change.
        # The 'mult' variable allows for scaling the growth rate if necessary.
        return np.log(column).diff() * 100 * mult
    
    elif transformation_code == 6:
        # Log Second Difference -> Mathematical Equation: 100 * ((ln(x(t)) - ln(x(t-1))) - (ln(x(t-1)) - ln(x(t-2))))
        # It measures the change in the growth rate (change in log first difference), capturing the momentum of change.
        # The 'mult' variable allows for scaling the change in growth rate if necessary.
        return np.log(column).diff().diff() * 100 * mult
    
    elif transformation_code == 7:
        # Exact Percent Change -> Mathematical Equation: 100 * ((x(t)/x(t-1))^mult - 1)
        # It measures the percentage change from one period to the next, with an option to compound the change using 'mult'.
        return ((column / column.shift(1))**mult - 1.0) * 100
    
    else:
        raise ValueError("Invalid transformation code")


# Create a mapping of columns to transformation codes
transformation_mapping = defn.set_index('description')['tcode'].to_dict()

# Extracting the time column
time_column = joined_dataset.index

# Applying the transformations to the dataframe
transformed_dataset = joined_dataset.copy()

for column in transformed_dataset.columns:
    # Check if the column is in the mapping, else apply special instruction for PCE
    tcode = transformation_mapping.get(column, None)
    transformed_dataset[column] = modified_log_transform(transformed_dataset[column], time_column, tcode, column)

# Drop the first 5 rows containing NaN values resulting from the transformation
transformed_dataset = transformed_dataset.iloc[5:]

# Displaying the first few rows of the transformed dataset
joined_dataset = transformed_dataset
joined_dataset.head(8)

# just do simple log 1st dif

# leave log out as possible transformation

