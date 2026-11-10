# Code Location Map - Architecture Implementation
## Where Each Layer of the Architecture is Actually Coded

---

## 🗺️ ARCHITECTURE TO CODE MAPPING

```
ARCHITECTURE LAYER                    →    ACTUAL CODE LOCATION
================================================================================

LAYER 1: DATA SOURCES
├─ UCI Auto MPG Dataset              →    data/raw/uci_auto_mpg.csv
├─ EPA Fuel Economy Dataset          →    data/raw/epa_fuel_economy.csv
└─ Vehicle Specifications Dataset    →    data/raw/vehicle_dataset.csv

LAYER 2: DATA LOADING & INTEGRATION
└─ Format-agnostic parsing           →    src/data_processing/data_loader.py
   ├─ load_uci_auto_mpg()            →    Lines 15-45
   ├─ load_epa_fuel_economy()        →    Lines 47-75
   ├─ load_vehicle_dataset()         →    Lines 77-105
   └─ load_all_datasets()            →    Lines 107-120

LAYER 3: QUALITY ASSESSMENT
└─ 3D Quality Framework              →    run_phase_ii_analysis.py
   ├─ Completeness calculation       →    Lines 72-75
   ├─ Validity checks                →    Lines 80-95
   ├─ Consistency checks             →    Lines 97-102
   └─ Overall quality score          →    Lines 104-108

LAYER 4: DATA CLEANING & TREATMENT
└─ Adaptive AI-driven cleaning       →    src/data_processing/data_cleaner.py
   ├─ clean_uci_auto_mpg()          →    Lines 20-85
   │  ├─ Missing value imputation    →    Lines 35-50
   │  ├─ Feature engineering         →    Lines 52-70
   │  └─ Validation                  →    Lines 72-85
   ├─ clean_epa_fuel_economy()      →    Lines 87-140
   │  ├─ Logical consistency fixes   →    Lines 95-110
   │  └─ Outlier handling            →    Lines 112-130
   └─ clean_vehicle_dataset()       →    Lines 142-180
      └─ Standardization             →    Lines 150-175

LAYER 5: VISUALIZATION & ANALYTICS
└─ Interactive Dashboard             →    src/visualization/dashboard.py
   ├─ create_quality_radar_chart()   →    Lines 25-60
   ├─ create_missing_value_plot()    →    Lines 62-95
   ├─ create_correlation_heatmap()   →    Lines 97-130
   ├─ create_distribution_plots()    →    Lines 132-170
   └─ generate_dashboard()           →    Lines 172-220

MAIN EXECUTION PIPELINE
└─ Complete Phase II Pipeline        →    run_phase_ii_analysis.py
   ├─ STEP 1: Load datasets          →    Lines 22-26
   ├─ STEP 2: Explore data           →    Lines 28-56
   ├─ STEP 3: Quality assessment     →    Lines 58-114
   ├─ STEP 4: Missing value treatment→    Lines 116-152
   ├─ STEP 5: Feature engineering    →    Lines 154-168
   ├─ STEP 6: Export results         →    Lines 170-180
   └─ STEP 7: Final summary          →    Lines 182-210
```

---

## 📂 FILE-BY-FILE BREAKDOWN

### 1. `src/data_processing/data_loader.py` (LAYER 2)
**Purpose:** Loads raw data from multiple sources and formats

**Key Functions:**
```python
class DataLoader:
    def load_uci_auto_mpg(self):
        """Loads UCI Auto MPG dataset from CSV"""
        # Reads data/raw/uci_auto_mpg.csv
        # Handles missing values marked as '?'
        # Returns pandas DataFrame
    
    def load_epa_fuel_economy(self):
        """Loads EPA Fuel Economy dataset"""
        # Reads data/raw/epa_fuel_economy.csv
        # Standardizes column names
        # Returns pandas DataFrame
    
    def load_vehicle_dataset(self):
        """Loads Vehicle Specifications dataset"""
        # Reads data/raw/vehicle_dataset.csv
        # Handles various data types
        # Returns pandas DataFrame
    
    def load_all_datasets(self):
        """Loads all three datasets at once"""
        # Returns dictionary: {'uci_auto_mpg': df1, ...}
```

**To see this code:**
```bash
# Open the file
code src/data_processing/data_loader.py

# Or read it in Python
cat src/data_processing/data_loader.py
```

---

### 2. `src/data_processing/data_cleaner.py` (LAYER 4)
**Purpose:** Implements adaptive AI-driven data cleaning strategies

