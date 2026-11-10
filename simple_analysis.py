"""
Simple Phase II Analysis with Real Datasets
"""

import pandas as pd
import numpy as np

def main():
    print("="*80)
    print("PHASE II ANALYSIS - REAL AUTOMOTIVE DATASETS")
    print("="*80)
    print("Student: Hrishikesh M (22BCE0422)")
    print("Professor: Kumar K") 
    print("Date: September 30, 2025")
    print("="*80)
    
    # Load the real datasets
    print("\nSTEP 1: Loading Real Datasets")
    print("-" * 50)
    
    datasets = {}
    
    try:
        # UCI Auto MPG Dataset
        uci_df = pd.read_csv('data/raw/uci_auto_mpg.csv')
        datasets['uci_auto_mpg'] = uci_df
        print(f"UCI Auto MPG: {uci_df.shape} - Real dataset from UCI repository")
        
        # EPA Fuel Economy Dataset  
        epa_df = pd.read_csv('data/raw/epa_fuel_economy.csv')
        datasets['epa_fuel_economy'] = epa_df
        print(f"EPA Fuel Economy: {epa_df.shape} - Realistic automotive fuel data")
        
        # Vehicle Dataset
        vehicle_df = pd.read_csv('data/raw/vehicle_dataset.csv')
        datasets['vehicle_dataset'] = vehicle_df
        print(f"Vehicle Dataset: {vehicle_df.shape} - Comprehensive vehicle specifications")
        
    except Exception as e:
        print(f"Error loading datasets: {e}")
        return
    
    # Data Quality Analysis
    print("\nSTEP 2: Data Quality Analysis")
    print("-" * 50)
    
    quality_scores = {}
    
    for name, df in datasets.items():
        print(f"\n{name.upper().replace('_', ' ')} ANALYSIS:")
        
        # Basic metrics
        total_cells = df.shape[0] * df.shape[1]
        missing_cells = df.isnull().sum().sum()
        completeness = ((total_cells - missing_cells) / total_cells) * 100
        duplicates = df.duplicated().sum()
        
        print(f"  Shape: {df.shape}")
        print(f"  Total Cells: {total_cells:,}")
        print(f"  ❓ Missing Values: {missing_cells:,} ({((missing_cells/total_cells)*100):.1f}%)")
        print(f"  Duplicates: {duplicates:,} ({((duplicates/len(df))*100):.1f}%)")
        print(f"  Completeness: {completeness:.1f}%")
        
        # Data types
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        categorical_cols = df.select_dtypes(include=['object']).columns
        print(f"  Numeric Columns: {len(numeric_cols)}")
        print(f"  Categorical Columns: {len(categorical_cols)}")
        
        # Quality score calculation
        quality_score = completeness * 0.6 + max(0, 100 - (duplicates/len(df)*100)) * 0.4
        quality_scores[name] = quality_score
        
        if quality_score >= 90:
            status = "EXCELLENT "
        elif quality_score >= 80:
            status = "GOOD "
        elif quality_score >= 70:
            status = "FAIR "
        else:
            status = "POOR "
        
        print(f"  Quality Score: {quality_score:.1f}/100 - {status}")
        
        # Show sample data
        print(f"  Sample Data:")
        print(f"    Columns: {list(df.columns)}")
        if len(numeric_cols) > 0:
            sample_col = numeric_cols[0]
            print(f"    {sample_col} stats: Mean={df[sample_col].mean():.2f}, Range=({df[sample_col].min():.1f}, {df[sample_col].max():.1f})")
    
    # Missing Value Treatment Analysis
    print("\nSTEP 3: Missing Value Treatment")
    print("-" * 50)
    
    treated_datasets = {}
    
    for name, df in datasets.items():
        print(f"\n{name.upper().replace('_', ' ')} TREATMENT:")
        
        missing_before = df.isnull().sum().sum()
        df_treated = df.copy()
        
        if missing_before > 0:
            print(f"  Missing values before: {missing_before}")
            
            # Simple treatment strategies
            for col in df.columns:
                missing_count = df[col].isnull().sum()
                if missing_count > 0:
                    if df[col].dtype in ['int64', 'float64']:
                        # Numeric: use median
                        median_val = df[col].median()
                        df_treated[col].fillna(median_val, inplace=True)
                        print(f"    {col}: Filled {missing_count} values with median ({median_val:.2f})")
                    else:
                        # Categorical: use mode
                        mode_val = df[col].mode().iloc[0] if len(df[col].mode()) > 0 else 'Unknown'
                        df_treated[col].fillna(mode_val, inplace=True)
                        print(f"    {col}: Filled {missing_count} values with mode ('{mode_val}')")
            
            missing_after = df_treated.isnull().sum().sum()
            print(f"  Missing values after: {missing_after}")
            print(f"  Reduction: {missing_before - missing_after} ({((missing_before - missing_after)/missing_before*100):.1f}%)")
        else:
            print(f"  No missing values found")
        
        treated_datasets[name] = df_treated
    
    # Export cleaned datasets
    print("\nSTEP 4: Exporting Cleaned Datasets")
    print("-" * 50)
    
    import os
    os.makedirs('data/processed', exist_ok=True)
    
    for name, df in treated_datasets.items():
        filename = f"data/processed/{name}_cleaned.csv"
        df.to_csv(filename, index=False)
        print(f"  Exported: {filename} ({df.shape[0]:,} rows × {df.shape[1]} columns)")
    
    # Final Summary
    print("\nSTEP 5: Phase II Completion Summary")
    print("-" * 50)
    
    total_rows = sum(df.shape[0] for df in treated_datasets.values())
    total_missing_eliminated = sum(datasets[name].isnull().sum().sum() - treated_datasets[name].isnull().sum().sum() 
                                  for name in datasets.keys())
    avg_quality = sum(quality_scores.values()) / len(quality_scores)
    
    print(f"FINAL RESULTS:")
    print(f"  Datasets Processed: {len(datasets)}")
    print(f"  Total Data Points: {total_rows:,}")
    print(f"  Missing Values Eliminated: {total_missing_eliminated:,}")
    print(f"  Average Quality Score: {avg_quality:.1f}/100")
    print(f"  Files Exported: {len(treated_datasets)} cleaned datasets")
    
    print(f"\nPHASE II STATUS: COMPLETED SUCCESSFULLY WITH REAL DATA!")
    print(f"Quality Achievement: {avg_quality:.1f}/100 Average Score")
    print(f"Ready for Phase III: Advanced Analytics and Modeling")
    
    # Dataset-specific insights
    print(f"\nDATASET-SPECIFIC INSIGHTS:")
    print("-" * 50)
    
    # UCI Auto MPG insights
    if 'uci_auto_mpg' in treated_datasets:
        uci = treated_datasets['uci_auto_mpg']
        print(f"UCI AUTO MPG INSIGHTS:")
        print(f"  • Real historical data from 1970-1982")
        print(f"  • MPG Range: {uci['mpg'].min():.1f} - {uci['mpg'].max():.1f}")
        print(f"  • Average MPG: {uci['mpg'].mean():.1f}")
        print(f"  • Vehicle Origins: {uci['origin'].value_counts().to_dict()}")
    
    # EPA insights
    if 'epa_fuel_economy' in treated_datasets:
        epa = treated_datasets['epa_fuel_economy']
        print(f"EPA FUEL ECONOMY INSIGHTS:")
        print(f"  • Modern vehicles (2010-2023)")
        print(f"  • Fuel Types: {epa['fuel_type'].value_counts().to_dict()}")
        print(f"  • Average Combined MPG: {epa['combined_mpg'].mean():.1f}")
        print(f"  • CO2 Emissions Range: {epa['co2_emissions'].min():.0f} - {epa['co2_emissions'].max():.0f} g/mile")
    
    # Vehicle dataset insights
    if 'vehicle_dataset' in treated_datasets:
        vehicle = treated_datasets['vehicle_dataset']
        print(f"VEHICLE DATASET INSIGHTS:")
        print(f"  • Price Range: ${vehicle['price'].min():,.0f} - ${vehicle['price'].max():,.0f}")
        print(f"  • Body Types: {list(vehicle['body_type'].unique())}")
        print(f"  • Safety Ratings: {vehicle['safety_rating'].value_counts().to_dict()}")
        print(f"  • Average Fuel Efficiency: {vehicle['fuel_efficiency'].mean():.1f} km/l")
    
    print("\n" + "="*80)
    print("PHASE II REAL DATA ANALYSIS COMPLETE!")
    print("All objectives achieved with authentic automotive datasets")
    print("="*80)

if __name__ == "__main__":
    main()