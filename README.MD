<div style="color:#00BFFF">

# Project Overview

## Why This Project Was Chosen

</div>

This project addresses a critical gap in economic data analysis by focusing on the delay in reporting quarterly Gross Domestic Product (GDP) figures. Such delays hinder the ability of policymakers and market analysts to make timely decisions in a rapidly changing economic landscape. Our goal is to bridge this gap by leveraging high-frequency data proxies to gain faster and more precise insights into consumer behavior, thereby supporting more agile economic policy and strategy formulation.

<div style="color:#FF7F50">

### Specific Questions or Goals

</div>

- **Identification** of high-frequency data sources as accurate proxies for consumer spending.
- **Validation** of these proxies against established measures of consumer expenditure.
- **Development** of techniques to ensure these proxies provide immediate and reliable insights.
- **Addressing** potential discrepancies and harmonizing data frequencies for accurate analysis.
- **Ensuring** the economic relevance of the findings beyond mere statistical correlations.

<div style="color:#FF7F50">

### Reference to Similar Studies

</div>

Inspiration for this project comes from previous research, such as the work by McCracken, M.W., and Ng, S. (2015), "[FRED-MD: A Monthly Database for Macroeconomic Research](https://doi.org/10.20955/wp.2015.012)," which highlights the value of high-frequency data in economic forecasting. This underscores the potential of alternative data sources, like credit card transactions and online search trends, to enhance real-time economic trend analysis.

<div style="color:#00BFFF">

## Data Sources Overview

</div>

<div style="color:#FF7F50">

### Gross Domestic Product (BEAU)

</div>

