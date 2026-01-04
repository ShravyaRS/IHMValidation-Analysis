# CRITICAL BUG: ATSAS Installation Incomplete

## Discovery
During systematic validation testing, discovered that SAS validation fails because ATSAS binaries are not accessible in the container.

## Evidence

### Error Message
```
FileNotFoundError: [Errno 2] No such file or directory: 'datcmp'
```

### Investigation Results
1. `which datcmp` - NOT FOUND
2. `find / -name datcmp` - NO RESULTS
3. `dpkg -L atsas | grep bin` - NO OUTPUT
4. ATSAS binaries completely missing from container

## Impact

### Severity: HIGH
- Affects: ALL structures with SAS data
- Blocks: Complete validation of SAS-containing structures
- Success rate: Only structures without SAS can be fully validated

### Affected Validation Types
- SAS validation: COMPLETELY BROKEN
- Other validations: Working correctly

## Root Cause Analysis

### Hypothesis 1: Installation Failed Silently
The ATSAS .deb package installation may have failed during Singularity build but didn't stop the build process.

### Hypothesis 2: Package Incomplete
The ATSAS package may not include the command-line tools, only libraries.

### Hypothesis 3: PATH Configuration
Binaries installed but not added to container PATH (UNLIKELY - cannot find binaries anywhere).

## Reproduction Steps

1. Build Singularity image with ATSAS-3.2.1-1_amd64.deb
2. Attempt validation on structure with SAS data (PDBDEV_00000010)
3. Observe failure at SAS validation step
4. Verify: `singularity exec image.sif which datcmp` returns nothing

## Verification This is Novel

Checked:
- GitHub issues: No mention of ATSAS installation failure
- Documentation: Assumes ATSAS works
- Existing issues: Focus on Bokeh/NumPy, not ATSAS

**This appears to be an undiscovered bug.**

## Proposed Solutions

### Solution 1: Verify ATSAS Package Contents
Before build, verify ATSAS .deb contains expected binaries:
```bash
dpkg-deb -c ATSAS-3.2.1-1_amd64.deb | grep bin
```

### Solution 2: Manual Binary Installation
If package lacks binaries, download ATSAS binaries separately.

### Solution 3: Alternative ATSAS Source
Use different ATSAS distribution or version.

### Solution 4: Disable SAS Validation
Add flag to skip SAS validation when ATSAS unavailable.

## Value of This Discovery

### For Project
1. Explains why some validations fail
2. Identifies critical missing dependency
3. Affects production use of validation server

### For Community
1. Other users likely hitting same issue
2. Documentation can be updated
3. Build process can be fixed

## Immediate Action Items

1. Report to Arthur as critical finding
2. Create GitHub issue with details
3. Test ATSAS package contents
4. Propose concrete fix

## Status
- **Discovered**: January 4, 2026
- **Verified**: Yes - reproduced, investigated, confirmed
- **Reported**: Pending
- **Fix**: Proposed (pending testing)
