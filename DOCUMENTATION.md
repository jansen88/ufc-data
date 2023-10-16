## Purpose
The purpose of this document is to provide project documentation, recording key findings and decisions. This will log key results from EDA or ML experiments.

## Documentation
| Analysis | Finding | Notebook |
| --- | --- | --- |
| Univariate analysis relating key attributes to match outcomes | 1. Confirmed that expected attributes relate to higher incidence of winning - e.g. taller <br />fighter wins more often, longer reach wins more often. <br /> 2. Also confirmed delta of attributes more appropriate than ratio | notebooks\EDA\20231012 Attributes vs match outcome.ipynb |
| Initial GBM testing / feature selection | 1. xgboost classifier on fighter attributes (delta features) has accuracy of 64% <br /> 2. Delta features seem to adequately summarise difference between fighter attributes <br /> 3. Highest importance features related to delta of striking stats, and surprisingly also difference in age <br /> 4. Lowest importance features were height, reach, stance and weight class. Takedown accuracy was <br /> surprisingly less important, compared to other features e.g. takedown attempts | notebooks\ml experiments\20231012 Initial GBM test.ipynb |