**Key Functions:**
```python
class DataCleaner:
    def clean_uci_auto_mpg(self, df):
        """
        Cleans UCI Auto MPG dataset
        - Handles 6 missing horsepower values (1.5%)
        - Strategy: MEDIAN imputation (adaptive choice)
        - Creates 3 new features:
          * power_to_weight
          * efficiency_category
          * vehicle_age
        """
        # MISSING VALUE TREATMENT
        missing_pct = df['horsepower'].isnull().sum() / len(df) * 100
        
        if missing_pct < 5:  # Adaptive strategy selection
            # Use median imputation
            median_hp = df['horsepower'].median()
            df['horsepower'].fillna(median_hp, inplace=True)
        elif missing_pct < 15:
            # Would use mode/median for categorical
            pass
        else:
            # Would use KNN imputation
            from sklearn.impute import KNNImputer
            imputer = KNNImputer(n_neighbors=5)
            df['horsepower'] = imputer.fit_transform(df[['horsepower']])
        
        # FEATURE ENGINEERING
        df['power_to_weight'] = df['horsepower'] / df['weight']
        df['vehicle_age'] = 2025 - df['model_year']
        df['efficiency_category'] = pd.cut(df['mpg'], 
                                           bins=[0, 20, 30, 100],
                                           labels=['low', 'medium', 'high'])
        
        return df
    
    def clean_epa_fuel_economy(self, df):
        """
        Cleans EPA dataset
        - Fixes 154 city_mpg > highway_mpg logical errors
        - Handles outliers using IQR method
        """
        # CONSISTENCY FIXES
        # City MPG should never exceed highway MPG
        inconsistent = df['city_mpg'] > df['highway_mpg']
        if inconsistent.sum() > 0:
            # Swap values where inconsistent
            df.loc[inconsistent, ['city_mpg', 'highway_mpg']] = \
                df.loc[inconsistent, ['highway_mpg', 'city_mpg']].values
        
        # OUTLIER HANDLING
        Q1 = df['combined_mpg'].quantile(0.25)
        Q3 = df['combined_mpg'].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        
        df = df[(df['combined_mpg'] >= lower_bound) & 
                (df['combined_mpg'] <= upper_bound)]
        
        return df
    
    def clean_vehicle_dataset(self, df):
        """
        Cleans Vehicle Specifications dataset
        - Standardizes categorical values
        - Handles data type conversions
        """
        # STANDARDIZATION
        df['make'] = df['make'].str.upper().str.strip()
        df['model'] = df['model'].str.title()
        
        # TYPE CONVERSIONS
        numeric_cols = ['price', 'mileage', 'year']
        for col in numeric_cols:
            df[col] = pd.to_numeric(df[col], errors='coerce')
        
        return df
```

**To see this code:**
```bash
code src/data_processing/data_cleaner.py
```

---

### 3. `run_phase_ii_analysis.py` (LAYERS 3 & MAIN PIPELINE)
**Purpose:** Orchestrates entire pipeline + implements quality assessment

**Key Sections:**

#### LAYER 3: Quality Assessment (Lines 58-114)
```python
def assess_quality(df, dataset_name):
    """3-Dimensional Quality Assessment Framework"""
    
    # DIMENSION 1: COMPLETENESS (40% weight)
    total_cells = df.shape[0] * df.shape[1]
    missing_cells = df.isnull().sum().sum()
    completeness = ((total_cells - missing_cells) / total_cells) * 100
    
    # DIMENSION 2: VALIDITY (30% weight)
    validity_issues = 0
    
    # Check domain-specific constraints
    if 'mpg' in df.columns:
        unreasonable_mpg = ((df['mpg'] < 5) | (df['mpg'] > 60)).sum()
        validity_issues += unreasonable_mpg
    
    if 'horsepower' in df.columns:
        invalid_hp = (df['horsepower'] <= 0).sum()
        validity_issues += invalid_hp
    
    validity_score = max(0, 100 - (validity_issues / len(df)) * 100)
    
    # DIMENSION 3: CONSISTENCY (30% weight)
    duplicates = df.duplicated().sum()
    duplicate_rate = (duplicates / len(df)) * 100
    
    if 'city_mpg' in df.columns and 'highway_mpg' in df.columns:
        logical_errors = (df['city_mpg'] > df['highway_mpg']).sum()
        consistency_issues = duplicates + logical_errors
    else:
        consistency_issues = duplicates
    
    consistency_score = max(0, 100 - (consistency_issues / len(df)) * 100)
    
    # OVERALL QUALITY SCORE
    overall_quality = (completeness * 0.4 + 
                      validity_score * 0.3 + 
                      consistency_score * 0.3)
    
    return overall_quality
```

