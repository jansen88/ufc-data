# ufc-predictor

## About
🥊 Repo to scrape historic UFC fighter stats/match results, and build a predictive model to predict the winner of future/hypothetical matches based on historic fighter stats

## Setup
Dependency management - Poetry (more frequently updated) or pip (`requirements.txt` exists but less frequently updated)
```
poetry install
```
To run web scraper and update match results/fighter stats:
```
python -m ufc.scraper
```
To run pre-processing, data cleaning, feature engineering on scraped data:
```
python -m ufc.preprocessing
```

## Features completed ✅
- Web-scraping - see `/ufc/scraper`
  - Scrape UFC data - fighter stats, and match results. Scraped data as at 2023-09-20 is available under `/data`
- Data cleaning, feature extraction, feature engineering - see `/ufc/preprocessing`
  - Pre-processing to clean data, reformat/restructure, data checks
  - Feature extraction and engineering, with key features derived from delta of fighter stats (e.g. `delta_age`, `delta_sig_strikes_landed_pm`, `delta_submission_avg_attempted_per15m`)
- Exploratory data analysis - see `/notebooks/eda` and [analyses log](https://github.com/jansen88/ufc-match-predictor/tree/master#detailed-log-of-analyses) below
- Initial model PoC - see `/notebooks/ml-experiments` and [analyses log](https://github.com/jansen88/ufc-match-predictor/tree/master#detailed-log-of-analyses) below
  - GBM / logistic regression see accuracy of ~65%. This initial result suggests that a machine learning model based on fighter attributes may perform comparably to a betting strategy of always picking the favourite ([65%](https://www.mmahive.com/ufc-favorites-vs-underdogs/)).
  - See [analyses log](https://github.com/jansen88/ufc-match-predictor/tree/master#detailed-log-of-analyses) below for feature importance and SHAP values

## Feature backlog 🚧
- Data extraction pipeline
  - Update allow for efficient refreshes - fetch only new events, but update all fighter stats
- Additional web-scraping: Historic betting odds
  - May provide additional signal/information (capture information from market sentiment)
  - Allows us to test viability of betting strategy - if model would outperform choosing favourite
  - Reconstruct modelling approach - instead of predicting if fighter1 or fighter2 win (randomly assigned), predict likelihood of underdog beating favourite
- Model iteration
  - Additional feature engineering
    - Fight win streak, finish rate (knockouts, submissions)
    - Derived features - durability, tag as wrester/striker/grappler etc.
    - Include if fighter is favourite (if have scraped odds)
    - If fighter has moved up/down weight class, short-notice replacement, weighed in over limit - need data source for this
  - Review training data
    - Check if predicting on fighters with insufficient data - if filtering to only fighters with > X fights produces better results
    - Check if trends change over time - does model perform better on more recent data, is including more historic data useful
- Finalise feature selection, model selection
- Evaluate model performance, particularly on historic betting odds to assess viability of betting strategy
- Inference for future matches
- Visualisation layer on top



## Detailed log of analyses

| Process | Analysis | Finding | Notebook |
| --- | --- | --- | --- |
| EDA | Univariate analysis relating key attributes to match outcomes | • Confirmed expected relationships between fighter attributes and match outcome. <br /> Age and average sig. strikes landed previously seem to have the strongest relationships to match win rate<br /> ![image](https://github.com/jansen88/ufc-match-predictor/assets/94953297/3b1999d0-efd5-4a9e-87fb-d3a2f29f29cb) <br /> • Confirmed delta of attributes has stronger relationship to match outcome than ratio | `notebooks\EDA\20231012 Attributes vs match outcome.ipynb` |
| | Data checks | • Data values / representation sensible <br /> • No intercorrelation - highest correlation sees values of ~0.2, for attributes with strongest linear relationship to outcome. | `notebooks\EDA\20231016 Data checks.ipynb` |
| Feature selection | Initial GBM testing / feature selection | • Delta (of fighter1 and fighter2) features capture as much signal as individual features  <br /> • Highest importance features related to delta of striking stats, and surprisingly also difference in age <br /> • Lowest importance features were height, reach, stance and weight class. Takedown accuracy was surprisingly less important, compared to other features e.g. takedown attempts  <br /> • Feature importance (all delta features) ![image](https://github.com/jansen88/ufc-match-predictor/assets/94953297/8090e1db-e46e-4714-bced-4a93da2293ae) <br /> • SHAP values (after removing less important delta features by RFECV) ![image](https://github.com/jansen88/ufc-match-predictor/assets/94953297/ed7a601d-6b58-4d55-9a05-e4f99cd65e84)| `notebooks\ml experiments\20231012 Initial GBM test.ipynb` |
| Model selection | Initial GBM testing / feature selection | • Initial tests saw accuracy of 64-65% <br /> • Variation in accuracy depending on hyperparameter selection,  different parameters across folds - may need tuning | `notebooks\ml experiments\20231012 Initial GBM test.ipynb` |
