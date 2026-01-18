
#!/usr/bin/env python3
"""
Unit Tests for IHMValidation Components
Tests individual validation functions
"""

import pytest
import subprocess
from pathlib import Path

class TestValidationComponents:
    """Test individual validation components"""
    
    def test_container_exists(self):
        """Test that container file exists"""
        container = Path("IHMValidation/ihmvalidation_complete.sif")
        assert container.exists(), "Container file not found"
        assert container.stat().st_size > 1e9, "Container seems too small"
    
    def test_atsas_accessible(self):
        """Test that ATSAS datcmp is accessible"""
        result = subprocess.run(
            ['singularity', 'exec', 
             'IHMValidation/ihmvalidation_complete.sif',
             'which', 'datcmp'],
            capture_output=True,
            text=True
        )
        assert result.returncode == 0, "datcmp not found in container"
        assert '/usr/bin/datcmp' in result.stdout
    
    def test_python_version(self):
        """Test Python version in container"""
        result = subprocess.run(
            ['singularity', 'exec',
             'IHMValidation/ihmvalidation_complete.sif',
             'python3', '--version'],
            capture_output=True,
            text=True
        )
        assert result.returncode == 0
        assert '3.10' in result.stdout, "Wrong Python version"
    
    def test_ihm_module_import(self):
        """Test that ihm module can be imported"""
        result = subprocess.run(
            ['singularity', 'exec',
             'IHMValidation/ihmvalidation_complete.sif',
             'python3', '-c', 'import ihm; print(ihm.__version__)'],
            capture_output=True,
            text=True
        )
        assert result.returncode == 0
        assert '2.7' in result.stdout

class TestValidationLogic:
    """Test validation logic and error detection"""
    
    def test_valid_structure_passes(self):
        """Test that valid structure passes validation"""
        result = subprocess.run(
            ['singularity', 'exec',
             'IHMValidation/ihmvalidation_complete.sif',
             'python3', '/opt/IHMValidation/ihm_validation/ihm_validator.py',
             '-f', 'examples/valid/good_structure.cif',
             '--output-root', 'tests/output',
             '--output-prefix', 'valid_test'],
            capture_output=True,
            timeout=300
        )
        # Should complete without fatal errors
        assert result.returncode in [0, 1], "Unexpected error code"
    
    def test_invalid_structure_detected(self):
        """Test that invalid structure is detected"""
        result = subprocess.run(
            ['singularity', 'exec',
             'IHMValidation/ihmvalidation_complete.sif',
             'python3', '/opt/IHMValidation/ihm_validation/ihm_validator.py',
             '-f', 'examples/invalid/broken_structure.cif',
             '--output-root', 'tests/output',
             '--output-prefix', 'invalid_test'],
            capture_output=True,
            timeout=60
        )
        # Should fail or complete with errors
        assert result.returncode != 0, "Failed to detect invalid structure"

if __name__ == '__main__':
    pytest.main([__file__, '-v'])
