## ⭐ Found This Useful?

If this analysis helped you or you found it valuable:

<table>
<tr>
<td width="33%" align="center">

### 🌟 Star This Repo
Show your appreciation and help others discover this analysis

[⭐ Star Now](../../stargazers)

</td>
<td width="33%" align="center">

### 🔗 Share It
Help the community by sharing

[📱 Tweet](https://twitter.com/intent/tweet?text=Comprehensive%20analysis%20of%20IHMValidation%20software%20-%20great%20example%20of%20systematic%20debugging&url=https://github.com/ShravyaRS/IHMValidation-Analysis)

</td>
<td width="33%" align="center">

### 💬 Discuss
Have questions or suggestions?

[💬 Open Issue](../../issues/new)

</td>
</tr>
</table>

### 📊 Star History

[![Star History Chart](https://api.star-history.com/svg?repos=ShravyaRS/IHMValidation-Analysis&type=Date)](https://star-history.com/#ShravyaRS/IHMValidation-Analysis&Date)

---

## 🚀 How to Use This Repository

### For Users Trying to Install IHMValidation
```bash
# 1. Skip the pain - use our discovered requirements
cd IHMValidation
cat > requirements.txt << 'DEPS'
pdfkit==1.0.0
bokeh==2.4.3
numpy>=1.20,<2.4
scipy>=1.7.0
matplotlib>=3.5.0
plotly>=5.0
ihm>=2.0
jinja2>=3.0
pytz
mendeleev
tornado>=6.2
pillow>=9.0
PyYAML>=6.0
DEPS

# 2. Install system dependency
sudo apt-get install wkhtmltopdf

# 3. Install Python packages
pip install -r requirements.txt

# 4. Run validation
cd ihm_validation
python3 ihm_validator.py your_structure.cif --output results/
```

### For Researchers Analyzing Software

1. **Read the methodology**: [COMPLETE_ANALYSIS_SUMMARY.md](COMPLETE_ANALYSIS_SUMMARY.md)
2. **Study the approach**: Check `scripts/phase*.sh` for systematic testing
3. **Learn bug discovery**: [reports/bug-report.md](reports/bug-report.md)
4. **See reproducibility**: [Dockerfile examples](reproducibility/)

### For Contributors to IHMValidation

1. **Critical bugs to fix**: See [Bug Priority Matrix](#bug-impact-matrix)
2. **Proposed fixes**: Each bug includes solution code
3. **Enhancement ideas**: [Enhancement Proposals](COMPLETE_ANALYSIS_SUMMARY.md#goal-4-technically-sound-enhancement-proposals)
4. **Ready to contribute**: Fork, fix, PR!

### For Academic Citation
```bibtex
@misc{ihmvalidation_analysis_2024,
  author = {Shravya RS},
  title = {IHMValidation: Comprehensive Technical Analysis},
  year = {2024},
  publisher = {GitHub},
  url = {https://github.com/ShravyaRS/IHMValidation-Analysis}
}
```

---

