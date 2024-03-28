import requests
import yaml
from bs4 import BeautifulSoup
import os
import random

# Paths setup
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Base directory for the cs5830 folder
params_path = os.path.join(base_dir, 'params', 'params.yaml')  # Path to params.yaml
data_dir = os.path.join(base_dir, 'data')  # Path to data folder

# Load parameters from params.yaml
with open(params_path, 'r') as file:
    params = yaml.safe_load(file)

n_locs = params['n_locs']
year = params['year']
directory_url = f'https://www.ncei.noaa.gov/data/local-climatological-data/access/{year}/'

# Ensure the data folder exists
if not os.path.exists(data_dir):
    os.makedirs(data_dir)

# Get the directory page content
response = requests.get(directory_url)
soup = BeautifulSoup(response.text, 'html.parser')

# Find all CSV file links
csv_links = [link.get('href') for link in soup.find_all('a') if link.get('href').endswith('.csv')]
print(csv_links)

# Download the specified number of CSV files starting with 9999999 because they are most likely to contain monthly data
random_csv_links = [link for link in csv_links if link.startswith('9999999')]
random_csv_links = random.sample(random_csv_links, n_locs)

for csv_link in random_csv_links:
    csv_url = directory_url + csv_link
    csv_response = requests.get(csv_url)
    filename = os.path.join(data_dir, csv_link.split('/')[-1])
    with open(filename, 'wb') as f:
        f.write(csv_response.content)
    print(f'Downloaded file: {filename}')
