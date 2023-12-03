"""
Cleaning steps:
- Rename columns
- Fix date types - e.g. dates
- Split fight record W-L-D into separate columns for W, L, D
- Convert measurements for height/weight/reach from strings in imperial
units to metric
- Check for and drop duplicates in fighters
"""

import pandas as pd
import numpy as np

def clean_events(raw_events) -> pd.DataFrame:
    """Preprocessing for modelling"""
    cleaned_events = raw_events.copy()
    
    # Subset columns
    cleaned_events = cleaned_events[[
        "event_name",
        "event_date",
        "Weight class",
        "fighter1",
        "fighter2",
        "outcome"
    ]]

    # Rename columns
    cleaned_events = cleaned_events.rename({
        "Weight class": "weight_class"
    }, axis=1)

    # Convert date types
    cleaned_events["event_date"] = pd.to_datetime(
        cleaned_events["event_date"]
    )

    return cleaned_events


def _convert_height_imperial_to_metric(height) -> float:
    try:
        # Split the height string into feet and inches
        if ("'" in height) & ("\"" in height):
            parts = height.split("'")
            feet = int(parts[0])
            inches = int(parts[1].rstrip('"'))
        elif ("\"" in height):
            feet = 0
            inches = int(height.split('"')[0])

        # Convert feet and inches to centimeters
        total_inches = feet * 12 + inches
        cm = total_inches * 2.54

        return cm
    except:
        return np.nan



def _convert_weight_imperial_to_metric(weight) -> float:
    pound = 0.453592
    kg = weight * pound

    return kg

def _drop_duplicates(fighters) -> pd.DataFrame:
    fighters["dupe_count"] = (
        fighters
        .groupby("name", as_index=False)
        ['name']
        .transform("count")
    )

    if len(fighters[fighters.dupe_count > 1]) > 0:
        print("Dropping duplicates...")
        print(fighters[fighters.dupe_count > 1])

    fighters = fighters[fighters["dupe_count"] == 1]
    fighters = fighters.drop("dupe_count", axis=1)

    return fighters


def clean_fighters(raw_fighters) -> pd.DataFrame:
    """Preprecessing for modelling"""

    cleaned_fighters = raw_fighters.copy()

    # replace missing values
    cleaned_fighters = cleaned_fighters.replace("--", np.NaN)

    # split up fight record
    cleaned_fighters[["curr_wins", "curr_losses", "curr_draws_nc"]] = \
        cleaned_fighters["fight_record"].str.split("-", expand=True)
    
    # convert imperial to metric
    cleaned_fighters["curr_weight"] = cleaned_fighters["Weight"] \
        .str.replace("lbs.", "") \
        .transform(lambda x: float(x)) \
        .pipe(_convert_weight_imperial_to_metric)
    
    cleaned_fighters["height"] = cleaned_fighters["Height"] \
        .transform(lambda x: str(x)) \
        .apply(lambda x: _convert_height_imperial_to_metric(x))
    
    cleaned_fighters["reach"] = cleaned_fighters["Reach"] \
        .transform(lambda x: str(x)) \
        .apply(lambda x: _convert_height_imperial_to_metric(x))
    
    # convert date types
    cleaned_fighters["dob"] = pd.to_datetime(
        cleaned_fighters["DOB"], format="%b%d,%Y"
    )

    # convert percentages
    cleaned_fighters[["Str.Acc.", "Str.Def", "TDDef.", "TDAcc."]] = \
        cleaned_fighters[["Str.Acc.", "Str.Def", "TDDef.", "TDAcc."]]\
            .applymap(lambda x: pd.to_numeric(x.rstrip('%'))/100)
    
    # subset and rename
    rename_cols = {
        "name": "name",
        "curr_wins": "curr_wins",
        "curr_losses": "curr_losses",
        "curr_weight": "curr_weight",
        "height": "height",
        "reach": "reach",
        "STANCE": "stance",
        "dob": "dob",
        "SLpM": "sig_strikes_landed_pm",
        "Str.Acc.": "sig_strikes_accuracy",
        "SApM": "sig_strikes_absorbed_pm",
        "Str.Def": "sig_strikes_defended",
        "TDAvg.": "takedown_avg_per15m",
        "TDAcc.": "takedown_accuracy",
        "TDDef.": "takedown_defence",
        "Sub.Avg.": "submission_avg_attempted_per15m",
    }
    
    cleaned_fighters = cleaned_fighters.rename(rename_cols, axis=1)
    cleaned_fighters = cleaned_fighters[rename_cols.values()]

    # Drop duplicates
    cleaned_fighters = _drop_duplicates(cleaned_fighters)

    return cleaned_fighters


def clean_odds(raw_odds) -> pd.DataFrame:

    odds_df = raw_odds.copy()

    # # Drop inf rows
    # odds_df = odds_df[
    #     ~(
    #         (odds_df["fighter1_odds"] == np.inf) | (odds_df["fighter2_odds"] == np.inf)
    #     )
    # ]

    # # Drop draws and no contests
    # odds_df = odds_df[odds_df["result"] != "-"]

    # Recode to favourite vs underdog
    # Where equal odds - we will consider fighter1 as the favourite (minority of cases so fine to include for modelling)
    odds_df["favourite"] = np.where(
        odds_df["fighter1_odds"] <= odds_df["fighter2_odds"], odds_df["fighter1"], odds_df["fighter2"]
    )
    odds_df["underdog"] = np.where(
        odds_df["fighter1_odds"] > odds_df["fighter2_odds"], odds_df["fighter1"], odds_df["fighter2"]
    )
    odds_df["outcome"] = np.select(
        [
            odds_df["result"] == odds_df["favourite"],
            odds_df["result"] == odds_df["underdog"]
        ],
        [
            "favourite",
            "underdog"
        ]
        , default = np.nan
    )

    odds_df["favourite_odds"] = np.where(
        odds_df["fighter1_odds"] <= odds_df["fighter2_odds"], odds_df["fighter1_odds"], odds_df["fighter2_odds"]
    )
    odds_df["underdog_odds"] = np.where(
        odds_df["fighter1_odds"] > odds_df["fighter2_odds"], odds_df["fighter1_odds"], odds_df["fighter2_odds"]
    )

    odds_df = odds_df[
        [
            "event", "favourite", "underdog", "favourite_odds", "underdog_odds", "outcome"
        ]
    ]

    return odds_df