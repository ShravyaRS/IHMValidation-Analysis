
# Validation Output Examples

## What to Expect

After running validation, you will get:

1. **Full Validation Report PDF** (~10-50 pages)
   - Detailed analysis of all validation components
   - High-resolution plots and figures
   - Comprehensive quality metrics

2. **Summary Report PDF** (2-3 pages)
   - Key findings at a glance
   - Pass/fail status for each component
   - Critical issues highlighted

3. **Interactive HTML Dashboard**
   - Bokeh-powered interactive plots
   - Zoom, pan, and hover for details
   - Exportable visualizations

## Example Screenshots

### Success Case
![Success Report](success_example.png)
*Example of successful validation with all checks passing*

### Quality Metrics
![Quality Metrics](metrics_example.png)
*Interactive quality assessment dashboard*

### Issue Detection
![Issue Detection](issues_example.png)
*Clear reporting when validation issues are found*

## Generate Your Own

Run validation to generate these outputs:
```bash
bash run_example.sh
```

Results will be in `example_output/` directory.
