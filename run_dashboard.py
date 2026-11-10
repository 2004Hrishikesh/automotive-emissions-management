"""
Run the Interactive Dashboard for Automotive Data Analytics
"""

import sys
import os
sys.path.append('src')

import pandas as pd
from visualization.dashboard import AutomotiveAnalyticsDashboard

def load_cleaned_datasets():
    """Load the cleaned datasets"""
    datasets = {}
    
    try:
        # Load cleaned datasets
        datasets['uci_auto_mpg'] = pd.read_csv('data/processed/uci_auto_mpg_cleaned.csv')
        print(f"✓ Loaded UCI Auto MPG: {datasets['uci_auto_mpg'].shape}")
    except Exception as e:
        print(f"✗ Could not load UCI dataset: {e}")
    
    try:
        datasets['epa_fuel_economy'] = pd.read_csv('data/processed/epa_fuel_economy_cleaned.csv')
        print(f"✓ Loaded EPA Fuel Economy: {datasets['epa_fuel_economy'].shape}")
    except Exception as e:
        print(f"✗ Could not load EPA dataset: {e}")
    
    try:
        datasets['vehicle_dataset'] = pd.read_csv('data/processed/vehicle_dataset_cleaned.csv')
        print(f"✓ Loaded Vehicle Dataset: {datasets['vehicle_dataset'].shape}")
    except Exception as e:
        print(f"✗ Could not load Vehicle dataset: {e}")
    
    return datasets

def create_quality_reports(datasets):
    """Create quality assessment reports for datasets"""
    quality_reports = {}
    
    for name, df in datasets.items():
        total_cells = df.shape[0] * df.shape[1]
        missing_cells = df.isnull().sum().sum()
        completeness = ((total_cells - missing_cells) / total_cells) * 100
        
        duplicates = df.duplicated().sum()
        duplicate_rate = (duplicates / len(df)) * 100
        consistency_score = max(0, 100 - duplicate_rate)
        
        # Validity checks
        validity_issues = 0
        if 'mpg' in df.columns:
            unreasonable_mpg = ((df['mpg'] < 5) | (df['mpg'] > 60)).sum()
            validity_issues += unreasonable_mpg
        
        validity_score = max(0, 100 - (validity_issues / len(df)) * 100)
        
        # Overall quality
        overall_quality = (completeness * 0.4 + validity_score * 0.3 + consistency_score * 0.3)
        
        quality_reports[name] = {
            'completeness': completeness,
            'validity': validity_score,
            'consistency': consistency_score,
            'quality_score': overall_quality,  # Changed from 'overall' to 'quality_score'
            'missing_values': missing_cells,
            'duplicates': duplicates,
            'total_records': len(df)
        }
    
    return quality_reports

def main():
    """Main function to run the dashboard"""
    print("="*60)
    print("AUTOMOTIVE DATA ANALYTICS DASHBOARD")
    print("="*60)
    print("Student: Hrishikesh M (22BCE0422)")
    print("Professor: Kumar K")
    print("="*60)
    print()
    
    # Load datasets
    print("Loading cleaned datasets...")
    datasets = load_cleaned_datasets()
    
    if not datasets:
        print("\n✗ No datasets found!")
        print("Please run 'python run_phase_ii_analysis.py' first to process the data.")
        return
    
    print(f"\n✓ Loaded {len(datasets)} datasets successfully")
    print()
    
    # Create quality reports
    print("Generating quality reports...")
    quality_reports = create_quality_reports(datasets)
    
    for name, report in quality_reports.items():
        print(f"\n{name.upper().replace('_', ' ')}:")
        print(f"  Quality Score: {report['quality_score']:.1f}/100")
        print(f"  Records: {report['total_records']:,}")
        print(f"  Completeness: {report['completeness']:.1f}%")
    
    print()
    print("="*60)
    print("Starting Interactive Dashboard...")
    print("="*60)
    print()
    
    # Create and run dashboard
    dashboard = AutomotiveAnalyticsDashboard(datasets, quality_reports)
    
    print("Dashboard Starting...")
    print("Dashboard URL: http://localhost:8050")
    print("Open your browser and navigate to the URL above")
    print("⏹️  Press Ctrl+C to stop the dashboard")
    print()
    
    try:
        dashboard.run_dashboard(debug=True, port=8050)
    except KeyboardInterrupt:
        print("\n\n✓ Dashboard stopped by user")
    except Exception as e:
        print(f"\n✗ Error running dashboard: {e}")
        print("\nTroubleshooting:")
        print("1. Make sure port 8050 is not already in use")
        print("2. Try running: pip install dash plotly pandas")
        print("3. Check if cleaned datasets exist in data/processed/")

if __name__ == "__main__":
    main()
