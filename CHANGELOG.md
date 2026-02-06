# Changelog

All notable changes to Python CorMap validation project.

## [1.0.0] - 2026-02-06

### Added
- Initial Python CorMap implementation
- Validation against DATCMP (56 datasets)
- Regression test suite (5 tests)
- Bootstrap confidence intervals
- Bland-Altman analysis
- Performance benchmarks (2484x speedup)
- Complete documentation

### Validated
- 84% agreement within 0.05 tolerance (95% CI: 68-96%)
- Pearson correlation r = 0.999998
- Spearman correlation rho = 0.927

### Known Limitations
- See LIMITATIONS.md

## [0.9.0] - 2026-02-04

### Added
- Initial validation with 6 datasets
- Basic comparison scripts

### Changed
- Expanded to 56 datasets for statistical robustness

## Future

### Planned
- Continuous integration (GitHub Actions)
- Automated validation on new PDB-IHM entries
- Extended validation on RNA/DNA SAS data
