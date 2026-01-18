
# System Architecture

## Container Layer Structure
```
┌─────────────────────────────────────────────────────────────────┐
│                     Singularity Container                        │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │                 Ubuntu 22.04 Base System                    │ │
│  │  ┌──────────────────────────────────────────────────────┐  │ │
│  │  │              System Libraries Layer                   │  │ │
│  │  │                                                        │  │ │
│  │  │  - libicu66 (ATSAS dependency)                        │  │ │
│  │  │  - libxft2 (Chimera GUI support)                      │  │ │
│  │  │  - libglib2.0-0, libxrender1                          │  │ │
│  │  │  - Firefox ESR (headless webdriver)                   │  │ │
│  │  └──────────────────────────────────────────────────────┘  │ │
│  │  ┌──────────────────────────────────────────────────────┐  │ │
│  │  │           Python Environment (Conda 3.10)             │  │ │
│  │  │                                                        │  │ │
│  │  │  Scientific Stack:                                    │  │ │
│  │  │  - numpy, scipy, matplotlib                           │  │ │
│  │  │  - pandas, networkx, biopython                        │  │ │
│  │  │                                                        │  │ │
│  │  │  Validation Specific:                                 │  │ │
│  │  │  - ihm==2.7                                           │  │ │
│  │  │  - selenium, bokeh                                    │  │ │
│  │  └──────────────────────────────────────────────────────┘  │ │
│  │  ┌──────────────────────────────────────────────────────┐  │ │
│  │  │            Specialized Software Layer                 │  │ │
│  │  │                                                        │  │ │
│  │  │  ┌─────────────────────────────────────────────────┐ │  │ │
│  │  │  │ ATSAS 3.0.3-1                                   │ │  │ │
│  │  │  │  - datcmp (SAS profile comparison)              │ │  │ │
│  │  │  │  - datgnom, datporod                            │ │  │ │
│  │  │  └─────────────────────────────────────────────────┘ │  │ │
│  │  │  ┌─────────────────────────────────────────────────┐ │  │ │
│  │  │  │ Chimera 1.19                                    │ │  │ │
│  │  │  │  - MapQ plugin                                  │ │  │ │
│  │  │  │  - Molecular visualization                      │ │  │ │
│  │  │  └─────────────────────────────────────────────────┘ │  │ │
│  │  │  ┌─────────────────────────────────────────────────┐ │  │ │
│  │  │  │ ChimeraX 1.11                                   │ │  │ │
│  │  │  │  - Next-gen visualization                       │ │  │ │
│  │  │  └─────────────────────────────────────────────────┘ │  │ │
│  │  │  ┌─────────────────────────────────────────────────┐ │  │ │
│  │  │  │ IMP (Integrative Modeling Platform)             │ │  │ │
│  │  │  └─────────────────────────────────────────────────┘ │  │ │
│  │  │  ┌─────────────────────────────────────────────────┐ │  │ │
│  │  │  │ MODELLER 10.5                                   │ │  │ │
│  │  │  └─────────────────────────────────────────────────┘ │  │ │
│  │  └──────────────────────────────────────────────────────┘  │ │
│  │  ┌──────────────────────────────────────────────────────┐  │ │
│  │  │              IHMValidation Framework                  │  │ │
│  │  │                                                        │  │ │
│  │  │  Core Modules (Patched):                              │  │ │
│  │  │  - ihm_validator.py (main entry point)                │  │ │
│  │  │  - em.py (EM validation with fixes)                   │  │ │
│  │  │  - sas.py (SAS validation)                            │  │ │
│  │  │  - cx.py (Cross-linking validation)                   │  │ │
│  │  │  - model_quality.py (Quality metrics)                 │  │ │
│  │  │  - report.py (PDF generation)                         │  │ │
│  │  └──────────────────────────────────────────────────────┘  │ │
│  └────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

## Component Interaction Diagram
```
┌──────────────┐
│    User      │
└──────┬───────┘
       │ execute validation command
       v
┌─────────────────────────────────┐
│     Singularity Runtime         │
│                                 │
│  Mounts:                        │
│  - Input: structure.cif         │
│  - Output: validation results   │
│  - Cache: downloaded databases  │
└────────┬───────────────────────┘
         │
         v
