## Real Module Dependency Flow
ihm_validator.py (Main Entry Point)
                        |
                        v
                format_checker.py (Validate format)
                        |
                        v
                mmcif_io.py (Parse structure)
                        |
    ____________________|____________________
    |                   |                   |
    v                   v                   v
cx.py              sas.py               em.py
(Crosslinking)    (Small Angle)         (Electron
Validation      Scattering             Microscopy)
(1,298 lines)    (729 lines)           (887 lines)
|                   |                   |
└─────────────┬─────┴───────────────────┘
v
molprobity.py + excludedvolume.py
(Geometry & Steric Validation)
|
v
futures.py (Run validations in parallel)
|
v
|              |             |
v              v             v
report.py    get_plots.py   images.py
(Compile      (Generate     (Render
results)     plots)        images)
|              |             |
└──────────┬───┴─────────────┘
v
generate_static_html_pages.py
|
v
Jinja2 templates + pdfkit
|
v
HTML Report + PDF Report
## Module Descriptions (Real Functions)

### cx.py - Crosslinking-MS Validation (1,298 lines)

**Functions include:**
- `__init__()` - Initialize with structure
- `get_models()` - Extract models from structure
- `get_raw_restraints()` - Get crosslinks
- `get_rtdtype()`, `get_ertype()` - Type assignments
- `assign_ertypes()`, `assign_rtdtypes()` - Assign types
- Calculates: satisfaction %, distance violations

### em.py - 3DEM Validation (887 lines)

**Functions include:**
- `__init__()` - Initialize
- `get_emdb_data()` - Fetch EM data
- `get_emdb_map()` - Download EM map
- `get_emdb_map_metadata()` - Get metadata
- `get_emdb_map_validation()` - Validation metrics
- `get_emdb_ids()` - Get EM IDs from structure
- Calculates: map correlation, resolution fit

### sas.py - SAS Validation (729 lines)

**Functions include:**
- `__init__()` - Initialize
- `get_atsas_version()` - Check ATSAS tools
- `get_sas_ids()` - Get SAS IDs
- `get_sasbdb_ids()` - Get SASBDB IDs
- `get_sascif_dicts()` - Parse SAS data
- `get_intensities()` - Get scattering intensities
- `get_rg_for_plot()` - Calculate Rg for plots
- Calculates: χ² fit, Rg predictions

### mmcif_io.py - Structure File I/O (1,349 lines)

**Purpose:** Parse and write PDB-IHM format mmCIF files

**This is the largest module because:**
- mmCIF is complex format
- Needs to handle all atom types
- Must preserve all metadata
- Requires coordinate transformations

### molprobity.py - Geometry Validation (662 lines)

**Checks:**
- Bond angles (Ramachandran)
- Bond lengths
- Steric clashes
- Geometry outliers

### report.py - Report Generation (545 lines)

**Generates:**
- Summary statistics
- Quality scores
- Compliance metrics
- Report structure

### get_plots.py & sas_plots.py & images.py - Visualization

Three separate modules for plotting:
- **get_plots.py** - General plot logic
- **sas_plots.py** - SAS-specific plots (profiles, fits)
- **images.py** - Image rendering and processing

Shows emphasis on **visual communication** of results.
