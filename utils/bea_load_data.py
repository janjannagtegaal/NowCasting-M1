import pandas as pd


def load_and_preprocess_gdp_data(file_path):
    """
    Loads and preprocesses the GDP data from a CSV file.
    Args:file_path (str): The path to the CSV file containing GDP data.
    Returns:pandas.DataFrame: Preprocessed GDP data.
    """

    # Load the data with specified rows to skip and number of rows to read
    pce_df = pd.read_csv(file_path, skiprows=3, nrows=28)

    # Drop the first column (unnecessary or identifier column)
    pce_df.drop(pce_df.columns[0], axis=1, inplace=True)

    # Rename the first column as 'description'
    pce_df.rename(columns={pce_df.columns[0]: "description"}, inplace=True)

    # Remove any characters after (and including) the "." in column names
    pce_df.columns = pce_df.columns.str.replace(r"\..*", "", regex=True)

    # Concatenate the column names with the first row values, handling NaNs
    pce_df.columns = pce_df.columns + " " + pce_df.iloc[0].fillna("")

    # Drop the first row as it's now part of the column names
    pce_df.drop(pce_df.index[0], inplace=True)

    # Reset the index of the DataFrame
    pce_df.reset_index(drop=True, inplace=True)

    # Correct any trailing space issues in the 'description' column name
    pce_df.rename(columns=lambda x: x.strip(), inplace=True)

    return pce_df


######################################################################


def create_structured_description(pce_df):
    """
    Process a DataFrame to create a structured description column.
    This function takes a DataFrame with a 'description' column and adds structure to it
    based on indentation levels, indicating hierarchical relationships.
    """

    # Function to determine the indentation level (number of leading spaces)
    def indentation_level(s):
        """Return the number of leading spaces in a string, indicating the indentation level."""
        return len(s) - len(s.lstrip())

    # Apply the function to find indentation levels
    pce_df["indentation"] = pce_df["description"].apply(indentation_level)

    # Initialize an empty list to store the new structured names
    structured_names = []
    current_parent = ""
    current_subparent = ""

    # Iterate through the DataFrame to construct the hierarchical names
    for index, row in pce_df.iterrows():
        if row["indentation"] == 0:
            name = row["description"].strip()
            current_parent = name
        elif row["indentation"] == 4:
            name = f"{current_parent} : {row['description'].strip()}"
            current_subparent = row["description"].strip()
        elif row["indentation"] == 8:
            name = (
                f"{current_parent} : {current_subparent} : {row['description'].strip()}"
            )
        else:
            name = row["description"].strip()

        structured_names.append(name)

    # Assigning the structured names to the 'description' column
    pce_df["description"] = structured_names

    # Dropping the 'indentation' column as it's no longer needed
    pce_df.drop("indentation", axis=1, inplace=True)

    return pce_df


######################################################################


def create_short_description(pce_df):
    """
    Create a column 'short_description' in the gdp_df DataFrame with abbreviated descriptions.
    Parameters:gdp_df (DataFrame): A DataFrame containing GDP data with a column 'description'.
    Returns:DataFrame: The modified DataFrame including a new 'short_description' column.
    """

    def abbreviate_description(desc):

        # Define a mapping from full descriptions to their abbreviations
        abbreviations = {
            "Gross domestic product": "GDP",
            "Personal consumption expenditures": "PCE",
            "Gross private domestic investment": "GPDI",
            "Net exports of goods and services": "NXGS",
            "Government consumption expenditures and gross investment": "GCEGI",
        }

        # Split the description into parts and abbreviate each part
        parts = desc.split(" : ")
        abbreviated_parts = [abbreviations.get(part, part) for part in parts]

        # Join the abbreviated parts and replace spaces with underscores
        abrev_descr = "_".join(abbreviated_parts).replace(" ", "_")

        # remove all leading "_" characters
        abrev_descr = abrev_descr.lstrip("_")

        # remove leading and trailing spaces from the description column
        abrev_descr = abrev_descr.strip()

        return abrev_descr

    # Apply the abbreviation function to each description
    pce_df["short_description"] = pce_df["description"].apply(abbreviate_description)
    pce_df["description"] = pce_df["description"].str.lstrip(" :").str.strip()

    # Insert the new column 'short_description' right after the 'description' column
    description_index = pce_df.columns.get_loc("description")
    pce_df.insert(
        description_index + 1, "short_description", pce_df.pop("short_description")
    )

    # drop the 'description' column
    pce_df.drop("description", axis=1, inplace=True)

    # move last row to after 1st row fo readability
    last_row = pce_df.iloc[-1].copy()
    pce_df = pce_df.iloc[:-1]
    pce_df = pd.concat(
        [pce_df.iloc[:1], last_row.to_frame().T, pce_df.iloc[1:]]
    ).reset_index(drop=True)

    return pce_df


######################################################################


def transform_date_formats(pce_df):
    # Step 1: Extract only non-date columns
    non_date_columns = pce_df.columns[:1]

    # Step 2: Extract and transform date columns
    date_columns = pce_df.columns[1:]  # Non-Date columns start from the 2nd column

    # Function to convert quarter to the format 'YYYYQX'
    def quarter_to_yyyyqx(q):
        year, quarter = q.split(" Q")
        return f"{year}Q{quarter}"

    # Apply this function to each of the date columns
    transformed_date_columns = [quarter_to_yyyyqx(col) for col in date_columns]

    # Step 3: Combine the columns back together
    pce_df.columns = list(non_date_columns) + transformed_date_columns

    # Transpose the dataset for easier manipulation (columns become rows)
    pce_df = pce_df.set_index("short_description").transpose()

    # Convert all columns to numeric
    for col in pce_df.columns:
        pce_df[col] = pd.to_numeric(pce_df[col], errors="coerce")

    return pce_df


######################################################################
