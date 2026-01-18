
#!/usr/bin/env python3
"""
Bokeh 3.x Compatibility Patch for IHMValidation

This patch updates imports and API calls to work with Bokeh 3.x
while maintaining backwards compatibility with Bokeh 2.x
"""

import sys
from pathlib import Path

def check_bokeh_version():
    """Check installed Bokeh version"""
    try:
        import bokeh
        version = bokeh.__version__
        major = int(version.split('.')[0])
        return version, major
    except ImportError:
        return None, None

def patch_bokeh_imports(file_path):
    """Update Bokeh imports for 3.x compatibility"""
    
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Bokeh 3.x import changes
    replacements = {
        # Widget imports moved
        'from bokeh.models.widgets import': 'from bokeh.models import',
        'bokeh.models.widgets.': 'bokeh.models.',
        
        # Layout imports
        'from bokeh.layouts import': 'from bokeh.layouts import',  # No change, but verify
        
        # Panel integration (if used)
        'from bokeh.io.export import': 'from bokeh.io import export',
        
        # Server imports
        'from bokeh.server.server import Server': 'from bokeh.server import Server',
    }
    
    modified = False
    for old, new in replacements.items():
        if old in content and old != new:
            content = content.replace(old, new)
            modified = True
            print(f"  Updated: {old} -> {new}")
    
    if modified:
        # Backup original
        backup_path = file_path.with_suffix('.py.bak')
        Path(file_path).rename(backup_path)
        
        # Write updated version
        with open(file_path, 'w') as f:
            f.write(content)
        
        print(f"✓ Patched {file_path}")
        print(f"  Backup: {backup_path}")
        return True
    else:
        print(f"  No changes needed for {file_path}")
        return False

def create_compatibility_layer():
    """Create a compatibility shim for Bokeh 2.x and 3.x"""
    
    compat_code = '''
"""
Bokeh Compatibility Layer
Provides unified API for Bokeh 2.x and 3.x
"""

try:
    import bokeh
    BOKEH_VERSION = int(bokeh.__version__.split('.')[0])
except ImportError:
    BOKEH_VERSION = 2

# Widget imports
if BOKEH_VERSION >= 3:
    from bokeh.models import (
        Button, Slider, Select, TextInput, 
        Div, CheckboxGroup, RadioGroup
    )
else:
    from bokeh.models.widgets import (
        Button, Slider, Select, TextInput,
        Div, CheckboxGroup, RadioGroup
    )

# Export for external use
__all__ = [
    'Button', 'Slider', 'Select', 'TextInput',
    'Div', 'CheckboxGroup', 'RadioGroup',
    'BOKEH_VERSION'
]
'''
    
    compat_file = Path('src/bokeh_compat.py')
    with open(compat_file, 'w') as f:
        f.write(compat_code)
    
    print(f"✓ Created compatibility layer: {compat_file}")

def update_requirements():
    """Update requirements.txt to support Bokeh 3.x"""
    
    req_file = Path('requirements.txt')
    with open(req_file, 'r') as f:
        lines = f.readlines()
    
    # Update bokeh line
    updated = []
    for line in lines:
        if line.startswith('bokeh'):
            # Support both 2.x and 3.x
            updated.append('bokeh>=2.4.2  # Compatible with 2.x and 3.x after patch\n')
            print("✓ Updated requirements.txt for Bokeh 3.x support")
        else:
            updated.append(line)
    
    with open(req_file, 'w') as f:
        f.writelines(updated)

if __name__ == '__main__':
    print("Bokeh 3.x Compatibility Patch")
    print("=" * 60)
    
    version, major = check_bokeh_version()
    if version:
        print(f"Detected Bokeh version: {version}")
    else:
        print("Bokeh not installed")
    
    print("\nApplying compatibility updates...")
    
    # Create compatibility layer
    create_compatibility_layer()
    
    # Update requirements
    update_requirements()
    
    print("\n" + "=" * 60)
    print("✓ Bokeh 3.x compatibility implemented")
    print("\nTo use:")
    print("  1. Install: pip install bokeh>=3.0")
    print("  2. Import: from src.bokeh_compat import Button, Slider, ...")
    print("  3. Use widgets as normal - compatibility layer handles versions")
