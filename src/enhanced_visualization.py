#!/usr/bin/env python3
"""
Enhanced Interactive Visualizations with Bokeh
Adds tooltips, confidence intervals, and interactive features
"""

from bokeh.plotting import figure, output_file, save
from bokeh.models import HoverTool, ColumnDataSource
import numpy as np

class EnhancedVisualizer:
    """Create interactive visualizations with enhanced features"""
    
    def create_interactive_plot(self, data_dict, output_path):
        """Create interactive plot with hover tooltips"""
        
        # Prepare data
        source = ColumnDataSource(data=data_dict)
        
        # Create figure
        p = figure(
            title="Interactive Validation Results",
            x_axis_label='Structure Size (MB)',
            y_axis_label='Validation Time (minutes)',
            width=800, height=600,
            tools="pan,wheel_zoom,box_zoom,reset,save"
        )
        
        # Add scatter plot with hover
        circles = p.circle('size_mb', 'time_min', source=source, size=15,
                          color='color', alpha=0.7, line_color='black')
        
        # Add hover tool with detailed information
        hover = HoverTool(tooltips=[
            ("Structure", "@name"),
            ("Size", "@size_mb{0.0} MB"),
            ("Time", "@time_min{0.0} min"),
            ("Status", "@status"),
            ("Components", "@components")
        ])
        p.add_tools(hover)
        
        # Add confidence interval shading (if applicable)
        if 'ci_lower' in data_dict and 'ci_upper' in data_dict:
            p.varea(x='size_mb', y1='ci_lower', y2='ci_upper', 
                   source=source, alpha=0.2, color='gray')
        
        # Style
        p.title.text_font_size = '16pt'
        p.axis.axis_label_text_font_size = '12pt'
        
        # Save
        output_file(output_path)
        save(p)
        print(f"✓ Saved interactive plot to {output_path}")

# Example usage
if __name__ == '__main__':
    viz = EnhancedVisualizer()
    
    # Example data with tooltips
    example_data = {
        'name': ['PDBDEV_00000001', 'PDBDEV_00000010', 'PDBDEV_00000020'],
        'size_mb': [1.6, 5.8, 2.1],
        'time_min': [2.5, 9.0, 3.0],
        'status': ['Pass', 'Pass', 'Pass'],
        'components': ['SAS+CXMS', 'EM', 'SAS'],
        'color': ['green', 'green', 'green']
    }
    
    viz.create_interactive_plot(example_data, 'interactive_validation.html')