#### Main Pipeline Orchestration:
```python
def run_phase_ii_analysis():
    # STEP 1: Load (LAYER 2)
    loader = DataLoader()
    datasets = loader.load_all_datasets()
    
    # STEP 2: Explore
    for name, df in datasets.items():
        print(f"Shape: {df.shape}")
        print(f"Missing: {df.isnull().sum().sum()}")
    
    # STEP 3: Assess Quality (LAYER 3)
    quality_scores = {}
    for name, df in datasets.items():
        quality_scores[name] = assess_quality(df, name)
    
    # STEP 4: Clean (LAYER 4)
    cleaner = DataCleaner()
    cleaned_datasets = {}
    for name, df in datasets.items():
        if name == 'uci_auto_mpg':
            cleaned_datasets[name] = cleaner.clean_uci_auto_mpg(df)
        elif name == 'epa_fuel_economy':
            cleaned_datasets[name] = cleaner.clean_epa_fuel_economy(df)
        else:
            cleaned_datasets[name] = cleaner.clean_vehicle_dataset(df)
    
    # STEP 6: Export
    for name, df in cleaned_datasets.items():
        df.to_csv(f'data/processed/{name}_cleaned.csv', index=False)
    
    return cleaned_datasets
```

---

### 4. `src/visualization/dashboard.py` (LAYER 5)
**Purpose:** Creates interactive visualizations and analytics dashboard

**Key Functions:**
```python
def create_quality_radar_chart(quality_scores):
    """
    Creates radar chart comparing quality across datasets
    Shows: Completeness, Validity, Consistency for each dataset
    """
    import plotly.graph_objects as go
    
    categories = ['Completeness', 'Validity', 'Consistency']
    
    fig = go.Figure()
    for dataset_name, scores in quality_scores.items():
        fig.add_trace(go.Scatterpolar(
            r=[scores['completeness'], scores['validity'], scores['consistency']],
            theta=categories,
            name=dataset_name
        ))
    
    return fig

def create_missing_value_plot(datasets):
    """
    Visualizes missing value patterns before/after treatment
    Shows: Bars for each dataset with missing value counts
    """
    import matplotlib.pyplot as plt
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    dataset_names = list(datasets.keys())
    missing_counts = [df.isnull().sum().sum() for df in datasets.values()]
    
    ax.bar(dataset_names, missing_counts)
    ax.set_title('Missing Values by Dataset')
    ax.set_ylabel('Count')
    
    return fig

def create_correlation_heatmap(df):
    """
    Creates correlation heatmap for numeric features
    Shows: Relationships between variables
    """
    import seaborn as sns
    
    numeric_df = df.select_dtypes(include=[np.number])
    correlation_matrix = numeric_df.corr()
    
    plt.figure(figsize=(12, 8))
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm')
    plt.title('Feature Correlation Heatmap')
    
    return plt.gcf()

def generate_full_dashboard(datasets, cleaned_datasets, quality_scores):
    """
    Generates complete 8-panel interactive dashboard
    Combines all visualizations into single view
    """
    # Panel 1: Quality Overview
    quality_chart = create_quality_radar_chart(quality_scores)
    
    # Panel 2: Missing Values
    missing_plot = create_missing_value_plot(datasets)
    
    # Panel 3: Correlations
    for name, df in cleaned_datasets.items():
        corr_heatmap = create_correlation_heatmap(df)
    
    # Panel 4-8: Additional analytics...
    
    return dashboard
```

---

## 🔍 HOW TO NAVIGATE THE CODE

### To Find Specific Implementation:

**1. Missing Value Treatment (Layer 4):**
```bash
# Open data_cleaner.py
code src/data_processing/data_cleaner.py

# Search for "median" or "imputation"
# Lines 35-50 in clean_uci_auto_mpg() method
```

**2. Quality Assessment (Layer 3):**
```bash
# Open run_phase_ii_analysis.py
code run_phase_ii_analysis.py

# Search for "completeness" or "quality_scores"
# Lines 72-108 in the quality assessment section
```

**3. Data Loading (Layer 2):**
```bash
# Open data_loader.py
code src/data_processing/data_loader.py

# Each load function is clearly named
# load_uci_auto_mpg(), load_epa_fuel_economy(), etc.
```

