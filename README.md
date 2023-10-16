# ufc-predictor

## About
🥊 Repo to scrape historic UFC fighter stats/match results, and build a predictive model to predict the winner of future/hypothetical matches based on historic fighter stats

## Features
✅ COMPLETED ✅:
- Web-scraping
  - Scrape UFC data - fighter stats, and match results. Scraped data as at 2023-09-20 is available under /data
- Data cleaning, feature extraction, feature engineering
  - Pre-processing to clean data, reformat/restructure, data checks
  - Initial feature engineering (for immediately extractable features) complete

🚧 TODO 🚧:

- Additional web-scraping: Historic betting odds
- Additional feature engineering: e.g. fight win streak, odds
- Build predictive model - Feature selection, model selection
- Evaluate model performance, particularly on historic betting odds to assess viability of betting strategy
- Inference + visualisation layer on top

## Setup
Dependency management
```
pip install -r requirements.txt
```
Run web scraper
```
python -m ufc.scraper
```
Run pre-processing, data cleaning, feature engineering on scraped data
```
python -m ufc.preprocessing
```

## Detailed log of analyses

| Process | Analysis | Finding | Notebook |
| --- | --- | --- | --- |
| EDA | Univariate analysis relating key attributes to match outcomes | * Confirmed that expected attributes relate to higher incidence of winning - e.g. taller <br />fighter wins more often, longer reach wins more often. <br /> * Also confirmed delta of attributes more appropriate than ratio | notebooks\EDA\20231012 Attributes vs match outcome.ipynb |
| | Data checks | * Data values / representation all seem sensible. No intercorrelation - highest correlation sees values of ~0.2, <br /> for attributes with highest expected relationship to outcome. | notebooks\EDA\20231016 Data checks.ipynb |
| Feature selection | Initial GBM testing / feature selection | * Delta features seem to adequately summarise difference between fighter attributes <br /> * Highest importance features related to delta of striking stats, and surprisingly also difference in age <br /> * Lowest importance features were height, reach, stance and weight class. Takedown accuracy was <br /> surprisingly less important, compared to other features e.g. takedown attempts | notebooks\ml experiments\20231012 Initial GBM test.ipynb |
| Model selection | Initial GBM testing / feature selection | * xgboost classifier sees accuracy of 64% | notebooks\EDA\20231016 Data checks.ipynb |
|  | Initial logistic regression testing |* See accuracy of 65% - surprisingly better than xgboost | notebooks\ml experiments\20231016 Logistic regression test.ipynb |
