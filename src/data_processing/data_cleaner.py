"""
Data Cleaning Module for Automotive Emissions and Fuel Efficiency Project
Handles data preprocessing, cleaning, and transformation
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.impute import SimpleImputer, KNNImputer
import warnings
warnings.filterwarnings('ignore')

class DataCleaner:
    """Class to handle data cleaning and preprocessing operations"""
    
    def __init__(self):
        self.scalers = {}
        self.encoders = {}
        self.imputers = {}
        
    def analyze_data_quality(self, df, dataset_name):
        """
        Analyze data quality and generate quality report
        
        Parameters:
        df (pd.DataFrame): Dataset to analyze
        dataset_name (str): Name of the dataset
        
        Returns:
        dict: Data quality report
        """
        quality_report = {
            'dataset_name': dataset_name,
            'shape': df.shape,
            'memory_usage': df.memory_usage(deep=True).sum() / 1024**2,
            'missing_values': {},
            'duplicates': df.duplicated().sum(),
            'numeric_columns': list(df.select_dtypes(include=[np.number]).columns),
            'categorical_columns': list(df.select_dtypes(include=['object']).columns),
            'data_types': dict(df.dtypes),
            'outliers': {},
            'summary_stats': {}
        }
        
        # Analyze missing values
        for col in df.columns:
            missing_count = df[col].isnull().sum()
            missing_percentage = (missing_count / len(df)) * 100
            quality_report['missing_values'][col] = {
                'count': missing_count,
                'percentage': missing_percentage
            }
        
        # Analyze outliers for numeric columns
        for col in quality_report['numeric_columns']:
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            
            outliers = df[(df[col] < lower_bound) | (df[col] > upper_bound)]
            quality_report['outliers'][col] = {
                'count': len(outliers),
                'percentage': (len(outliers) / len(df)) * 100,
                'lower_bound': lower_bound,
                'upper_bound': upper_bound
            }
        
        # Summary statistics
        quality_report['summary_stats'] = df.describe().to_dict()
        
        return quality_report
    
    def clean_uci_auto_mpg(self, df):
        """
        Clean UCI Auto MPG dataset
        
        Parameters:
        df (pd.DataFrame): Raw UCI Auto MPG data
        
        Returns:
        pd.DataFrame: Cleaned dataset
        """
        df_clean = df.copy()
        
        # Handle missing values represented as '?'
        df_clean = df_clean.replace('?', np.nan)
        
        # Convert numeric columns
        numeric_cols = ['mpg', 'cylinders', 'displacement', 'horsepower', 'weight', 'acceleration', 'model_year']
        for col in numeric_cols:
            if col in df_clean.columns:
                df_clean[col] = pd.to_numeric(df_clean[col], errors='coerce')
        
        # Handle missing horsepower values with median imputation
        if 'horsepower' in df_clean.columns:
            median_hp = df_clean['horsepower'].median()
            df_clean['horsepower'].fillna(median_hp, inplace=True)
        
        # Remove duplicate rows
        df_clean = df_clean.drop_duplicates()
        
        # Handle outliers using IQR method
        for col in numeric_cols:
            if col in df_clean.columns:
                Q1 = df_clean[col].quantile(0.25)
                Q3 = df_clean[col].quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - 1.5 * IQR
                upper_bound = Q3 + 1.5 * IQR
                
                # Cap outliers instead of removing them
                df_clean[col] = df_clean[col].clip(lower=lower_bound, upper=upper_bound)
        
        # Create derived features
        if all(col in df_clean.columns for col in ['weight', 'horsepower']):
            df_clean['power_to_weight_ratio'] = df_clean['horsepower'] / df_clean['weight']
        
        if 'model_year' in df_clean.columns:
            df_clean['vehicle_age'] = 2024 - (1900 + df_clean['model_year'])
        
        # Encode categorical variables
        if 'origin' in df_clean.columns:
            origin_mapping = {1: 'USA', 2: 'Europe', 3: 'Japan'}
            df_clean['origin_name'] = df_clean['origin'].map(origin_mapping)
        
        print(f"UCI Auto MPG cleaning completed. Shape: {df.shape} -> {df_clean.shape}")
        return df_clean
    
    def clean_epa_fuel_economy(self, df):
        """
        Clean EPA Fuel Economy dataset
        
        Parameters:
        df (pd.DataFrame): Raw EPA data
        
        Returns:
        pd.DataFrame: Cleaned dataset
        """
        df_clean = df.copy()
        
        # Remove rows with missing critical values
        critical_cols = ['city_mpg', 'highway_mpg', 'combined_mpg']
        df_clean = df_clean.dropna(subset=critical_cols)
        
        # Handle negative or zero MPG values
        for col in critical_cols:
            df_clean = df_clean[df_clean[col] > 0]
        
        # Standardize fuel type names
        if 'fuel_type' in df_clean.columns:
            fuel_type_mapping = {
                'regular': 'Regular',
                'premium': 'Premium',
                'diesel': 'Diesel',
                'electric': 'Electric'
            }
            df_clean['fuel_type'] = df_clean['fuel_type'].str.lower().map(fuel_type_mapping).fillna(df_clean['fuel_type'])
        
        # Handle CO2 emissions - impute missing values
        if 'co2_emissions' in df_clean.columns:
            # Use KNN imputation for CO2 emissions based on MPG values
            features_for_imputation = ['city_mpg', 'highway_mpg', 'combined_mpg', 'engine_size']
            available_features = [col for col in features_for_imputation if col in df_clean.columns]
            
            if len(available_features) > 1:
                imputer = KNNImputer(n_neighbors=5)
                df_clean[['co2_emissions'] + available_features] = imputer.fit_transform(
                    df_clean[['co2_emissions'] + available_features]
                )
        
        # Create efficiency categories
        if 'combined_mpg' in df_clean.columns:
            df_clean['efficiency_category'] = pd.cut(
                df_clean['combined_mpg'],
                bins=[0, 20, 30, 40, float('inf')],
                labels=['Low', 'Medium', 'High', 'Very High']
            )
        
        # Remove duplicates
        df_clean = df_clean.drop_duplicates()
        
        print(f"EPA Fuel Economy cleaning completed. Shape: {df.shape} -> {df_clean.shape}")
        return df_clean
    
    def clean_vehicle_dataset(self, df):
        """
        Clean Vehicle dataset
        
        Parameters:
        df (pd.DataFrame): Raw Vehicle data
        
        Returns:
        pd.DataFrame: Cleaned dataset
        """
        df_clean = df.copy()
        
        # Handle missing values in numeric columns
        numeric_cols = ['engine_capacity', 'fuel_efficiency', 'price', 'mileage']
        for col in numeric_cols:
            if col in df_clean.columns:
                if df_clean[col].isnull().sum() > 0:
                    median_value = df_clean[col].median()
                    df_clean[col].fillna(median_value, inplace=True)
        
        # Handle unrealistic values
        if 'price' in df_clean.columns:
            # Remove vehicles with price less than $1000 or more than $500,000
            df_clean = df_clean[(df_clean['price'] >= 1000) & (df_clean['price'] <= 500000)]
        
        if 'mileage' in df_clean.columns:
            # Remove vehicles with unrealistic mileage (negative or more than 500,000)
            df_clean = df_clean[(df_clean['mileage'] >= 0) & (df_clean['mileage'] <= 500000)]
        
        if 'fuel_efficiency' in df_clean.columns:
            # Remove vehicles with unrealistic fuel efficiency
            df_clean = df_clean[(df_clean['fuel_efficiency'] > 0) & (df_clean['fuel_efficiency'] <= 50)]
        
        # Standardize make names
        if 'make' in df_clean.columns:
            df_clean['make'] = df_clean['make'].str.title().str.strip()
        
        # Create vehicle age
        if 'year' in df_clean.columns:
            df_clean['vehicle_age'] = 2024 - df_clean['year']
        
        # Create price categories
        if 'price' in df_clean.columns:
            df_clean['price_category'] = pd.cut(
                df_clean['price'],
                bins=[0, 15000, 30000, 50000, float('inf')],
                labels=['Budget', 'Mid-range', 'Premium', 'Luxury']
            )
        
        # Remove duplicates
        df_clean = df_clean.drop_duplicates()
        
        print(f"Vehicle dataset cleaning completed. Shape: {df.shape} -> {df_clean.shape}")
        return df_clean
    
    def normalize_features(self, df, columns_to_normalize=None):
        """
        Normalize numeric features using StandardScaler
        
        Parameters:
        df (pd.DataFrame): Dataset to normalize
        columns_to_normalize (list): List of columns to normalize
        
        Returns:
        pd.DataFrame: Dataset with normalized features
        """
        df_normalized = df.copy()
        
        if columns_to_normalize is None:
            columns_to_normalize = df.select_dtypes(include=[np.number]).columns
        
        scaler = StandardScaler()
        df_normalized[columns_to_normalize] = scaler.fit_transform(df_normalized[columns_to_normalize])
        
        # Store scaler for future use
        self.scalers['features'] = scaler
        
        return df_normalized
    
    def encode_categorical_features(self, df, categorical_columns=None):
        """
        Encode categorical features
        
        Parameters:
        df (pd.DataFrame): Dataset with categorical features
        categorical_columns (list): List of categorical columns to encode
        
        Returns:
        pd.DataFrame: Dataset with encoded features
        """
        df_encoded = df.copy()
        
        if categorical_columns is None:
            categorical_columns = df.select_dtypes(include=['object']).columns
        
        for col in categorical_columns:
            if col in df.columns and df[col].dtype == 'object':
                encoder = LabelEncoder()
                df_encoded[f'{col}_encoded'] = encoder.fit_transform(df[col].astype(str))
                self.encoders[col] = encoder
        
        return df_encoded
    
    def generate_cleaning_report(self, original_df, cleaned_df, dataset_name):
        """
        Generate a comprehensive cleaning report
        
        Parameters:
        original_df (pd.DataFrame): Original dataset
        cleaned_df (pd.DataFrame): Cleaned dataset
        dataset_name (str): Name of the dataset
        
        Returns:
        dict: Cleaning report
        """
        report = {
            'dataset_name': dataset_name,
            'original_shape': original_df.shape,
            'cleaned_shape': cleaned_df.shape,
            'rows_removed': original_df.shape[0] - cleaned_df.shape[0],
            'removal_percentage': ((original_df.shape[0] - cleaned_df.shape[0]) / original_df.shape[0]) * 100,
            'original_missing_values': original_df.isnull().sum().sum(),
            'cleaned_missing_values': cleaned_df.isnull().sum().sum(),
            'original_duplicates': original_df.duplicated().sum(),
            'cleaned_duplicates': cleaned_df.duplicated().sum(),
            'new_features_created': len(cleaned_df.columns) - len(original_df.columns)
        }
        
        return report

if __name__ == "__main__":
    # Example usage
    from data_loader import DataLoader
    
    loader = DataLoader()
    datasets = loader.load_all_datasets()
    
    cleaner = DataCleaner()
    
    # Clean each dataset
    cleaned_datasets = {}
    cleaning_reports = {}
    
    for name, df in datasets.items():
        print(f"\nCleaning {name}...")
        
        if name == 'uci_auto_mpg':
            cleaned_df = cleaner.clean_uci_auto_mpg(df)
        elif name == 'epa_fuel_economy':
            cleaned_df = cleaner.clean_epa_fuel_economy(df)
        elif name == 'vehicle_dataset':
            cleaned_df = cleaner.clean_vehicle_dataset(df)
        else:
            cleaned_df = df.copy()
        
        cleaned_datasets[name] = cleaned_df
        cleaning_reports[name] = cleaner.generate_cleaning_report(df, cleaned_df, name)
    
    # Display cleaning reports
    for name, report in cleaning_reports.items():
        print(f"\nCleaning Report for {name}:")
        print(f"Original shape: {report['original_shape']}")
        print(f"Cleaned shape: {report['cleaned_shape']}")
        print(f"Rows removed: {report['rows_removed']} ({report['removal_percentage']:.2f}%)")
        print(f"Missing values: {report['original_missing_values']} -> {report['cleaned_missing_values']}")
        print(f"New features created: {report['new_features_created']}")