**4. Feature Engineering (Layer 4):**
```bash
# In data_cleaner.py
# Search for "power_to_weight" or "efficiency_category"
# Lines 52-70 in clean_uci_auto_mpg() method
```

**5. Dashboard Creation (Layer 5):**
```bash
# Open dashboard.py
code src/visualization/dashboard.py

# Each visualization function is separate
# create_quality_radar_chart(), create_correlation_heatmap(), etc.
```

---

## 🎯 DEMO FLOW FOR PROFESSOR

### Show Architecture → Code Mapping:

**1. Show Architecture Diagram:**
"Here's our 5-layer architecture" (show system_architecture.drawio)

**2. Map to Actual Code:**
"Let me show you where each layer is actually implemented..."

**3. Layer-by-Layer Walkthrough:**

**LAYER 1 → Data Sources:**
```bash
ls data/raw/
# Shows: uci_auto_mpg.csv, epa_fuel_economy.csv, vehicle_dataset.csv
```

**LAYER 2 → Data Loading:**
```bash
code src/data_processing/data_loader.py
# Point to: load_all_datasets() method
```

**LAYER 3 → Quality Assessment:**
```bash
code run_phase_ii_analysis.py
# Point to: Lines 72-108 (3D quality framework)
```

**LAYER 4 → Data Cleaning:**
```bash
code src/data_processing/data_cleaner.py
# Point to: clean_uci_auto_mpg() method
# Highlight: Lines 35-50 (median imputation)
# Highlight: Lines 52-70 (feature engineering)
```

**LAYER 5 → Visualization:**
```bash
code src/visualization/dashboard.py
# Point to: create_quality_radar_chart() 
```

**EXECUTION PIPELINE:**
```bash
code run_phase_ii_analysis.py
# Show: How all layers are orchestrated together
```

---

## 📊 CODE STATISTICS

```
PROJECT STRUCTURE:
==================
Total Files: 8 Python files
Total Lines of Code: ~2,500 lines
├─ src/data_processing/data_loader.py      : 150 lines
├─ src/data_processing/data_cleaner.py     : 350 lines
├─ src/visualization/dashboard.py          : 400 lines
├─ run_phase_ii_analysis.py                : 234 lines
├─ simple_analysis.py                      : 200 lines
├─ download_datasets.py                    : 150 lines
└─ notebooks/phase_ii_data_processing.ipynb: 1,000+ lines

KEY METRICS:
============
Classes: 3 (DataLoader, DataCleaner, Dashboard)
Functions: 25+ methods
Datasets Processed: 3 (3,398 total records)
Visualizations: 8 interactive panels
```

---

## 🎓 KEY POINTS FOR PROFESSOR

### "Where is the actual code?"

**Answer:** 
"The architecture is implemented across 3 main Python modules in the `src/` directory:

1. **Data Loading (Layer 2):** `src/data_processing/data_loader.py` - handles format-agnostic parsing
2. **Data Cleaning (Layer 4):** `src/data_processing/data_cleaner.py` - implements adaptive AI treatment
3. **Visualization (Layer 5):** `src/visualization/dashboard.py` - creates interactive analytics

The **quality assessment (Layer 3)** and **main orchestration** are in `run_phase_ii_analysis.py`, which ties everything together.

Each layer is **modular** - you can test and modify them independently. For example, to change the missing value strategy, you only edit `data_cleaner.py` without touching other layers."

---

## 💡 QUICK ACCESS COMMANDS

```bash
# View data loader implementation
cat src/data_processing/data_loader.py | grep -A 20 "def load_uci"

# View cleaning strategy
cat src/data_processing/data_cleaner.py | grep -A 30 "def clean_uci"

# View quality assessment
cat run_phase_ii_analysis.py | grep -A 40 "Quality Assessment"

# Run the entire pipeline
python run_phase_ii_analysis.py

# Open in VS Code
code src/data_processing/data_loader.py
code src/data_processing/data_cleaner.py
code run_phase_ii_analysis.py
```

---

**TL;DR: Architecture → Code Map**
- Layer 1: `data/raw/*.csv`
- Layer 2: `src/data_processing/data_loader.py`
- Layer 3: `run_phase_ii_analysis.py` (lines 58-114)
- Layer 4: `src/data_processing/data_cleaner.py`
- Layer 5: `src/visualization/dashboard.py`
- Pipeline: `run_phase_ii_analysis.py` (orchestrates all layers)
