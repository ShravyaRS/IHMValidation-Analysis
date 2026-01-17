
# Contributing to IHMValidation Container

Thank you for considering contributing to this project!

## How to Contribute

### Reporting Bugs

Found a bug? Please open an issue with:
- Clear description of the problem
- Steps to reproduce
- Expected vs actual behavior
- System information (OS, Singularity version)
- Relevant log output

**Template:**
```
**Bug Description**: Brief summary

**Steps to Reproduce**:
1. Step one
2. Step two

**Expected**: What should happen
**Actual**: What actually happens

**Environment**:
- OS: Ubuntu 22.04
- Singularity: 3.8.0
- Structure: PDBDEV_XXXXXXXX
```

### Suggesting Enhancements

Have an idea? Open an issue with:
- Clear description of the enhancement
- Use case or motivation
- Proposed implementation (if applicable)

### Pull Requests

1. **Fork the repository**
```bash
   git clone https://github.com/ShravyaRS/IHMValidation-Analysis.git
   cd IHMValidation-Analysis
```

2. **Create a feature branch**
```bash
   git checkout -b feature/your-feature-name
```

3. **Make your changes**
   - Follow existing code style
   - Add documentation for new features
   - Test with all 8 validation structures

4. **Test thoroughly**
```bash
   # Rebuild container with your changes
   sudo singularity build --force test.sif singularity/Singularity.def
   
   # Run validation tests
   for pdb in 00000001 00000010 00000015 00000020 00000025 00000030 00000035 00000040; do
     singularity exec test.sif python3 \
       /opt/IHMValidation/ihm_validation/ihm_validator.py \
       -f test-data-extended/PDBDEV_${pdb}.cif \
       --output-root test-output \
       --output-prefix PDBDEV_${pdb}
   done
```

5. **Commit your changes**
```bash
   git add .
   git commit -m "Clear description of changes"
```

6. **Push and create PR**
```bash
   git push origin feature/your-feature-name
```
   
   Then open a Pull Request on GitHub with:
   - Clear title
   - Description of changes
   - Test results (must maintain 100% success rate)

## Coding Standards

### Shell Scripts
- Use `#!/bin/bash` shebang
- Add header comments explaining purpose
- Use meaningful variable names
- Add error checking (`set -e`)

### Python Patches
- Follow existing code style
- Include verification checks
- Add comments for complex logic
- Test syntax with `ast.parse()`

### Documentation
- Update README.md for user-facing changes
- Update TECHNICAL_DETAILS.md for implementation changes
- Keep ARCHITECTURE.md diagrams current
- Add inline comments for complex code

## Testing Requirements

All contributions must:
- Maintain 100% validation success rate (8/8 structures)
- Build successfully without errors
- Not increase container size significantly
- Work on Ubuntu 22.04 with Singularity 3.8+

## Code Review Process

1. Automated checks run on PR submission
2. Maintainer reviews code and tests
3. Feedback provided if changes needed
4. PR merged when approved

## Questions?

Open an issue with the "question" label or contact via GitHub.

## License

By contributing, you agree that your contributions will be licensed under the same license as this project.
