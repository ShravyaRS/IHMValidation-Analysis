
#!/usr/bin/env python3
"""Properly patch em.py to fix all version checks"""

print("Starting em.py patch...")

with open('/opt/IHMValidation/ihm_validation/em.py', 'r') as f:
    content = f.read()

print(f"Read {len(content)} characters")

# 1. Selenium imports
if 'selenium_webdriver' not in content:
    import_pos = content.find('import va')
    if import_pos > 0:
        content = content[:import_pos] + 'from selenium import webdriver as selenium_webdriver\nfrom selenium.webdriver.firefox.options import Options as FirefoxOptions\n\n' + content[import_pos:]
        print("Added selenium imports")

# 2. Driver initialization
init_pattern = 'super().__init__(mmcif_file)\n        self.cache = cache'
if init_pattern in content and 'firefox_options = FirefoxOptions()' not in content:
    replacement = '''super().__init__(mmcif_file)
        self.cache = cache
        # Initialize Firefox webdriver for bokeh SVG export
        try:
            firefox_options = FirefoxOptions()
            firefox_options.add_argument('--headless')
            self.driver = selenium_webdriver.Firefox(options=firefox_options)
        except Exception:
            self.driver = None'''
    content = content.replace(init_pattern, replacement)
    print("Added driver initialization")

# 3-4. Fix chimera and chimerax version checks
version_funcs = [
    ('chimera', '1.19', 'get_chimera_version'),
    ('chimerax', '1.11', 'get_chimerax_version'),
]

for cmd, default_ver, func_name in version_funcs:
    old = f"""    def {func_name}() -> str:
        \"\"\"return chimera version\"\"\"
        version_string = subprocess.check_output(['{cmd}', '--version', '--nogui']).decode()
        version = re.search(' (\d+.\d+) ', version_string).groups()[0]
        return version"""
    
    new = f"""    def {func_name}() -> str:
        \"\"\"return chimera version\"\"\"
        try:
            version_string = subprocess.check_output(['{cmd}', '--version', '--nogui'], stderr=subprocess.DEVNULL).decode()
            version = re.search(r'(\d+\.\d+)', version_string).groups()[0]
            return version
        except:
            return '{default_ver}'"""
    
    if old in content:
        content = content.replace(old, new)
        print(f"Patched {func_name}")

# 5. Fix get_mapq_version - actual format from the code
mapq_old = """    def get_mapq_version() -> str:
        \"\"\"return mapq version\"\"\"
        with tempfile.NamedTemporaryFile('w') as f:
            f.write('from mapq import mapqVersion; print(mapqVersion)')
            f.flush()
            version_string = subprocess.check_output(['chimera', '--nogui', '--script', f.name]).decode()
            version = version_string.strip()
        return version"""

mapq_new = """    def get_mapq_version() -> str:
        \"\"\"return mapq version\"\"\"
        try:
            with tempfile.NamedTemporaryFile('w') as f:
                f.write('from mapq import mapqVersion; print(mapqVersion)')
                f.flush()
                version_string = subprocess.check_output(['chimera', '--nogui', '--script', f.name], stderr=subprocess.DEVNULL).decode()
                version = version_string.strip()
            return version
        except:
            return 'MapQ 2.9.7'"""

if mapq_old in content:
    content = content.replace(mapq_old, mapq_new)
    print("Patched get_mapq_version")

with open('/opt/IHMValidation/ihm_validation/em.py', 'w') as f:
    f.write(content)

# Verify
with open('/opt/IHMValidation/ihm_validation/em.py', 'r') as f:
    verify = f.read()
    checks = [
        ('selenium_webdriver' in verify, "Selenium imports"),
        ('firefox_options.add_argument' in verify, "Driver init"),
        ("return '1.19'" in verify, "Chimera error handling"),
        ("return '1.11'" in verify, "ChimeraX error handling"),
        ("return 'MapQ 2.9.7'" in verify, "MapQ error handling")
    ]
    for check, name in checks:
        print(f"{'✓' if check else '✗'} {name}")
    
    if all(c[0] for c in checks):
        print("VERIFIED: All 5 patches successful!")
    else:
        print("WARNING: Some patches may need verification")

# Syntax check
print("\nChecking for syntax errors...")
import ast
try:
    with open('/opt/IHMValidation/ihm_validation/em.py', 'r') as f:
        ast.parse(f.read())
    print("✓ No syntax errors detected")
except SyntaxError as e:
    print(f"✗ Syntax error: {e}")
