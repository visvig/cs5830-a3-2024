import pandas as pd
from sklearn.metrics import r2_score
import os

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Base directory for the cs5830 folder

# Path to the extracted csv files
extracted_folder = os.path.join(base_dir, 'outputs')  # Path to output folder

# Path to the processed csv files
processed_folder = os.path.join(base_dir, 'outputs_process')  # Path to output folder

output_folder = os.path.join(base_dir, 'results')  # Path to output folder

# Read the extracted csv files
extracted_files = os.listdir(extracted_folder)
print(extracted_files)
extracted_data = pd.concat([pd.read_csv(os.path.join(extracted_folder, file)) for file in extracted_files if file.endswith('.csv')])
print(extracted_data)

# Read the processed csv files
processed_files = os.listdir(processed_folder)
print(processed_files)
processed_data = pd.concat([pd.read_csv(os.path.join(processed_folder, file)) for file in processed_files if file.endswith('.csv')])

# Remove rows with NaN values from extracted_data and processed_data
extracted_data = extracted_data.dropna()
processed_data = processed_data.dropna()

print(extracted_data)
print(processed_data)

extracted_data['DATE'] = pd.to_datetime(extracted_data['DATE'])
print(extracted_data)

extracted_data['MonthlyTotalLiquidPrecipitation'] = pd.to_numeric(extracted_data['MonthlyTotalLiquidPrecipitation'], errors='coerce')
extracted_data['MonthlyMeanTemperature'] = pd.to_numeric(extracted_data['MonthlyMeanTemperature'], errors='coerce')

processed_data['DATE'] = pd.to_datetime(processed_data['DATE'])
print(processed_data)

# Calculate the R-squared value for MonthlyTotalLiquidPrecipitation and MonthlyMeanTemperature for matching station. use DATE as independent variable
r2_values = []
for station in extracted_data['STATION'].unique():
    print("station:", station)
    extracted_station_data = extracted_data[extracted_data['STATION'] == station]
    print(extracted_station_data)
    processed_station_data = processed_data[processed_data['STATION'] == station]
    print(processed_station_data)
    
    merged_data = pd.merge(extracted_station_data, processed_station_data, on='DATE', suffixes=('_extracted', '_processed'))
    print(merged_data)
    print(merged_data['DATE'], merged_data['MonthlyTotalLiquidPrecipitation_extracted'], merged_data['MonthlyTotalLiquidPrecipitation_processed'])
    print(merged_data['DATE'], merged_data['MonthlyMeanTemperature_extracted'], merged_data['MonthlyMeanTemperature_processed'])
    
    r2_precipitation = r2_score(merged_data['MonthlyTotalLiquidPrecipitation_extracted'], merged_data['MonthlyTotalLiquidPrecipitation_processed'])
    r2_temperature = r2_score(merged_data['MonthlyMeanTemperature_extracted'], merged_data['MonthlyMeanTemperature_processed'])
    
    r2_values.append({'STATION': station, 'R2_Precipitation': r2_precipitation, 'R2_Temperature': r2_temperature})

print(r2_values)

# if R2 value is greater than 0.9 for both MonthlyTotalLiquidPrecipitation and MonthlyMeanTemperature for a STATION, then print that STATION is C (Consisitent)

# Export evaluation results to a text file
output_file = os.path.join(output_folder, 'evaluation_results.txt')
with open(output_file, 'w') as f:
    for r2_value in r2_values:
        if r2_value['R2_Precipitation'] > 0.9 and r2_value['R2_Temperature'] > 0.9:
            f.write(f"{r2_value['STATION']} C\n")
        else:
            f.write(f"{r2_value['STATION']} I\n")


