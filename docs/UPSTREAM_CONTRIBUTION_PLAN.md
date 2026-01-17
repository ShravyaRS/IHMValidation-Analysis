
# Upstream Contribution Strategy

## Objective
Contribute fixes back to IHMValidation repository to benefit the entire community.

## Proposed Contributions

### 1. Pull Request: ATSAS Installation Fix
**Target**: `IHMValidation/docs/installation.md`  
**Changes**:
````markdown
### Ubuntu 22.04 ATSAS Installation

For Ubuntu 22.04, ATSAS requires manual libicu66 installation:
```bash
# Install libicu66 dependency
wget http://archive.ubuntu.com/ubuntu/pool/main/i/icu/libicu66_66.1-2ubuntu2_amd64.deb
sudo apt install -y ./libicu66_66.1-2ubuntu2_amd64.deb

# Install ATSAS
sudo dpkg -i ATSAS-3.0.3-1_amd64.deb
sudo apt install -y -f
```
````

**Impact**: Prevents other users from encountering the same issue

### 2. Pull Request: Robust Version Detection
**Target**: `IHMValidation/ihm_validation/em.py`  
**Changes**: Add try-except blocks to version detection functions  
**Rationale**: Prevents validation failures when libraries are missing  
**Backward Compatibility**: Yes (defaults to sensible versions)

### 3. Pull Request: Webdriver Initialization
**Target**: `IHMValidation/ihm_validation/em.py`  
**Changes**: Initialize Selenium webdriver in __init__  
**Rationale**: Enables Bokeh plot generation  
**Backward Compatibility**: Yes (graceful fallback if unavailable)

## Contribution Timeline

### Phase 1: Documentation (Week 1)
- Create GitHub issues documenting each problem
- Provide reproduction steps
- Link to this repository as reference implementation

### Phase 2: Pull Requests (Week 2-3)
- Submit ATSAS installation documentation PR
- Submit em.py error handling PR
- Submit webdriver initialization PR

### Phase 3: Community Engagement (Ongoing)
- Respond to maintainer feedback
- Revise PRs as requested
- Help other users facing similar issues

## Expected Outcomes

1. **Official adoption** of fixes in upstream repository
2. **Citation** in IHMValidation documentation
3. **Community benefit** - all users get improvements
4. **Professional recognition** - visible open-source contribution

## Success Metrics

- [ ] Issues created and acknowledged by maintainers
- [ ] PRs submitted and under review
- [ ] At least 1 PR merged
- [ ] Fixes included in next IHMValidation release
