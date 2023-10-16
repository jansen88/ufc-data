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
- Additional feature engineering
  - Low hanging fruit done - more complex features in backlog
- EDA / visualisations
- Build predictive model
    - Feature selection
    - Model selection
- Evaluate model performance
  - Also evaluate vs betting odds, weighting errors by odds to assess viability of betting strategy
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

| Analysis | Finding | Notebook |
| --- | --- | --- |
| Univariate analysis relating key attributes to match outcomes | 1. Confirmed that expected attributes relate to higher incidence of winning - e.g. taller <br />fighter wins more often, longer reach wins more often. <br /> 2. Also confirmed delta of attributes more appropriate than ratio | notebooks\EDA\20231012 Attributes vs match outcome.ipynb |
| Data checks | Data values / representation all seem sensible. No intercorrelation - highest correlation sees values of ~0.2, <br /> for attributes with highest expected relationship to outcome. | notebooks\EDA\20231016 Data checks.ipynb |
| Initial GBM testing / feature selection | 1. xgboost classifier on fighter attributes (delta features) has accuracy of 64% <br /> 2. Delta features seem to adequately summarise difference between fighter attributes <br /> 3. Highest importance features related to delta of striking stats, and surprisingly also difference in age <br /> 4. Lowest importance features were height, reach, stance and weight class. Takedown accuracy was <br /> surprisingly less important, compared to other features e.g. takedown attempts | notebooks\ml experiments\20231012 Initial GBM test.ipynb |
