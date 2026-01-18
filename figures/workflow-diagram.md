# IHMValidation Workflow

## High-Level Process Flow
```
┌─────────────────────────────────────────────────────────────┐
│                    Input: structure.cif                      │
└────────────────────────┬────────────────────────────────────┘
                         │
                         v
┌─────────────────────────────────────────────────────────────┐
│              Step 1: Format Validation                       │
│                                                              │
│  - Verify mmCIF format                                       │
│  - Parse molecular structure                                 │
│  - Extract metadata                                          │
└────────────────────────┬────────────────────────────────────┘
                         │
                         v
┌─────────────────────────────────────────────────────────────┐
│              Step 2: Model Quality Assessment                │
│                                                              │
│  - Excluded volume satisfaction                              │
│  - Geometry validation                                       │
│  - Stereochemistry checks                                    │
└────────────────────────┬────────────────────────────────────┘
                         │
                         v
┌─────────────────────────────────────────────────────────────┐
│              Step 3: SAS Validation                          │
│                                                              │
│  - ATSAS datcmp analysis                                     │
│  - Profile comparison (experimental vs model)                │
│  - Chi-squared fit quality                                   │
│  - Guinier analysis                                          │
└────────────────────────┬────────────────────────────────────┘
                         │
                         v
┌─────────────────────────────────────────────────────────────┐
│              Step 4: Cross-linking MS Validation             │
│                                                              │
│  - Distance restraint satisfaction                           │
│  - Violation analysis                                        │
│  - Cross-link coverage                                       │
└────────────────────────┬────────────────────────────────────┘
                         │
                         v
┌─────────────────────────────────────────────────────────────┐
│              Step 5: 3D-EM Validation                        │
│                                                              │
│  - Map-model correlation (Chimera)                           │
│  - MapQ quality assessment                                   │
│  - Local resolution analysis                                 │
└────────────────────────┬────────────────────────────────────┘
                         │
                         v
┌─────────────────────────────────────────────────────────────┐
│              Step 6: Precision Analysis                      │
│                                                              │
│  - PrISM sampling assessment                                 │
│  - Ensemble diversity metrics                                │
│  - Uncertainty quantification                                │
└────────────────────────┬────────────────────────────────────┘
                         │
                         v
┌─────────────────────────────────────────────────────────────┐
│              Step 7: Report Generation                       │
│                                                              │
│  - Full validation PDF                                       │
│  - Summary validation PDF                                    │
│  - Interactive HTML report                                   │
│  - Supplementary data tables                                 │
└────────────────────────┬────────────────────────────────────┘
                         │
                         v
┌─────────────────────────────────────────────────────────────┐
│                    Output Files                              │
│                                                              │
│  - structure_full_validation.pdf                             │
│  - structure_summary_validation.pdf                          │
│  - structure_htmls.zip                                       │
└─────────────────────────────────────────────────────────────┘
```

## Data Flow Details

### Input Processing
```
structure.cif
    │
    ├── Structural Information
    │   ├── Atomic coordinates
    │   ├── Coarse-grained beads
    │   └── Multi-scale representation
    │
    ├── Restraint Information
    │   ├── SAS profiles
    │   ├── Cross-links
    │   ├── EM maps
    │   └── Other experimental data
    │
    └── Metadata
        ├── Sample information
        ├── Experimental conditions
        └── Software provenance
```

### Validation Components

#### SAS Validation Pipeline
```
SAS Data → ATSAS datcmp → Profile Comparison → Chi-squared → Pass/Fail
                ↓
          Guinier Analysis
                ↓
          Plot Generation
```

#### Cross-linking MS Pipeline
```
CX-MS Data → Distance Calculation → Restraint Check → Violation Analysis → Pass/Fail
                                            ↓
                                    Coverage Assessment
                                            ↓
                                    Satisfaction Plot
```

#### EM Validation Pipeline
```
EM Map → Chimera Fit → Correlation → MapQ Assessment → Pass/Fail
              ↓              ↓
         Resolution    Local Quality
              ↓              ↓
         Visualization → Combined Report
```

## Error Handling Flow
```
┌──────────────┐
│ Validation   │
│   Step       │
└──────┬───────┘
       │
       ├─── Success ────────────→ Continue
       │
       └─── Failure ────┐
                        │
                        v
                ┌───────────────┐
                │ Error Type?   │
                └───────┬───────┘
                        │
            ├───────────┼───────────┤
            │           │           │
            v           v           v
       ┌────────┐  ┌────────┐  ┌────────┐
       │ Fatal  │  │Warning │  │ Info   │
       └───┬────┘  └───┬────┘  └───┬────┘
           │           │           │
           v           v           v
       [Stop]     [Continue]  [Continue]
                   [Log]       [Log]
```

## Performance Characteristics

### Timeline by Structure Size
```
Structure Size    Validation Time
1-2 MB           ████░░░░░░  2-3 min
2-4 MB           ███████░░░  4-6 min
4-6 MB           ██████████  8-10 min
```

### Resource Usage
```
Memory Usage Pattern:
    
8GB  ┤                                    ╭─ Peak (large structures)
6GB  ┤                          ╭────────╯
4GB  ┤              ╭──────────╯
2GB  ┼─────────────╯            Typical usage
0GB  ┴────────────────────────────────────
     Start    SAS    CX-MS    EM    Report
```
