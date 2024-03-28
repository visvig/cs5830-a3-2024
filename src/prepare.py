import os
import pandas as pd

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Base directory for the cs5830 folder
data_folder = os.path.join(base_dir, 'data')  # Path to data folder
output_folder = os.path.join(base_dir, 'outputs')  # Path to output folder

# Create the output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Get the list of CSV files in the data folder
csv_files = [file for file in os.listdir(data_folder) if file.endswith(".csv")]

# Iterate over each CSV file
for csv_file in csv_files:
    # Read the CSV file
    df = pd.read_csv(os.path.join(data_folder, csv_file), dtype=object)
    
    # Extract the desired columns
    extracted_columns = df[["STATION", "DATE", "MonthlyTotalLiquidPrecipitation", "MonthlyMeanTemperature"]]
    
    # Save the extracted columns to a new CSV file
    output_file = os.path.join(output_folder, f"extracted_{csv_file}")
    extracted_columns.to_csv(output_file, index=False)