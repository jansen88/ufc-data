# ufc-predictor

## About
🥊 Repo to scrape historic UFC fighter stats/match results, and build a predictive model to predict the winner of future/hypothetical matches based on historic fighter stats

## Features
✅ COMPLETED ✅:
- Web-scraping
  - Scrape UFC data - fighter stats, and match results. Scraped data as at 2023-09-20 is available under /data
- Data cleaning, feature extraction, feature engineering
  - Pre-processing to clean data, reformat/restructure, data checks
  - Feature extraction based on fighter statistics

🚧 TODO 🚧:
- Data extraction pipeline
  - Update allow for efficient refreshes - fetch only new events, but update all fighter stats
- Additional web-scraping: Historic betting odds - unlocks additional information/signal for model, also allows us to test viability of betting strategy and if model is better than just choosing favourite
- Model iteration
  - Additional feature engineering
    - Fight win streak, finish rate (knockouts, submissions)
    - Derived features - durability, tag as wrester/striker/grappler etc.
    - Include if fighter is favourite (if have scraped odds)
  - Review training data
    - Check if predicting on fighters with insufficient data - if filtering to only fighters with > X fights produces better results
    - Check if trends change over time - does model perform better on more recent data, is including more historic data useful
- Finalise feature selection, model selection
- Evaluate model performance, particularly on historic betting odds to assess viability of betting strategy
- Inference + visualisation layer on top

## Setup
Dependency management - poetry or pip
```
poetry install
```
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
| EDA | Univariate analysis relating key attributes to match outcomes | * Confirmed expected relationships between fighter attributes and match outcome <br /> * Confirmed delta of attributes has stronger relationship to match outcome than ratio | notebooks\EDA\20231012 Attributes vs match outcome.ipynb |
| | Data checks | * Data values / representation sensible <br /> * No intercorrelation - highest correlation sees values of ~0.2, for attributes with strongest linear relationship to outcome. | notebooks\EDA\20231016 Data checks.ipynb |
| Feature selection | Initial GBM testing / feature selection | * Delta (of fighter1 and fighter2) features capture as much signal as individual features  <br /> * Highest importance features related to delta of striking stats, and surprisingly also difference in age <br /> * Lowest importance features were height, reach, stance and weight class. Takedown accuracy was <br /> surprisingly less important, compared to other features e.g. takedown attempts | notebooks\ml experiments\20231012 Initial GBM test.ipynb |
| Model selection | Initial GBM testing / feature selection | * Initial tests saw accuracy of 64-65% <br /> * Variation in accuracy depending on hyperparameter selection,  different parameters across folds - may need tuning| notebooks\ml experiments\20231012 Initial GBM test.ipynb |
|  | Initial logistic regression testing |* Initial tests saw accuracy of 65%| notebooks\ml experiments\20231016 Logistic regression test.ipynb |
