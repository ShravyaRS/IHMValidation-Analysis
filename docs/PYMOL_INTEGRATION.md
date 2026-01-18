
# PyMOL Integration Guide

Visualize IHMValidation results in PyMOL.

## Installation
```bash
# Install PyMOL
conda install -c conda-forge pymol-open-source

# Or via package manager
sudo apt install pymol
```

## Basic Visualization

### Load Structure
```python
# In PyMOL
load examples/valid/good_structure.cif, structure1
```

### Color by Validation Results
```python
# Color by B-factor (can represent quality metrics)
spectrum b, rainbow, structure1

# Show cross-links
distance xlinks, /structure1//A/42/CA, /structure1//A/85/CA
```

## Advanced: Automated Visualization Script
```python
# validation_viz.py - PyMOL script
from pymol import cmd
import json

def load_validation_results(structure_cif, results_json):
    """Load structure and color by validation metrics"""
    
    # Load structure
    cmd.load(structure_cif, "structure")
    
    # Load validation results
    with open(results_json) as f:
        results = json.load(f)
    
    # Color by quality score
    for residue, score in results['quality'].items():
        if score > 0.8:
            cmd.color("green", f"structure and resi {residue}")
        elif score > 0.5:
            cmd.color("yellow", f"structure and resi {residue}")
        else:
            cmd.color("red", f"structure and resi {residue}")
    
    # Show cross-links
    if 'crosslinks' in results:
        for xl in results['crosslinks']:
            res1, res2 = xl['residue1'], xl['residue2']
            cmd.distance(f"xlink_{res1}_{res2}",
                        f"structure and resi {res1} and name CA",
                        f"structure and resi {res2} and name CA")

# Usage in PyMOL
# run validation_viz.py
# load_validation_results('structure.cif', 'validation_results.json')
```

## Example Workflow

1. **Run Validation**
```bash
singularity exec IHMValidation/ihmvalidation_complete.sif python3 \
  /opt/IHMValidation/ihm_validation/ihm_validator.py \
  -f structure.cif \
  --output-root results \
  --output-prefix structure
```

2. **Extract Quality Metrics**
```python
# extract_metrics.py
import json

def extract_for_pymol(validation_output):
    """Extract metrics in PyMOL-friendly format"""
    # Parse validation output
    # Export as JSON
    pass
```

3. **Visualize in PyMOL**
```bash
pymol structure.cif
# Then load script and color
```

## Gallery

### Quality Visualization
![PyMOL Quality](../docs/screenshots/pymol_quality.png)
*Structure colored by validation quality scores*

### Cross-link Satisfaction
![PyMOL Cross-links](../docs/screenshots/pymol_xlinks.png)
*Cross-linking restraints visualized*

## Tips

- Use `set cartoon_fancy_helices, 1` for better visualization
- Color schemes: `spectrum` command for continuous scales
- Save sessions: `save session.pse` for reproducibility

## References

- [PyMOL Wiki](https://pymolwiki.org/)
- [IHMValidation Docs](https://github.com/salilab/IHMValidation)
