# IHMValidation: Architecture Deep Dive

## Overview Diagram

How data flows through the system:
INPUT FILES
↓
[Structure coordinates (mmCIF)]
[Experimental data (SAS/MS/EM)]
↓
VALIDATION PIPELINE
├── Stage 1: Load Data
├── Stage 2: Data Quality Check
├── Stage 3: Model Quality Check
├── Stage 4: Fit Assessment
└── Stage 5: Report Generation
↓
OUTPUT REPORT
↓
[HTML Report + PDF Report]

## Module Responsibilities

### validation.py (Main Controller)
- Orchestrates the entire pipeline
- Decides what to do and in what order
- Manages input and output
- Like the "conductor" of an orchestra

### data_quality.py (Data Checks)
- Checks if input files are valid
- Checks if experimental data is good quality
- Produces quality metrics

### model_quality.py (Geometry Checks)
- Checks if atoms are in correct positions
- Checks bond angles
- Checks for clashes between atoms
- Like checking if Lego blocks fit together correctly

### sas_validation.py (SAS-Specific)
- Handles Small Angle Scattering data
- Calculates if model matches SAS measurements
- Specific to SAS data type

### crosslink_validation.py (Crosslinking-Specific)
- Handles Crosslinking-MS data
- Checks if crosslinks are satisfied
- Specific to Crosslinking-MS data type

### 3dem_validation.py (3DEM-Specific)
- Handles Electron Microscopy data
- Calculates correlation with EM map
- Specific to 3DEM data type

### reporting.py (Report Creator)
- Takes all results
- Creates visualizations (graphs, plots)
- Makes HTML reports
- Makes PDF reports

### utils.py (Helper Functions)
- General utility functions
- Reusable helper code
- Formatting and common operations

## Testing Structure

Each module has a corresponding test file:

- validation.py → test_validation.py
- data_quality.py → test_data_quality.py
- model_quality.py → test_model_quality.py
- sas_validation.py → test_sas.py
- crosslink_validation.py → test_crosslink.py
- 3dem_validation.py → test_3dem.py
- reporting.py → test_reporting.py

Plus test data files in `data/` folder.

**Why?** Each piece is tested separately to ensure it works correctly.

## How It All Fits Together

1. **validation.py** calls **data_quality.py** → Check if data is good
2. **validation.py** calls **model_quality.py** → Check if geometry is good
3. **validation.py** calls **sas_validation.py** (if SAS data) → Validate SAS
4. **validation.py** calls **crosslink_validation.py** (if Crosslink data) → Validate crosslinks
5. **validation.py** calls **3dem_validation.py** (if 3DEM data) → Validate 3DEM
6. **validation.py** calls **reporting.py** → Create report

It's like a recipe:
- Start with ingredients (data)
- Follow steps in order
- End with final product (report)

## Why This Design?

### Modularity
- Each module does ONE thing well
- Easy to understand
- Easy to test
- Easy to modify

### Extensibility
- Want to add FRET support? 
- Create fret_validation.py
- Register it in validation.py
- Done!

### Maintainability
- Change one module without affecting others
- Fix bugs in isolation
- Test independently

### Scalability
- Could run data types in parallel
- Could distribute computation
- Could add more data types easily