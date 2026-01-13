#!/usr/bin/env python3
"""Properly patch em.py to fix webdriver initialization"""

import sys

# Read the original file
with open('/opt/IHMValidation/ihm_validation/em.py', 'r') as f:
    lines = f.readlines()

# Find where to add imports (after the shebang and existing imports)
import_insert_line = None
for i, line in enumerate(lines):
    if line.strip().startswith('import ') or line.strip().startswith('from '):
        import_insert_line = i + 1

if import_insert_line:
    # Add selenium imports
    lines.insert(import_insert_line, 'from selenium import webdriver as selenium_webdriver\n')
    lines.insert(import_insert_line + 1, 'from selenium.webdriver.firefox.options import Options as FirefoxOptions\n')

# Find and replace self.driver = None
for i, line in enumerate(lines):
    if 'self.driver = None' in line:
        indent = len(line) - len(line.lstrip())
        replacement = [
            ' ' * indent + '# Initialize Firefox webdriver for bokeh SVG export\n',
            ' ' * indent + 'try:\n',
            ' ' * (indent + 4) + 'firefox_options = FirefoxOptions()\n',
            ' ' * (indent + 4) + 'firefox_options.add_argument("--headless")\n',
            ' ' * (indent + 4) + 'self.driver = selenium_webdriver.Firefox(options=firefox_options)\n',
            ' ' * indent + 'except Exception:\n',
            ' ' * (indent + 4) + 'self.driver = None\n'
        ]
        lines[i:i+1] = replacement
        break

# Write back
with open('/opt/IHMValidation/ihm_validation/em.py', 'w') as f:
    f.writelines(lines)

print("em.py patched successfully")
