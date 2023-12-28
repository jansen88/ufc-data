
# ufc-data ![1920px-UFC_Logo svg](https://github.com/jansen88/ufc-match-predictor/assets/94953297/8b2850b7-34c6-46a4-bea5-07cf9488e79a)


## 📖 Contents
* [ℹ️ About ](https://github.com/jansen88/ufc-data?tab=readme-ov-file#-about)
* [🔧 Setup](https://github.com/jansen88/ufc-data?tab=readme-ov-file#-setup)
* [📁 Datasets](https://github.com/jansen88/ufc-data/?tab=readme-ov-file#-datasets)
* [⚒️ Data extraction](https://github.com/jansen88/ufc-data?tab=readme-ov-file#-data-extraction))
* [📊 EDA / Data viz](https://github.com/jansen88/ufc-data?tab=readme-ov-file#-eda--data-viz)
* [🔮 Predictive model](https://github.com/jansen88/ufc-data?tab=readme-ov-file#-predictive-model)

## ℹ️ About 
The UFC (Ultimate Fighting Championship) is a global mixed martial arts (MMA) organization, hosting weekly competitive events that showcase fighters from a range of weight classes and backgrounds. 

This repository contains code and resources relating to the UFC. This includes one of the most comprehensive public UFC datasets available, encompassing official match outcomes and history compiled from the UFC, fighter statistics, as well as historic betting odds. 

The purpose of compiling these datasets is for personal interest for data analysis and to test building a predictive model for match outcome on, as well as being publicly available for external interest.

## 🔧 Setup 
Dependency management - Poetry (more actively maintained) or pip (`requirements.txt` exists but less frequently updated)
```
poetry install
```

## 📁 Datasets

`complete_ufc_data` captures a comprehensive UFC dataset uniquely combining 30 years of match history (from 1994), individual figher statistics and 9 years of historic betting odds (from Nov 2014).

<details open>
  <summary>Data dictionary</summary>


  | Column | Sample values| Description | Source |
  | ---  | ---  | --- | --- |
  | `event_date` | `2023-09-16`	| Date of UFC event | Scraped from UFC match history |
  | `event_name` | `UFC Fight Night: Grasso vs. Shevchenko 2`	| Name of UFC event | Scraped from UFC match history |
  | `weight_class` | `Women's Flyweight` | Weight class of UFC match | Scraped from UFC match history |
  | `fighter1`, `fighter2` | `Alexa Grasso`, `Valentina Shevchenko` | Fighter names; note that `fighter1` should usually be the winner of the match, as this is how the names are ordered in the official match history | Scraped from UFC match history|
  | `favourite`, `underdog` | `Valentina Shevchenko`, `Alexa Grasso`, `NaN` | Fighter names from betting favourite and betting underdogs. <br /> <br /> Note that betting odds do not exist for older years, and that where odds do exist,  there will be missing values where fighter names on the betting site and official UFC match history did not match | Scraped from historic odds on betmma.tips|
  | `favourite_odds`, `underdog_odds` | `1.67`, `2.88`, `NaN` | Betting odds (decimal) | Scraped from historic odds on betmma.tips |
  | `betting_outcome` | `favourite`, `underdog`, `NaN` | Whether the favourite or the underdog was the winner of the match. Provided in this format for easier querying on odds | Scraped from historic odds on betmma.tips |
  | `outcome` | `fighter`, `fighter2`, `Draw` | Match outcome - will usually be `fighter1` as this is how names are ordered in the official match history | Derived from UFC match history|
  | `method` | `S-DEC`, `U-DEC`, `KO/TKO Punches`| Method of victory | Scraped from UFC match history |
  | `round` | `5` | Round of victory | Scraped from UFC match history |
  | fighter1_* <br /> e.g., `fighter1_height`, `fighter1_dob`, `fighter1_reach`, `fighter1_sig_strikes_landed_pm`, `fighter1_takedown_avg_per15m`| | Fighter attributes for `fighter1` at time data was scraped| Derived from UFC fighter statistics | 
  | fighter2_* | | Fighter attributes for `fighter2` at time data was scraped | Derived from UFC fighter statistics | 
  | `events_extract_ts`, `odds_extract_ts`, `fighter_extract_ts` | `2023-09-21 02:02:55.178363	` | Timestamp when dataset was scraped | |

</details>

The raw datasets (scraped from the official [UFC](ufcstats.com) website and [betmma.tips](betmma.tips]) are also available under `/data/`.

## ⚒️ Data extraction

🏃 Code:
* To run web scraper and update match results/fighter stats/betting odds:
  ```
  python -m ufc.scraper
  ```
  Note that the following arguments are permitted:
  * `--events`, `--fighters`, `--odds`, to scrape individually/multiple, rather than all. The default is to scrape all.
* To run pre-processing, data cleaning, on scraped data:
  ```
  python -m ufc.preprocessing
  ```

✅ Features completed:
* Scrape UFC data - fighter stats, and match results
* Scrape historic betting odds from betmma.tips
* Pre-processing to clean data, reformat/restructure, data checks

🚧 Feature backlog 
* Update allow for efficient refreshes, appending instead of replacing all - fetch only new events, but update all fighter stats

## 📊 EDA / Data viz
Some interesting insights and visualisations are shared here:
* Age and average strikes landed PM are key contributors to likelihood of victory; the younger fighter or better striker had an edge and won ~60% of matches historically.  <br />
  ![image](https://github.com/jansen88/ufc-match-predictor/assets/94953297/3b1999d0-efd5-4a9e-87fb-d3a2f29f29cb)

* Historic likelihood of the betting favourite winning increases from a little over 50%, to over 75% as the difference in decimal odds exceeds 2.0.  <br />
  ![image](https://github.com/jansen88/ufc-match-predictor/assets/94953297/9ec6cc29-bcb2-4164-b076-c6a7b2049059)

## 🔮 Predictive model
🚧 Development of ML model to test how well match outcome can be predicted based on fighter stats is WiP:
* Initial PoCs (GBM, logistic regression) attempting to predict match outcome from fighter attributes (had not yet scraped betting odds) saw accuracy of ~65%
* This is comparable to a betting strategy of always picking the favourite ([65%](https://www.mmahive.com/ufc-favorites-vs-underdogs/)), which suggests that betting market sentiment may capture most information the model is currently trained on.
* Significant opportunity still to iterate with further testing of features:
    * Fight win streak, finish rate (knockouts, submissions)
    * Derived features - durability, tag as wrester/striker/grappler etc.
    * Include if fighter is favourite (if have scraped odds)
* Note that MMA is a highly volatile and unpredictable sport, where there are frequently upsets, and match outcome may not be consistently predictable

| Process | Analysis | Finding | Notebook |
| --- | --- | --- | --- |
| Feature selection | Initial GBM testing / feature selection | • Delta (of fighter1 and fighter2) features capture as much signal as individual features  <br /> • Highest importance features related to delta of striking stats, and surprisingly also difference in age <br /> • Lowest importance features were height, reach, stance and weight class. Takedown accuracy was surprisingly less important, compared to other features e.g. takedown attempts  <br /> • Feature importance (all delta features) ![image](https://github.com/jansen88/ufc-match-predictor/assets/94953297/8090e1db-e46e-4714-bced-4a93da2293ae) <br /> • SHAP values (after removing less important delta features by RFECV) ![image](https://github.com/jansen88/ufc-match-predictor/assets/94953297/ed7a601d-6b58-4d55-9a05-e4f99cd65e84)| `notebooks\ml experiments\20231012 Initial GBM test.ipynb` |
| Model selection | Initial GBM testing / feature selection | • Initial tests saw accuracy of 64-65% <br /> • Variation in accuracy depending on hyperparameter selection,  different parameters across folds - may need tuning | `notebooks\ml experiments\20231012 Initial GBM test.ipynb` |

