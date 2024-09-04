import pandas as pd
from unidecode import unidecode
import services.logging_service as log
from datetime import datetime
import json

def read_csv(csv):
    return pd.read_csv(csv)

def to_csv(data_frame: pd.DataFrame, path: str, index_param: bool = False):
    data_frame.to_csv(path, index = index_param)
    log.info(f"Dataset saved as {path}")

def insert_column_after_column(data_frame : pd.DataFrame, original_column : str ,column_to_insert: str):
    index = data_frame.columns.get_loc(original_column)
    insert_position = index + 1
    data_frame.insert(insert_position, column_to_insert, '')
    
    log.info(f"Function - insert_column_after_column - Done. \nAdded {column_to_insert} to the dataset ")

# Assuming log is already defined as log = logging.getLogger(__name__)

def generate_company_data_by_missing_feature(data_frame, expected_missing_feature, feature_list):
    # Filter out rows based on the specified column (expected_missing_feature) and conditions
    filtered_companies = data_frame[
        data_frame[expected_missing_feature].isnull() & 
        data_frame['company_name'].notnull()
    ]
    
    # List to hold the result
    result_list = []
    
    # Iterate through the filtered DataFrame rows
    for index, row in filtered_companies.iterrows():
        company_data = {'company_name': row['company_name']}
        
        # Add the Crunchbase URL by default
        if pd.notnull(row.get('permalink')):
            company_data['crunchbase_url'] = 'https://www.crunchbase.com' + row['permalink']
        else:
            company_data['crunchbase_url'] = None

        # Add selected features and their values for the row
        for feature in feature_list:
            if feature in row:
                company_data[feature] = row[feature]
            else:
                company_data[feature] = None  # Handle cases where feature might not exist

        result_list.append(company_data)
    
    log.info("generate_company_data_by_missing_feature - Done.")
    return result_list




def update_dataframe(data_frame: pd.DataFrame, value_to_update: str, column_to_update: str):
    try:
        # Convert value_to_update to JSON
        values_as_json = json.loads(value_to_update)
        
        # Iterate over each key-value pair and update the DataFrame
        for item in values_as_json:
            key = item['Key']
            value = item['Value']
            # Update the specified column where the company_name matches the key
            data_frame.loc[data_frame['company_name'] == key, column_to_update] = value

        log.info("Function - update_dataframe - Done.")
    except json.JSONDecodeError as e:
        log.error(f"Error decoding JSON: {e}")
        raise ValueError("Invalid JSON format passed to value_to_update")
    
    return data_frame

# Function to validate 'founded_year'
def validate_founded_year(year):
    current_year = datetime.now().year
    try:
        if 578 <= int(year) <= current_year:
            return int(year)
        else:
            return pd.NA 
    except ValueError:
        return pd.NA

# Function to clean and validate 'homepage_url'
def validate_homepage_url(url):
    if pd.notna(url):
        if url.startswith(('http://', 'https://')):
            return url
        else:
            return pd.NA
    else:
     return pd.NA

def clean_up_data_frame(data_frame: pd.DataFrame):
    # Drop empty rows
    data_frame.dropna(how='all', inplace=True)

    # Convert special characters in 'city' column
    data_frame['city'] = data_frame['city'].apply(lambda x: unidecode(x) if pd.notnull(x) else x)
    
    # Clean and standardize 'city' column
    data_frame['city'] = data_frame['city'].str.strip().str.title()

    # Set 'funding_total_usd' to NaN if the value is 0 or negative
    data_frame['funding_total_usd'] = data_frame['funding_total_usd'].apply(lambda x: pd.NA if x <= 0 else x)

    # Validate the 'founded_year' column
    data_frame['founded_year'] = data_frame['founded_year'].apply(validate_founded_year)

    # Validate and clean the 'homepage_url' column
    data_frame['homepage_url'] = data_frame['homepage_url'].apply(validate_homepage_url)


    log.info("Function - clean_up_data_frame - Done.")
    return data_frame