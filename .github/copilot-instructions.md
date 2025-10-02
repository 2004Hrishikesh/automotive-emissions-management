# AI Coding Agent Instructions - Automotive Emissions Optimization Project

## Project Overview
Foundation of Data Science course project focusing on automotive industry vehicle emissions and fuel efficiency optimization. This is a multi-phase academic project implementing real-time adaptive emissions prediction systems and integrated fuel efficiency optimization frameworks.

**Current Status:** Phase II (Data Processing) - Completed
**Next Phase:** Phase III (Advanced Analytics and Modeling)

## Project Structure & Key Components

### Core Architecture
- **Data Layer:** Multi-source automotive datasets (UCI Auto MPG, EPA Fuel Economy, Vehicle specifications)
- **Processing Layer:** Comprehensive data cleaning and quality assessment pipeline
- **Analysis Layer:** Missing value treatment, outlier detection, feature engineering
- **Visualization Layer:** Interactive analytics dashboards and process documentation
- **Output Layer:** Cleaned datasets and comprehensive reporting

### Critical File Locations
- **Main Notebook:** `notebooks/phase_ii_data_processing.ipynb` - Complete Phase II implementation
- **Data Processing:** `src/data_processing/` - Core data loading and cleaning modules
- **Visualization:** `src/visualization/dashboard.py` - Interactive dashboard components
- **Processed Data:** `data/processed/` - Cleaned datasets ready for analysis
- **Documentation:** `docs/phase_ii_reports/` - Comprehensive reports and data dictionaries

## Development Patterns & Conventions

### Data Processing Pipeline
The project follows a structured 5-layer approach:
1. **Data Sources** → Multi-format loading with comprehensive error handling
2. **Quality Assessment** → Completeness, validity, and consistency evaluation  
3. **Missing Value Treatment** → Strategy-based imputation (median/mode/KNN/deletion)
4. **Data Cleaning** → Outlier handling, feature engineering, validation
5. **Export & Documentation** → Structured output with full traceability

### Class Architecture Pattern
```python
# Standard pattern for data processing components
class ComponentName:
    def __init__(self):
        self.results = {}
        self.log = []
    
    def analyze_[aspect](self, df, dataset_name):
        # Analysis logic
        return results
    
    def generate_[output](self, results):
        # Output generation
        return formatted_results
```

### Quality Assessment Framework
- **Completeness:** Missing value analysis with percentage thresholds
- **Validity:** Domain-specific validation rules for automotive data
- **Consistency:** Logical relationship verification (e.g., city_mpg < highway_mpg)
- **Quality Scoring:** Weighted composite score (40% completeness, 30% validity, 30% consistency)

## Integration Points & Dependencies

### Required Libraries Stack
```python
# Core data processing
pandas, numpy, scikit-learn

# Visualization & dashboards  
matplotlib, seaborn, plotly, dash

# Analysis & modeling
scipy, statsmodels (for Phase III)
```

### Data Flow Dependencies
1. **AutomotiveDataLoader** → Must execute before any analysis
2. **DataQualityAssessment** → Depends on loaded datasets
3. **MissingValueAnalyzer** → Requires quality assessment results
4. **Dashboard components** → Need processed datasets and quality reports

## Phase-Specific Considerations

### Phase II Completion Requirements
- ✅ Comprehensive data loading with error handling
- ✅ Multi-dimensional quality assessment (completeness/validity/consistency)
- ✅ Advanced missing value treatment with strategy selection
- ✅ Interactive analytics dashboard with 8+ visualization panels
- ✅ Process flow and architecture diagrams
- ✅ Before/after comparison analysis with statistical improvements

### Phase III Preparation Notes
- Cleaned datasets exported in `data/processed/` directory
- Quality scores available for model selection guidance
- Feature engineering foundations established for advanced analytics
- Data dictionaries generated for variable understanding

## Debugging & Development Workflow

### Common Data Issues
- **Missing UCI data access:** Fallback to generated sample data with realistic distributions
- **Memory constraints:** Datasets sized appropriately for educational environment
- **Visualization rendering:** Plotly figures may need explicit `.show()` calls in notebooks

### Validation Checkpoints
1. **Post-loading:** Verify dataset shapes and basic statistics
2. **Post-cleaning:** Compare before/after metrics for improvement validation
3. **Pre-export:** Ensure quality scores meet minimum thresholds (>70 for FAIR status)

### Performance Considerations
- Sample size optimization for educational purposes (398-2000 rows per dataset)
- Memory-efficient processing with chunked operations where applicable
- Visualization complexity balanced for clarity vs. comprehensiveness

## Academic Compliance & Documentation

### Required Deliverables Format
- **Student Info:** Hrishikesh M, 22BCE0422, Professor Kumar K
- **Date Format:** September 30, 2025 (Phase II deadline)
- **Report Structure:** Executive summary → methodology → results → next steps
- **Code Documentation:** Class docstrings, inline comments, processing logs

### Grading Criteria Alignment
- **Data Handling (40%):** Multi-source loading, error handling, validation
- **Data Munging (35%):** Missing values, outliers, feature engineering  
- **Dashboard/Visualization (15%):** Interactive analytics, process diagrams
- **Documentation/Comparison (10%):** Reports, before/after analysis

When working on this project, prioritize data quality and comprehensive documentation over complex algorithms. The focus is on demonstrating mastery of fundamental data science processes rather than advanced modeling techniques.