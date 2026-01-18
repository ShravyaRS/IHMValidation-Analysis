
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
