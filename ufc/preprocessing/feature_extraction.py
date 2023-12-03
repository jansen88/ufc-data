"""
Feature extraction steps
- Combine (clean) scraped data to extract features
- Extract features available from data without additional calculation steps

In more detail:
- Take clean fighters and events data
- Because we are predicting response outcome = "fighter1" or "fighter2",
need to randomly shuffle fighter1 and fighter 2 data from events results -
by default fighter1 is always the winner.
- Map features from fighter stats from fighters onto fighter1 and fighter2,
renamed as fighter1_*, fighter2_*
    - See code for detail of stats kept as features
- Drop missing values

"""

import pandas as pd
import numpy as np
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

from ufc import constants

# def extract_features(cleaned_odds, cleaned_fighters) -> pd.DataFrame():

    # # Drop inf rows
    # odds_df = odds_df[
    #     ~(
    #         (odds_df["fighter1_odds"] == np.inf) | (odds_df["fighter2_odds"] == np.inf)
    #     )
    # ]

    # # Drop draws and no contests
    # odds_df = odds_df[odds_df["result"] != "-"]


# cleaned_events: take weight_class, outcome is more complete for draw and N/C
# cleaned_odds: take favourite, underdog, and odds
#   join to cleaned_events on event_name and winner of fight
# cleaned_fighters: take all fighter attributes

# events_labels = pd.DataFrame(cleaned_events["event_name"].unique(), columns=["events"])
# odds_labels = pd.DataFrame(cleaned_odds["event"].unique(), columns=["odds"])



def prep_data_for_modelling(cleaned_events, cleaned_fighters) -> pd.DataFrame:
    # Filter to more recent years
    # HYPOTHESIS TO CONFIRM - more recent years more relevant
    df = cleaned_events[cleaned_events["event_date"].dt.year >= constants.KEEP_YEAR]

    # Filter to only outcome where there was a winner - lose ~3% rows
    df = df[df.outcome == "fighter1"]

    # Randomly sample to choose swap fighter1 and fighter2 so response
    # is not only fighter1
    np.random.seed(seed=constants.SEED)
    df["swap_fighter"] = np.random.choice(
        ["fighter1", "fighter2"],
        size=len(df)
    )

    # Swap fighter1, fighter2
    swap_idx = df[df["swap_fighter"] == "fighter2"].index
    df.loc[swap_idx,['fighter1','fighter2']] = df.loc[swap_idx,['fighter2','fighter1']].values
    df["outcome"] = df["swap_fighter"]

    # Fetch fighter1, fighter2 stats from fighters
    keep_attributes = [
        'height',
        'curr_weight',
        "dob",
        'reach',
        'stance',
        'sig_strikes_landed_pm',
        'sig_strikes_accuracy',
        'sig_strikes_absorbed_pm',
        'sig_strikes_defended',
        'takedown_avg_per15m',
        'takedown_accuracy',
        'takedown_defence',
        'submission_avg_attempted_per15m'
    ]

    fighter1 = cleaned_fighters.copy()
    rename_fighter1_dict = {x:f"fighter1_{x}" for x in keep_attributes}
    fighter1.rename(rename_fighter1_dict, axis=1, inplace=True)

    fighter2 = cleaned_fighters.copy()
    rename_fighter2_dict = {x:f"fighter2_{x}" for x in keep_attributes}
    fighter2.rename(rename_fighter2_dict, axis=1, inplace=True)

    df = (
        df
        .merge(
            fighter1,
            how="left",
            left_on="fighter1",
            right_on="name"
        )
        .merge(
            fighter2,
            how="left",
            left_on="fighter2",
            right_on="name"
        )
    )

    # Subset columns
    df = df[
            [
                # index
                "event_date",
                "fighter1",
                "fighter2",

                # response
                "outcome",

                # features
                "weight_class",
            ] +
            [f"fighter1_"+x for x in keep_attributes] +
            [f"fighter2_"+x for x in keep_attributes]
        ]

    # Drop rows with missing values
    # Checked these are expected - so happy to drop all
    print("Checking for missing values and dropping...")
    print(df.isnull().sum())

    df = df.dropna(axis=0)

    return df







