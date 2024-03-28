import pandas as pd
import os


# Define the input and output file paths
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Base directory for the cs5830 folder
input_folder = os.path.join(base_dir, 'data')  # Path to input folder
output_folder = os.path.join(base_dir, 'outputs_process')  # Path to output folder

if not os.path.exists(output_folder):
    os.makedirs(output_folder, exist_ok=True)


# Get a list of all CSV files in the input folder
csv_files = [file for file in os.listdir(input_folder) if file.endswith('.csv')]

# Process each CSV file
for file in csv_files:
    # Read the CSV file into a DataFrame
    df = pd.read_csv(os.path.join(input_folder, file), dtype=object)
    
    # Extract the required columns
    df = df[['STATION', 'DATE', 'DailyPrecipitation', 'DailyAverageDryBulbTemperature']]
    
    # Convert the 'DATE' column to datetime format
    df['DATE'] = pd.to_datetime(df['DATE'])

    df['DailyPrecipitation'] = pd.to_numeric(df['DailyPrecipitation'], errors='coerce')
    df['DailyAverageDryBulbTemperature'] = pd.to_numeric(df['DailyAverageDryBulbTemperature'], errors='coerce')

    
    # Add new columns for MonthlyMeanTemperature and MonthlyTotalLiquidPrecipitation
    df['MonthlyMeanTemperature'] = df.groupby(df['DATE'].dt.month)['DailyAverageDryBulbTemperature'].transform('mean')
    df['MonthlyTotalLiquidPrecipitation'] = df.groupby(df['DATE'].dt.month)['DailyPrecipitation'].transform('sum')
    
    # Filter the DataFrame to keep only the last DATE timestamp of each month
    df = df[df['DATE'] == df.groupby(df['DATE'].dt.to_period('M'))['DATE'].transform('max')]
    
    # Create the output file path
    output_file = os.path.join(output_folder, f'processed_{file}')
    
    # Save the processed DataFrame to a new CSV file
    df.to_csv(output_file, index=False)