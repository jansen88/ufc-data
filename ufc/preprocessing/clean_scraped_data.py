import pandas as pd
import numpy as np

def read_scraped_events():
    return pd.read_csv("./data/event_results.csv")

def read_scraped_fighters():
    return pd.read_csv("./data/fighter_stats.csv")


def clean_events(raw_events):
    """Preprocessing for modelling"""
    cleaned_events = raw_events.copy()
    
    # Subset columns
    cleaned_events = cleaned_events[[
        "event_date",
        "Weight class",
        "fighter1",
        "fighter2",
        "outcome"
    ]]

    # Rename columns
    cleaned_events = cleaned_events.rename({
        "Weight class": "weight_class"
    })

    # Convert date types
    cleaned_events["event_date"] = pd.to_datetime(
        cleaned_events["event_date"]
    )

    return cleaned_events


def convert_height_imperial_to_metric(height):
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



def convert_weight_imperial_to_metric(weight):
    pound = 0.453592
    kg = weight * pound

    return kg


def clean_fighters(raw_fighters):
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
        .pipe(convert_weight_imperial_to_metric)
    
    cleaned_fighters["curr_height"] = cleaned_fighters["Height"] \
        .transform(lambda x: str(x)) \
        .apply(lambda x: convert_height_imperial_to_metric(x))
    
    cleaned_fighters["reach"] = cleaned_fighters["Reach"] \
        .transform(lambda x: str(x)) \
        .apply(lambda x: convert_height_imperial_to_metric(x))
    
    # convert date types
    cleaned_fighters["dob"] = pd.to_datetime(
        cleaned_fighters["DOB"], format="%b%d,%Y"
    )

    # convert percentages
    cleaned_fighters[["Str.Acc.", "Str.Def", "TDDef.", "TDAcc."]] = \
        cleaned_fighters[["Str.Acc.", "Str.Def", "TDDef.", "TDAcc."]]\
            .map(lambda x: pd.to_numeric(x.rstrip('%'))/100)
    
    # subset and rename
    rename_cols = {
        "name": "name",
        "curr_wins": "curr_wins",
        "curr_losses": "curr_losses",
        "curr_weight": "curr_weight",
        "curr_height": "curr_height",
        "reach": "reach",
        "STANCE": "stance",
        "dob": "dob",
        "SLpM": "sig_strikes_landed_pm",
        "Str.Acc.": "sig_strikes_accuracy",
        "SApM": "sig_strikes_abosrbed_pm",
        "Str.Def": "sig_strikes_defended",
        "TDAvg.": "takedown_avg_per15m",
        "TDAcc.": "takedown_accuracy",
        "TDDef.": "takedown_defence",
        "Sub.Avg.": "submission_avg_attempted_per15m",
    }
    
    cleaned_fighters = cleaned_fighters.rename(rename_cols, axis=1)
    cleaned_fighters = cleaned_fighters[rename_cols.values()]

    return cleaned_fighters





raw_events = read_scraped_events()
cleaned_events = clean_events(raw_events)

raw_fighters = read_scraped_fighters()
cleaned_fighters = clean_fighters(raw_fighters)