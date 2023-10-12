# ufc-predictor

## About
🥊 Repo to scrape historic UFC fighter stats/match results, and build a predictive model to predict the winner of future/hypothetical matches based on historic fighter stats

## Setup
```
pip install -r requirements.txt
```

## Features
✅ COMPLETED ✅:
- Scrape UFC data - fighter stats, and match results. Scraped data as at 2023-09-20 is available under /data.\
```
python -m ufc.scraper
```
- Pre-processing to prep scraped data for modelling - see /data/prepped_data_for_modelling.csv
```
python -m ufc.preprocessing
```

🚧 TODO 🚧:
- Pre-processing/cleaning scraped data
- EDA / visualisations on cleaned data
- Build predictive model
- Visualisation layer on top - potentially a Dash app
