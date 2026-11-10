"""
Phase II Analysis with Real Datasets
Automotive Industry: Vehicle Emissions and Fuel Efficiency Optimization
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

# Import our modules
import sys
import os
sys.path.append('src')

from data_processing.data_loader import DataLoader
from data_processing.data_cleaner import DataCleaner

def run_phase_ii_analysis():
    """Run complete Phase II analysis with real datasets"""
    
    print("="*80)
    print("PHASE II ANALYSIS - REAL AUTOMOTIVE DATASETS")
    print("="*80)
    print("Student: Hrishikesh M (22BCE0422)")
    print("Professor: Kumar K")
    print("Date: September 30, 2025")
    print("="*80)
    
    # 1. Load Real Datasets
    print("\nSTEP 1: Loading Real Datasets")
    print("-" * 50)
    
    loader = DataLoader()
    datasets = loader.load_all_datasets()
    
    # 2. Initial Data Exploration
    print("\nSTEP 2: Initial Data Exploration")
    print("-" * 50)
    
    for dataset_name, df in datasets.items():
        print(f"\n{dataset_name.upper().replace('_', ' ')} DATASET:")
        print(f"  Shape: {df.shape}")
        print(f"  Columns: {list(df.columns)}")
        print(f"  Memory Usage: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
        print(f"  Missing Values: {df.isnull().sum().sum()}")
        print(f"  Data Types: {df.dtypes.value_counts().to_dict()}")
        
        # Show sample data
        print(f"  Sample Data:")
        print(df.head(3).to_string())
        
        # Basic statistics for numeric columns
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) > 0:
            print(f"  Numeric Columns Summary:")
            for col in numeric_cols[:3]:  # Show first 3 numeric columns
                print(f"    {col}: Mean={df[col].mean():.2f}, Std={df[col].std():.2f}, Range=({df[col].min():.1f}, {df[col].max():.1f})")
    
    # 3. Data Quality Assessment
    print("\nSTEP 3: Data Quality Assessment")
    print("-" * 50)
    
    quality_scores = {}
    for dataset_name, df in datasets.items():
        print(f"\n{dataset_name.upper().replace('_', ' ')} QUALITY ASSESSMENT:")
        
        # Calculate quality metrics
        total_cells = df.shape[0] * df.shape[1]
        missing_cells = df.isnull().sum().sum()
        completeness = ((total_cells - missing_cells) / total_cells) * 100
        
        # Check for duplicates
        duplicates = df.duplicated().sum()
        duplicate_rate = (duplicates / len(df)) * 100
        
        # Assess validity (domain-specific checks)
        validity_issues = 0
        
        # For UCI dataset - check reasonable MPG values
        if 'mpg' in df.columns:
            unreasonable_mpg = ((df['mpg'] < 5) | (df['mpg'] > 60)).sum()
            validity_issues += unreasonable_mpg
            if unreasonable_mpg > 0:
                print(f"     Unreasonable MPG values: {unreasonable_mpg}")
        
        # For EPA dataset - check city < highway MPG
        if all(col in df.columns for col in ['city_mpg', 'highway_mpg']):
            logical_errors = (df['city_mpg'] > df['highway_mpg']).sum()
            validity_issues += logical_errors
            if logical_errors > 0:
                print(f"     City MPG > Highway MPG: {logical_errors} cases")
        
        # Calculate overall quality score
        validity_score = max(0, 100 - (validity_issues / len(df)) * 100)
        consistency_score = max(0, 100 - duplicate_rate)
        
        overall_quality = (completeness * 0.4 + validity_score * 0.3 + consistency_score * 0.3)
        quality_scores[dataset_name] = overall_quality
        
        print(f"    Completeness: {completeness:.1f}%")
        print(f"    Validity Score: {validity_score:.1f}%")
        print(f"    Consistency Score: {consistency_score:.1f}%")
        print(f"    Overall Quality Score: {overall_quality:.1f}/100")
        
        if overall_quality >= 90:
            status = "EXCELLENT "
        elif overall_quality >= 80:
            status = "GOOD "
        elif overall_quality >= 70:
            status = "FAIR "
        else:
            status = "POOR "
        
        print(f"    Status: {status}")
    
    # 4. Missing Value Analysis
    print("\nSTEP 4: Missing Value Treatment")
    print("-" * 50)
    
    cleaner = DataCleaner()
    cleaned_datasets = {}
    
    for dataset_name, df in datasets.items():
        print(f"\n{dataset_name.upper().replace('_', ' ')} MISSING VALUE TREATMENT:")
        
        missing_before = df.isnull().sum().sum()
        print(f"  Missing values before: {missing_before}")
        
        if missing_before > 0:
            # Apply appropriate cleaning based on dataset
            if dataset_name == 'uci_auto_mpg':
                cleaned_df = cleaner.clean_uci_auto_mpg(df)
            elif dataset_name == 'epa_fuel_economy':
                cleaned_df = cleaner.clean_epa_fuel_economy(df)
            elif dataset_name == 'vehicle_dataset':
                cleaned_df = cleaner.clean_vehicle_dataset(df)
            else:
                cleaned_df = df.copy()
            
            missing_after = cleaned_df.isnull().sum().sum()
            print(f"  Missing values after: {missing_after}")
            print(f"  Reduction: {missing_before - missing_after} ({((missing_before - missing_after) / max(missing_before, 1) * 100):.1f}%)")
            print(f"  Shape change: {df.shape} -> {cleaned_df.shape}")
        else:
            cleaned_df = df.copy()
            print("  No missing values found")
        
        cleaned_datasets[dataset_name] = cleaned_df
    
    # 5. Feature Engineering Summary
    print("\n⚙️ STEP 5: Feature Engineering Summary")
    print("-" * 50)
    
    for dataset_name, df in cleaned_datasets.items():
        original_df = datasets[dataset_name]
        new_features = len(df.columns) - len(original_df.columns)
        
        print(f"\n{dataset_name.upper().replace('_', ' ')}:")
        print(f"  Original columns: {len(original_df.columns)}")
        print(f"  Final columns: {len(df.columns)}")
        print(f"  New features created: {new_features}")
        
        if new_features > 0:
            new_cols = set(df.columns) - set(original_df.columns)
            print(f"  New features: {list(new_cols)}")
    
    # 6. Export Results
    print("\nSTEP 6: Exporting Processed Datasets")
    print("-" * 50)
    
    os.makedirs('data/processed', exist_ok=True)
    
    for dataset_name, df in cleaned_datasets.items():
        filename = f"data/processed/{dataset_name}_cleaned.csv"
        df.to_csv(filename, index=False)
        print(f"  Saved: {filename} ({df.shape[0]:,} rows × {df.shape[1]} columns)")
    
    # 7. Final Summary
    print("\nSTEP 7: Phase II Completion Summary")
    print("-" * 50)
    
    total_original_rows = sum(df.shape[0] for df in datasets.values())
    total_processed_rows = sum(df.shape[0] for df in cleaned_datasets.values())
    total_missing_eliminated = sum(datasets[name].isnull().sum().sum() - cleaned_datasets[name].isnull().sum().sum() 
                                  for name in datasets.keys())
    avg_quality_score = sum(quality_scores.values()) / len(quality_scores)
    
    print(f"PHASE II RESULTS:")
    print(f"  Datasets Processed: {len(datasets)}")
    print(f"  Total Data Points: {total_original_rows:,} -> {total_processed_rows:,}")
    print(f"  Missing Values Eliminated: {total_missing_eliminated:,}")
    print(f"  Average Quality Score: {avg_quality_score:.1f}/100")
    print(f"  Cleaned Datasets Exported: {len(cleaned_datasets)}")
    
    print(f"\nPHASE II STATUS: COMPLETED SUCCESSFULLY")
    print(f"All deliverables generated and ready for submission")
    print(f"Datasets ready for Phase III: Advanced Analytics and Modeling")
    
    print("\n" + "="*80)
    
    return {
        'datasets': datasets,
        'cleaned_datasets': cleaned_datasets,
        'quality_scores': quality_scores,
        'summary': {
            'total_rows': total_processed_rows,
            'missing_eliminated': total_missing_eliminated,
            'avg_quality': avg_quality_score
        }
    }

if __name__ == "__main__":
    results = run_phase_ii_analysis()
    
    # Additional detailed analysis
    print("\nDETAILED DATASET ANALYSIS")
    print("="*80)
    
    for name, df in results['cleaned_datasets'].items():
        print(f"\n{name.upper().replace('_', ' ')} - CLEANED DATASET DETAILS:")
        print(f"Shape: {df.shape}")
        print(f"Quality Score: {results['quality_scores'][name]:.1f}/100")
        
        # Show key statistics
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) > 0:
            print("Key Statistics:")
            stats_df = df[numeric_cols].describe()
            print(stats_df.round(2))
        
        print("-" * 60)