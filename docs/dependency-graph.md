# IHMValidation Dependency Graph

## Discovered Dependency Chain
```
ihm_validator.py
    ├── pdfkit ❌ (not documented)
    ├── jinja2 ❌ (not documented)
    └── report.py
        ├── mmcif_io.py
        │   ├── utility.py ✅
        │   └── ihm ❌ (not documented)
        ├── excludedvolume.py
        │   └── mendeleev ❌ (not documented)
        ├── get_plots.py
        │   └── bokeh ❌ (version conflict!)
        ├── sas.py
        │   ├── scipy ❌
        │   └── numpy ❌ (version conflict!)
        └── sas_plots.py
            ├── matplotlib ❌
            └── plotly ❌

❌ = Not documented (discovered through errors)
✅ = Found in codebase
```