┌─────────────────────────────────┐
│   ihm_validator.py (main)       │
│                                 │
│  - Parse CLI arguments          │
│  - Initialize components        │
│  - Orchestrate workflow         │
└────┬────────────────────────────┘
     │
     ├──────────────┬──────────────┬──────────────┬──────────────┐
     │              │              │              │              │
     v              v              v              v              v
┌─────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐
│ Quality │  │   SAS    │  │  CX-MS   │  │   EM     │  │  PrISM   │
│ Module  │  │ Module   │  │  Module  │  │  Module  │  │  Module  │
└────┬────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘
     │            │              │              │              │
     │            v              │              v              │
     │       ┌────────┐          │         ┌────────┐         │
     │       │ ATSAS  │          │         │Chimera │         │
     │       │datcmp  │          │         │ MapQ   │         │
     │       └────────┘          │         └────────┘         │
     │                           │                            │
     └───────────────┬───────────┴───────────┬────────────────┘
                     │                       │
                     v                       v
              ┌─────────────┐        ┌─────────────┐
              │   Plots &   │        │   Metrics   │
              │Visualizations│       │Calculations │
              └──────┬──────┘        └──────┬──────┘
                     │                       │
                     └───────────┬───────────┘
                                 │
                                 v
                        ┌─────────────────┐
                        │  Report Module  │
                        │                 │
                        │  - Aggregate    │
                        │  - Template     │
                        │  - Generate PDF │
                        └────────┬────────┘
                                 │
                                 v
                        ┌─────────────────┐
                        │  Output Files   │
                        │                 │
                        │  - Full PDF     │
                        │  - Summary PDF  │
                        │  - HTML archive │
                        └─────────────────┘
```

## Patch Application Architecture
```
Container Build Time:
─────────────────────────────────────────────────────────────

1. Base system installation
   └→ apt packages, conda setup

2. Clone IHMValidation repository
   └→ git clone from upstream

3. Apply patches (patch_em_properly.py)
   │
   ├→ Read em.py source code
   │
   ├→ Insert selenium imports
   │  └→ from selenium import webdriver as selenium_webdriver
   │
   ├→ Add webdriver initialization
   │  └→ firefox_options = FirefoxOptions()
   │     firefox_options.add_argument('--headless')
   │     self.driver = selenium_webdriver.Firefox(options=firefox_options)
   │
   ├→ Wrap get_chimera_version() with try-except
   │  └→ return '1.19' on failure
   │
   ├→ Wrap get_chimerax_version() with try-except
   │  └→ return '1.11' on failure
   │
   └→ Wrap get_mapq_version() with try-except
      └→ return 'MapQ 2.9.7' on failure

4. Verify all patches applied
   └→ Syntax check with ast.parse()

5. Finalize container
   └→ Create SIF image
```

## Dependency Resolution Graph
```
IHMValidation
     │
     ├──[requires]──→ Python 3.10
     │                   │
     │                   ├──[requires]──→ numpy, scipy, matplotlib
     │                   └──[requires]──→ ihm==2.7
     │
     ├──[requires]──→ ATSAS
     │                   │
     │                   └──[requires]──→ libicu66  [FIXED]
     │
     ├──[requires]──→ Chimera
     │                   │
     │                   └──[requires]──→ libxft2  [FIXED]
     │
     ├──[requires]──→ ChimeraX
     │
     ├──[requires]──→ IMP
     │
     ├──[requires]──→ MODELLER
     │
     └──[requires]──→ Selenium
                        │
                        └──[requires]──→ Firefox (headless)  [FIXED]
```

## Error Handling Architecture
```
Function Call
     │
     ├──[try]──→ Execute command
     │             │
     │             ├──[success]──→ Return result
     │             │
     │             └──[exception]──→ Log warning
     │                               └→ Return default value
     │
     └──[validation continues]
```

This pattern applied to:
- get_chimera_version() → default: '1.19'
- get_chimerax_version() → default: '1.11'
- get_mapq_version() → default: 'MapQ 2.9.7'
- Webdriver initialization → default: None (skip plots)
