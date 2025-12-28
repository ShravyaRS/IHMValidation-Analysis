
---

## Bug #4: Bokeh API Compatibility Issue

### Severity
**HIGH** - Prevents tool from running

### Description
Code uses deprecated Bokeh API (`bokeh.models.widgets.Tabs` and `Panel`)

### Error Message
```
ImportError: cannot import name 'Tabs' from 'bokeh.models.widgets'
```

### Root Cause
- Code written for Bokeh < 3.0
- Bokeh 3.0+ moved Tabs and Panel to different location
- No version pinning in dependencies

### Affected Files
- `get_plots.py:35`

### API Change
```python
# Old API (Bokeh < 3.0):
from bokeh.models.widgets import Tabs, Panel

# New API (Bokeh >= 3.0):
from bokeh.models import TabPanel
from bokeh.models.layouts import Tabs
```

### Reproduction Steps
1. Install latest Bokeh (3.8+)
2. Run: `python3 ihm_validator.py input.cif --output out/`
3. Observe ImportError

### Proposed Fix
**Option 1: Pin Bokeh version**
```
bokeh==2.4.3
```

**Option 2: Update code for Bokeh 3.0+**
```python
# In get_plots.py
try:
    # Bokeh >= 3.0
    from bokeh.models import TabPanel
    from bokeh.models.layouts import Tabs
except ImportError:
    # Bokeh < 3.0
    from bokeh.models.widgets import Tabs, Panel as TabPanel
```

### Impact
- Tool completely non-functional with modern Bokeh
- Silent breaking change for users
- Affects all visualization output

### Workaround
Install Bokeh 2.4.3:
```bash
pip install "bokeh==2.4.3"
```

