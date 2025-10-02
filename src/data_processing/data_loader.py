"""
Data Loader Module for Automotive Emissions and Fuel Efficiency Project
Handles loading and initial processing of multiple datasets
"""

import pandas as pd
import numpy as np
import requests
from io import StringIO
import warnings
warnings.filterwarnings('ignore')

class DataLoader:
    """Class to handle loading of automotive datasets"""
    
    def __init__(self):
        self.datasets = {}
        
    def load_uci_auto_mpg(self, local_path=None):
        """
        Load UCI Auto MPG dataset
        
        Parameters:
        local_path (str): Path to local file if available
        
        Returns:
        pd.DataFrame: Loaded dataset
        """
        # First try to load from downloaded file
        try:
            data = pd.read_csv('data/raw/uci_auto_mpg.csv')
            print(f"✓ Loaded UCI Auto MPG data from downloaded file: {data.shape}")
            self.datasets['uci_auto_mpg'] = data
            return data
        except Exception as e:
            print(f"Downloaded file not found, trying web source: {e}")
        
        if local_path:
            try:
                data = pd.read_csv(local_path)
                print(f"Loaded UCI Auto MPG data from local file: {data.shape}")
                return data
            except Exception as e:
                print(f"Error loading local file: {e}")
        
        # Load from UCI repository
        try:
            url = "https://archive.ics.uci.edu/ml/machine-learning-databases/auto-mpg/auto-mpg.data"
            response = requests.get(url)
            
            # Define column names as they're not in the data file
            columns = ['mpg', 'cylinders', 'displacement', 'horsepower', 
                      'weight', 'acceleration', 'model_year', 'origin', 'car_name']
            
            # Read the data
            data = pd.read_csv(StringIO(response.text), sep='\s+', names=columns)
            print(f"Loaded UCI Auto MPG data from web: {data.shape}")
            
            self.datasets['uci_auto_mpg'] = data
            return data
            
        except Exception as e:
            print(f"Error loading UCI Auto MPG data: {e}")
            return self._create_sample_auto_mpg_data()
    
    def _create_sample_auto_mpg_data(self):
        """Create sample data if online sources fail"""
        np.random.seed(42)
        n_samples = 398
        
        data = {
            'mpg': np.random.normal(23.5, 7.8, n_samples),
            'cylinders': np.random.choice([3, 4, 5, 6, 8], n_samples, p=[0.05, 0.45, 0.1, 0.25, 0.15]),
            'displacement': np.random.normal(194, 104, n_samples),
            'horsepower': np.random.normal(104, 38, n_samples),
            'weight': np.random.normal(2978, 849, n_samples),
            'acceleration': np.random.normal(15.5, 2.8, n_samples),
            'model_year': np.random.randint(70, 83, n_samples),
            'origin': np.random.choice([1, 2, 3], n_samples, p=[0.62, 0.19, 0.19]),
            'car_name': [f'vehicle_{i}' for i in range(n_samples)]
        }
        
        df = pd.DataFrame(data)
        # Ensure positive values where needed
        df['mpg'] = np.abs(df['mpg'])
        df['displacement'] = np.abs(df['displacement'])
        df['horsepower'] = np.abs(df['horsepower'])
        df['weight'] = np.abs(df['weight'])
        df['acceleration'] = np.abs(df['acceleration'])
        
        print("Created sample UCI Auto MPG data")
        return df
    
    def create_sample_epa_data(self):
        """Create sample EPA Fuel Economy data"""
        # Try to load from downloaded file first
        try:
            df = pd.read_csv('data/raw/epa_fuel_economy.csv')
            print(f"✓ Loaded EPA Fuel Economy data from downloaded file: {df.shape}")
            self.datasets['epa_fuel_economy'] = df
            self.loading_log.append("✓ EPA Fuel Economy data loaded from downloaded file")
            return df
        except Exception as e:
            print(f"Downloaded file not found, creating sample data: {e}")
        
        np.random.seed(42)
        n_samples = 1000
        
        makes = ['Toyota', 'Honda', 'Ford', 'Chevrolet', 'BMW', 'Mercedes', 'Audi', 'Volkswagen']
        fuel_types = ['Regular', 'Premium', 'Diesel', 'Electric']
        
        data = {
            'make': np.random.choice(makes, n_samples),
            'model': [f'Model_{i}' for i in range(n_samples)],
            'year': np.random.randint(2010, 2024, n_samples),
            'fuel_type': np.random.choice(fuel_types, n_samples, p=[0.6, 0.2, 0.15, 0.05]),
            'city_mpg': np.random.normal(25, 5, n_samples),
            'highway_mpg': np.random.normal(33, 6, n_samples),
            'combined_mpg': np.random.normal(28, 5, n_samples),
            'co2_emissions': np.random.normal(350, 100, n_samples),
            'engine_size': np.random.normal(2.4, 0.8, n_samples),
            'transmission_type': np.random.choice(['Manual', 'Automatic', 'CVT'], n_samples, p=[0.2, 0.6, 0.2])
        }
        
        df = pd.DataFrame(data)
        # Ensure positive values
        df['city_mpg'] = np.abs(df['city_mpg'])
        df['highway_mpg'] = np.abs(df['highway_mpg'])
        df['combined_mpg'] = np.abs(df['combined_mpg'])
        df['co2_emissions'] = np.abs(df['co2_emissions'])
        df['engine_size'] = np.abs(df['engine_size'])
        
        print(f"Created sample EPA data: {df.shape}")
        self.datasets['epa_fuel_economy'] = df
        return df
    
    def create_sample_vehicle_dataset(self):
        """Create sample Vehicle dataset similar to Kaggle format"""
        # Try to load from downloaded file first
        try:
            df = pd.read_csv('data/raw/vehicle_dataset.csv')
            print(f"✓ Loaded Vehicle dataset from downloaded file: {df.shape}")
            self.datasets['vehicle_dataset'] = df
            self.loading_log.append("✓ Vehicle dataset loaded from downloaded file")
            return df
        except Exception as e:
            print(f"Downloaded file not found, creating sample data: {e}")
        
        np.random.seed(42)
        n_samples = 2000
        
        makes = ['Toyota', 'Honda', 'Ford', 'Chevrolet', 'BMW', 'Mercedes', 'Audi', 'Volkswagen', 'Nissan', 'Hyundai']
        body_types = ['Sedan', 'SUV', 'Hatchback', 'Coupe', 'Wagon', 'Convertible']
        
        data = {
            'make': np.random.choice(makes, n_samples),
            'model': [f'Model_{i}' for i in range(n_samples)],
            'year': np.random.randint(2000, 2024, n_samples),
            'body_type': np.random.choice(body_types, n_samples),
            'engine_capacity': np.random.normal(2.2, 0.9, n_samples),
            'fuel_efficiency': np.random.normal(15, 4, n_samples),  # km/l
            'price': np.random.exponential(25000, n_samples),
            'mileage': np.random.exponential(50000, n_samples),
            'safety_rating': np.random.choice([3, 4, 5], n_samples, p=[0.2, 0.5, 0.3])
        }
        
        df = pd.DataFrame(data)
        # Ensure positive values
        df['engine_capacity'] = np.abs(df['engine_capacity'])
        df['fuel_efficiency'] = np.abs(df['fuel_efficiency'])
        df['price'] = np.abs(df['price'])
        df['mileage'] = np.abs(df['mileage'])
        
        print(f"Created sample Vehicle dataset: {df.shape}")
        self.datasets['vehicle_dataset'] = df
        return df
    
    def load_all_datasets(self):
        """Load all datasets"""
        print("Loading all datasets...")
        
        # Load UCI Auto MPG
        uci_data = self.load_uci_auto_mpg()
        
        # Create sample EPA data
        epa_data = self.create_sample_epa_data()
        
        # Create sample Vehicle data
        vehicle_data = self.create_sample_vehicle_dataset()
        
        return {
            'uci_auto_mpg': uci_data,
            'epa_fuel_economy': epa_data,
            'vehicle_dataset': vehicle_data
        }
    
    def save_datasets(self, data_dict, output_dir='../data/raw'):
        """Save datasets to CSV files"""
        import os
        os.makedirs(output_dir, exist_ok=True)
        
        for name, df in data_dict.items():
            filepath = os.path.join(output_dir, f'{name}.csv')
            df.to_csv(filepath, index=False)
            print(f"Saved {name} to {filepath}")

if __name__ == "__main__":
    loader = DataLoader()
    datasets = loader.load_all_datasets()
    
    # Display basic info about each dataset
    for name, df in datasets.items():
        print(f"\n{name.upper()}:")
        print(f"Shape: {df.shape}")
        print(f"Columns: {list(df.columns)}")
        print(f"Memory usage: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")