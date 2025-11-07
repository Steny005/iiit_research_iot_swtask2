import pandas as pd
import ast
import os
from sqlalchemy import create_engine
import numpy as np

# --- CONFIGURATION ---
DATA_FILE = 'iot_dataset.csv'
MAPPING_FILE = 'iot_dataset_mapping.csv'

# --- !!! IMPORTANT: UPDATE THIS LINE !!! ---
# Format: 'postgresql://username:password@hostname:port/database_name'
# Default:  'postgresql://postgres:YOUR_PASSWORD@localhost:5432/iot_db'
DB_URL = 'postgresql://postgres:chiNNu2005@localhost:5432/iot_db'
# --- END CONFIGURATION ---

def get_column_mapping():
    """Loads the CSV mapping file into a usable dictionary."""
    mapping_df = pd.read_csv(MAPPING_FILE)
    column_mapping = {}
    for _, row in mapping_df.iterrows():
        try:
            column_mapping[row['value_col']] = ast.literal_eval(row['original_column'])
        except Exception:
            column_mapping[row['value_col']] = {}
    return column_mapping

def process_vertical(data_df, vertical_name, column_mapping):
    """
    Filters and processes the DataFrame for a single vertical.
    """
    print(f"Processing vertical: {vertical_name}...")
    
    # 1. Create the renaming map for this vertical
    rename_map = {}
    all_mapped_columns = []
    for i in range(1, 13):
        value_col = f'value {i}'
        sensor_name = column_mapping.get(value_col, {}).get(vertical_name)
        
        # Only add if the sensor name is valid (not empty string)
        if sensor_name:
            rename_map[value_col] = sensor_name
            all_mapped_columns.append(value_col)
    
    if not rename_map:
        print(f"Warning: No valid sensor mappings found for vertical {vertical_name}. Skipping.")
        return None

    # 2. Filter the DataFrame
    vertical_df = data_df[data_df['type'] == vertical_name].copy()

    # 3. Select only the columns we need
    # We want node_id, created_at, and all the 'value X' columns
    columns_to_keep = ['node_id', 'created_at'] + all_mapped_columns
    
    # Ensure all columns exist before trying to select
    columns_to_keep = [col for col in columns_to_keep if col in vertical_df.columns]
    
    processed_df = vertical_df[columns_to_keep]

    # 4. Rename 'value X' columns to sensor names (e.g., 'pm25')
    processed_df = processed_df.rename(columns=rename_map)
    
    # 5. Handle NaNs: Replace pandas NaN with None (which becomes NULL in SQL)
    # Also convert timestamps to datetime objects for SQL
    processed_df = processed_df.astype(object).where(pd.notna(processed_df), None)
    processed_df['created_at'] = pd.to_datetime(processed_df['created_at'])

    print(f"Finished processing {vertical_name}. Found {len(processed_df)} records.")
    return processed_df

def main():
    print("Starting data loading script...")
    
    # 1. Check for files
    if not os.path.exists(DATA_FILE) or not os.path.exists(MAPPING_FILE):
        print(f"Error: Required file not found. Make sure '{DATA_FILE}' and '{MAPPING_FILE}' are in this directory.")
        return

    # 2. Create database connection engine
    try:
        engine = create_engine(DB_URL)
        with engine.connect() as conn:
            print("Successfully connected to PostgreSQL.")
    except Exception as e:
        print(f"Error: Could not connect to database. Check DB_URL and ensure PostgreSQL is running.")
        print(f"Details: {e}")
        return

    # 3. Load and process data
    print("Loading mapping file...")
    column_mapping = get_column_mapping()
    
    print(f"Loading main data file '{DATA_FILE}' (this may take a moment)...")
    data_df = pd.read_csv(DATA_FILE)
    
    verticals = data_df['type'].unique() # ['AQ', 'WF', 'SL']
    
    # 4. Loop, process, and insert
    for vertical in verticals:
        if vertical not in ['AQ', 'WF', 'SL']: # Ignore any other types
            continue
            
        table_name = f"{vertical.lower()}_data" # e.g., 'aq_data'
        
        # Process the data for this vertical
        processed_df = process_vertical(data_df, vertical, column_mapping)
        
        if processed_df is not None and not processed_df.empty:
            print(f"Inserting data into table '{table_name}'...")
            try:
                # Use pandas.to_sql to efficiently insert
                # 'replace' will drop the table first if it exists and create a new one
                # 'append' would add to it. 'replace' is safer for re-running the script.
                processed_df.to_sql(
                    table_name,
                    con=engine,
                    if_exists='replace',
                    index=False
                )
                print(f"Successfully loaded data into '{table_name}'.")
            except Exception as e:
                print(f"Error inserting data into '{table_name}'.")
                print(f"Details: {e}")
        else:
            print(f"No data to insert for vertical {vertical}.")
            
    print("Data loading script finished.")

if __name__ == "__main__":
    main()