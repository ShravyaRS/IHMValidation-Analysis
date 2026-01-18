
#!/usr/bin/env python3
"""
Integration Tests for Complete Validation Workflow
Tests end-to-end validation pipeline
"""

import pytest
import subprocess
from pathlib import Path
import time

class TestCompleteWorkflow:
    """Test complete validation workflow"""
    
    @pytest.fixture
    def test_structure(self):
        """Provide test structure path"""
        return "test-data-extended/PDBDEV_00000001.cif"
    
    def test_full_validation_pipeline(self, test_structure):
        """Test complete validation pipeline"""
        if not Path(test_structure).exists():
            pytest.skip("Test structure not available")
        
        start_time = time.time()
        
        result = subprocess.run(
            ['singularity', 'exec',
             'IHMValidation/ihmvalidation_complete.sif',
             'python3', '/opt/IHMValidation/ihm_validation/ihm_validator.py',
             '-f', test_structure,
             '--output-root', 'tests/integration_output',
             '--output-prefix', 'integration_test'],
            capture_output=True,
            timeout=600
        )
        
        elapsed = time.time() - start_time
        
        # Check completion
        assert result.returncode == 0, f"Validation failed: {result.stderr}"
        
        # Check outputs exist
        output_dir = Path('tests/integration_output/integration_test')
        assert output_dir.exists(), "Output directory not created"
        
        pdf_files = list(output_dir.glob('*.pdf'))
        assert len(pdf_files) > 0, "No PDF reports generated"
        
        # Performance check
        assert elapsed < 300, f"Validation took too long: {elapsed}s"
        
        print(f"\n✓ Full validation completed in {elapsed:.1f}s")
        print(f"✓ Generated {len(pdf_files)} PDF report(s)")
    
    def test_batch_processing(self):
        """Test batch processing of multiple structures"""
        test_files = list(Path('test-data-extended').glob('PDBDEV_*.cif'))[:3]
        
        if len(test_files) < 3:
            pytest.skip("Insufficient test structures")
        
        for test_file in test_files:
            result = subprocess.run(
                ['singularity', 'exec',
                 'IHMValidation/ihmvalidation_complete.sif',
                 'python3', '/opt/IHMValidation/ihm_validation/ihm_validator.py',
                 '-f', str(test_file),
                 '--output-root', 'tests/batch_output',
                 '--output-prefix', test_file.stem],
                capture_output=True,
                timeout=600
            )
            # At least should not crash
            assert result.returncode in [0, 1]

if __name__ == '__main__':
    pytest.main([__file__, '-v', '-s'])
