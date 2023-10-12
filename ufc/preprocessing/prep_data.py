"""
Data prep steps before modelling
- Take clean fighters and events data
- Because we are predicting response outcome = "fighter1" or "fighter2",
need to randomly shuffle fighter1 and fighter 2 data from events results -
by default fighter1 is always the winner.
- Map features from fighter stats from fighters onto fighter1 and fighter2,
renamed as fighter1_*, fighter2_*
    - See code for detail of stats kept as features
- Drop missing values

TODO
- Add fighter record prior to fight as feature

"""

import pandas as pd
import numpy as np

from ufc import constants


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
    features = [
        'curr_height',
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
    keep_but_not_features = [
        'dob'
    ]

    fighter1 = cleaned_fighters.copy()
    rename_fighter1_dict = {x:f"fighter1_{x}" for x in features + keep_but_not_features}
    fighter1.rename(rename_fighter1_dict, axis=1, inplace=True)

    fighter2 = cleaned_fighters.copy()
    rename_fighter2_dict = {x:f"fighter2_{x}" for x in features + keep_but_not_features}
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

    ### Additional feature engineering
    df["fighter1_age"] = df["event_date"].dt.year - df["fighter1_dob"].dt.year
    df["fighter2_age"] = df["event_date"].dt.year - df["fighter2_dob"].dt.year

    additional_features = ["age"]

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
            [f"fighter1_"+x for x in features+additional_features] +
            [f"fighter2_"+x for x in features+additional_features]
        ]
    
    # Drop rows with missing values
    # Checked these are expected - so happy to drop all
    print("Checking for missing values and dropping...")
    print(df.isnull().sum())

    df = df.dropna(axis=0)

    return df