- **Short Description:** Data from the U.S. Bureau of Economic Analysis, detailing seasonally adjusted quarterly U.S. GDP rates and components.
- **Relevance:** Crucial for nowcasting consumption with its detailed, time-series information.
- **Data Frequency:** Quarterly.
- **Location & Access:** Available for download in CSV format from the [U.S. Bureau of Economic Analysis (BEA)](https://www.bea.gov/data/gdp/gross-domestic-product).
- **Variables of Interest:** Private Consumption Expenditure (PCE).

<div style="color:#FF7F50">

### Federal Reserve Economic Data (FRED)

</div>

- **Short Description:** Managed by the Federal Reserve Bank of St. Louis, this database features 123 monthly economic indicators.
- **Relevance:** Offers a granular view of economic trends potentially impacting consumer spending.
- **Data Frequency:** Monthly.
- **Location & Access:** Direct download in CSV format from [FRED database](https://research.stlouisfed.org/econ/mccracken/fred-databases/).
- **Variables of Interest:** Indicators from various economic sectors for evaluating alternative proxies for nowcasting.

<div style="color:#00BFFF">

## Data Preparation and Analysis

</div>

<div style="color:#FF7F50">

### Loading and Preprocessing GDP Data

</div>

1. **Initial Loading**: The GDP data is loaded from a CSV file, omitting the first three rows for titles and summaries, and reads the next 28 rows for analysis.
2. **Column Clean-up**: Removes the index column and trims all leading and trailing spaces for data cleanliness.
3. **Column Renaming and Adjustment**: Renames the first column to 'description' and adjusts column names for clarity by concatenating them with the first row's values.
4. **Index Reset**: Resets the DataFrame index to ensure clean, sequential indexing after row modifications.
5. **Structuring Descriptions**: Implements a hierarchical naming system to reflect component hierarchies and maps full component descriptions to abbreviations for simplified future reference.
6. **Transforming Date Formats**: Standardizes date columns into 'YYYYQX' format for easier temporal analysis and transposes the dataset to prioritize time series analysis.

<div style="color:#FF7F50">

### Loading and Preprocessing FRED-MD Data

</div>

1. **Data Retrieval**: Loads the latest version of the FRED-MD dataset, filtering out rows with complete NAs and converting 'SASdate' to a Period Index for time-series analysis.
2. **Column Name Mapping**: Enhances data readability by mapping FRED-MD column names to descriptive titles using a definitions file.
3. **Transforming Monthly Data to Quarterly**: Filters monthly data to the last month of each quarter and converts it to a quarterly format to align with GDP report frequencies.

<div style="color:#FF7F50">

### Joining Data Sources

</div>

- **Data Merge**: After preprocessing, merges the FRED-MD dataset with the PCE data on their quarterly indices into a `joined_dataset` for combined analysis.

<div style="color:#FF7F50">

### Initial Data Visualization and Inspection

</div>

- **PCE Rate of Change Calculation**: Calculates the rate of change for PCE to identify trends and outliers, using a custom function `analyze_and_plot` for comprehensive visualization.

<div style="color:#FF7F50">

### Data Filtering

</div>

1. **Date Range Filtering**: Narrows the dataset to observations from 1980 onwards to capture sufficient business cycles for long-term analysis.
2. **Column Filtering**: Removes less reliable indicators based on their relevance and timeliness for macro-economic research.

<div style="color:#FF7F50">

### Handling Data Issues

</div>

- **Missing Data and Outliers**: Utilizes visual tools like `missingno` to identify and manage missing data and applies the Z-score method to handle outliers without eliminating them, preserving critical information.

<div style="color:#FF7F50">

### Normalisation and Data Transformation

</div>

1. **Indicator Measurement Type Harmonization**: Categorizes economic measures by type (e.g., dollar values, rates) for consistent analysis.

<div style="color:#00BFFF">

## Data Transformation with Log and Differencing

</div>

Economic indicators often display significant variability and trends that can obscure underlying patterns. To address this, we employ data transformation techniques aimed at stabilizing the variance in datasets, especially for indicators exhibiting exponential growth or substantial fluctuations. Following the guidelines suggested by McCracken, we align our data handling practices with established methods in economic analysis to ensure consistency and accuracy.

<div style="color:#FF7F50">

### Transformation Types

</div>

The transformation process is critical for preparing the data for in-depth analysis. Here are the transformation types as per the FRED column `tcode`, indicating the specific method applied to a series `x`:

1. **No Transformation:** The data remains unchanged and is used in its original form: `x(t)`.
2. **First Difference:** This highlights trends by showing the change from one period to the next: `∆xt => x.diff()`.
3. **Second Difference:** It captures acceleration or deceleration in trends by examining the change in the first difference: `∆2xt => x.diff().diff()`.
4. **Natural Log:** This method stabilizes variance and linearizes exponential growth trends: `log(xt) => np.log(x)`.
5. **First Difference of Log:** It transforms data into a stationary series, indicating percentage changes: `∆log(xt) => np.log(x).diff()`.
6. **Second Difference of Log:** Similar to the second difference but applied to logged data: `∆2log(xt) => np.log(x).diff().diff()`.
7. **Percentage Change from Prior Period:** This emphasizes relative changes by calculating percentage changes from the previous period: `∆(xt/xt−1 −1.0) => (indicator / indicator.shift(1) - 1.0) * 100`.

<div style="color:#FF7F50">

### Implementation

</div>

Our implementation strategy involves mapping the FRED transformation codes to the corresponding series in our `joined_dataset`. This mapping is facilitated by a specialized function, `modified_log_transform`, which applies the selected transformation to each series based on its associated transformation code from the `fred_indicator_mappings` dataset.

<div style="color:#FF7F50">

#### Transformation Function

</div>

The `modified_log_transform` function is designed to apply the appropriate transformation to each economic indicator in the dataset. This ensures that each indicator is processed according to its specific characteristics and the transformation code it is associated with.

<div style="color:#FF7F50">

#### Resulting Adjustments

</div>

After applying the transformations, we process the transformed data, dropping any initial rows containing `NaN` values to ensure a clean dataset for analysis. This  approach enhances our dataset's suitability for advanced statistical modeling, aligning our methodology with established standards and enabling meaningful comparisons and insights.

By adhering to these transformation standards, we effectively prepare our dataset for the rigorous analysis required to achieve our project goals, ensuring that the economic indicators are accurately represented.

<div style="color:#00BFFF">

## Correlation Analysis

</div>

<div style="color:#FF7F50">

### Objective

</div>

Our correlation analysis aims to uncover linear relationships between economic indicators and Personal Consumption Expenditures (PCE) without presuming the nature of these relationships. This is crucial for handling economic data characterized by non-linear trends and outliers.

<div style="color:#FF7F50">

### Methodology

</div>

- **Spearman's Rank Correlation:** We utilize Spearman's rank correlation for its non-parametric nature, adept at identifying linear relationships and robust against outliers and NaN values.
- **Key Objectives:**
  - **Identifying Influential Indicators:** Sort correlations from highest to lowest based on absolute values to pinpoint strong linear relationships with PCE.
  - **Navigating the Correlation Landscape:** View the magnitude and directionality of each relationship to understand how fluctuations in indicators resonate with PCE shifts.

<div style="color:#FF7F50">

### Implementation

</div>

- **Visualization Strategy:** We use horizontal bar plots, highlighting positive correlations in sky blue and negative correlations in coral, with a clear marker for zero correlation. This visual distinction helps underscore the directional influence of each indicator on PCE.
- **Analytical Precision:** By focusing on the top N positively and negatively correlated indicators, we streamline our investigation towards variables with substantial predictive value for PCE.

<div style="color:#FF7F50">

### Results

</div>

- **Labor and Housing Markets:** These indicators stand out among the top correlated variables, emphasizing their crucial role in consumer expenditure dynamics.
- **Correlation Strengths:** We observe moderate positive relationships (coefficients ranging from 0.39 to 0.55) and weak negative relationships (coefficients from -0.13 to -0.29) among the top indicators.

<div style="color:#00BFFF">

## Multicollinearity Analysis with Variance Inflation Factor (VIF)

</div>

<div style="color:#FF7F50">

### Overview

</div>

High multicollinearity among variables can obscure individual indicator impacts on PCE, making it crucial to assess and manage.

<div style="color:#FF7F50">

### Techniques

</div>

- **Circular Correlation Heatmap:** A visualization tool offering a comprehensive view of indicator interrelationships through hierarchical clustering of correlation matrices. It highlights clusters of closely correlated variables, aiding in multicollinearity detection.
- **Variance Inflation Factor (VIF) Analysis:** Quantifies the inflation in the variance of estimated regression coefficients due to intercorrelations among predictors. A VIF above 10 indicates significant multicollinearity.

<div style="color:#FF7F50">

### Observations and Strategic Steps Forward

</div>

- **Proxy Selection:** We prioritize proxies with strong correlations to PCE and unique insights, employing linear regression to assess predictive strength and examining seasonality and stationarity.
- **Dimension Reduction:** Utilizing techniques like Principal Component Analysis (PCA) to consolidate highly correlated variables into a manageable set of components, mitigating multicollinearity while enhancing model interpretability and efficiency.

<div style="color:#00BFFF">

## Linear Regression Analysis for PCE Determinants

</div>

<div style="color:#FF7F50">

### Objective

</div>

The primary goal is to utilize the R2 (coefficient of determination) metric to identify variables that significantly explain the variance in PCE, enabling us to pinpoint the most influential determinants.

<div style="color:#FF7F50">

### Methodical Approach

</div>

1. **Data Preparation:**
   - Exclusion of the dependent variable (PCE) from the pool of independent variables.
   - Data cleansing to eliminate rows with NaN or infinite values.
   - Model fitting involving linear regression models between each variable and PCE.

2. **Assessment of R2 Values:**
   - Generation of PCE predictions for each independent variable, followed by calculation of the R2 value to gauge explanatory power.
   - Higher R2 values indicate a stronger linear relationship and a higher degree of explained variance in PCE.

<div style="color:#FF7F50">

### Utilising R2 and Correlation Coefficients Together

</div>

An interactive scatterplot combining R2 values and correlation coefficients with PCE enhances our understanding, enabling strategic proxy selection for further analysis. This dual-metric approach allows for a nuanced understanding of each variable's influence on PCE.

<div style="color:#FF7F50">

### Why This Approach Is Beneficial

</div>

- Identifies key PCE drivers by combining R2 values and correlation coefficients, offering a comprehensive view of each variable's influence.
- Refines proxy selection, focusing on variables that provide significant insights into PCE dynamics.

<div style="color:#00BFFF">

## Proxy Selection and Analysis

</div>

<div style="color:#FF7F50">

### Defining Filtering Thresholds

</div>

Clear criteria based on correlation coefficients and R2 values help identify the most informative proxies for our model. Economic intuition also plays a crucial role in validating the logical connection of these proxies to PCE dynamics.

<div style="color:#FF7F50">

### Seasonality and Stationarity Assessment

</div>

- **Seasonality Assessment:** Utilizing Autocorrelation Function (ACF) analysis to identify and adjust for seasonal patterns within our dataset.
- **Stationarity Assessment:** Employing the Augmented Dickey-Fuller (ADF) test to confirm the stationarity of our series, ensuring the validity of our statistical models.

<div style="color:#FF7F50">

### Integration of Findings for Proxy Selection

</div>

By incorporating findings from seasonality, stationarity assessments, and correlation analysis, we refine our list of proxies, prioritizing indicators that are statistically sound and highly correlated with PCE.

<div style="color:#00BFFF">

## Addressing Multicollinearity with PCA

</div>

<div style="color:#FF7F50">

### Principal Component Analysis (PCA) Analysis

</div>

To tackle multicollinearity and enhance model performance, we implemented PCA for dimensionality reduction, transforming the dataset into a set of principal components used as new predictors in our regression model.

<div style="color:#FF7F50">

### Methodological Overview

</div>

1. **Data Preparation:** Ensuring the dataset is clean and missing values are appropriately handled.
2. **PCA Implementation:** Reducing dataset complexity to address multicollinearity and improve interpretability.
3. **Model Performance:** Evaluating the predictive accuracy using Mean Absolute Error (MAE) and Root Mean Squared Error (RMSE), confirming the effectiveness of our model.

<div style="color:#FF7F50">

### Model Insights

</div>

- **Scree Plot Analysis:** A Scree Plot helps identify the principal components that account for the most variance, guiding the selection of components for regression.
- **Regression Using Principal Components:** A Linear Regression model utilizing principal components as predictors to forecast PCE, enhancing model clarity and interpretability.

This final section encapsulates the thorough and strategic approach undertaken to identify, analyze, and model the determinants of PCE. Through meticulous data preparation, rigorous analysis, and sophisticated modeling techniques, this project offers valuable insights into consumer spending dynamics, laying a solid foundation for informed economic policy and strategy formulation.
