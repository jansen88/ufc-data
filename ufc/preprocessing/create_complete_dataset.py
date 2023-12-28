

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from ufc import constants


def add_fighter_attributes(
        df: pd.DataFrame,
        cleaned_fighters: pd.DataFrame,
        keep_attributes: list
) -> pd.DataFrame:

    """add fighter1 and fighter2 attributes to df"""

    fighter1 = cleaned_fighters.copy()
    rename_fighter1_dict = {x:f"fighter1_{x}" for x in keep_attributes}
    fighter1 = fighter1[["name"] + keep_attributes]
    fighter1.rename(rename_fighter1_dict, axis=1, inplace=True)

    fighter2 = cleaned_fighters.copy()
    rename_fighter2_dict = {x:f"fighter2_{x}" for x in keep_attributes}
    fighter2 = fighter2[["name"] + keep_attributes]
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
        .assign(fighter_extract_ts = cleaned_fighters.timestamp[0])
        .drop(["name_x", "name_y"], axis=1)
    )

    return df


def combine_all_datasets(cleaned_events, cleaned_odds, cleaned_fighters):
    """
    a. Join events to odds data first
        - Left join
        - Will lose odds where names don't match or older years where don't have odds
    b. Then join fighter1, fighter2 attributes from fighters onto events
    """

    # Rename cols
    cleaned_events.rename(
        {"timestamp": "events_extract_ts"},
        axis=1, inplace=True
    )
    cleaned_odds.rename(
        {
            "timestamp": "odds_extract_ts",
            "date": "event_date",
            "outcome": "betting_outcome",
        },
        axis=1, inplace=True
    )

    ### a. Join events to odds on event date and fighter names
    def combine_fighter_names(row, fighter1, fighter2):
        if row[fighter1] < row[fighter2]:
            return row[fighter1] + ' - ' + row[fighter2]
        else: 
            return row[fighter2] + ' - ' + row[fighter1]


    cleaned_events["match_name"] = cleaned_events.apply(
        combine_fighter_names, args=("fighter1", "fighter2"),
        axis=1
    )

    cleaned_odds["match_name"] = cleaned_odds.apply(
        combine_fighter_names, args=("favourite", "underdog"),
        axis=1
    )

    # NOTE - concatenating names doesn't produce 100% match rate;
    # some differences e.g. "Jr." vs "Jr", non-Anglo names e.g. "Un" vs
    # "Woong"
    # Lose about 15%
    # TODO - explore fuzzy join

    # join odds onto events
    complete_df = pd.merge(
        cleaned_events,
        cleaned_odds[[
                        "event_date", "match_name",
                            "favourite", "underdog",
                            "favourite_odds", "underdog_odds", "betting_outcome",
                            "odds_extract_ts"
                    ]],
        on = ["event_date", "match_name"],
        how="left"
    )

    # check where odds didn't match onto event details
    # complete_df[complete_df.odds_extract_ts.isna()]

    ### b. Fetch fighter1, fighter2 stats from fighters
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

    complete_df = add_fighter_attributes(complete_df, cleaned_fighters, keep_attributes)

    # reorder columns
    complete_df = complete_df[
        [
            "event_date",
            "event_name",
            "weight_class",
            "fighter1",
            "fighter2",
            "favourite",
            "underdog",
            "favourite_odds",
            "underdog_odds",
            "betting_outcome", # retain both to make querying a bit easier
            "outcome",
            "method",
            "round",
        ] + 

        [f"fighter1_{x}" for x in keep_attributes] +

        [f"fighter2_{x}" for x in keep_attributes] + 

        [
            "events_extract_ts",
            "odds_extract_ts",
            "fighter_extract_ts"
        ]
    ]

    return complete_df

def check_odds_completeness(complete_df):
    complete_df["year"] = complete_df.event_date.dt.year

    check_na = (
        complete_df
        .groupby("year", as_index=False)
        .agg(
            na = ("odds_extract_ts", lambda x: x.isna().sum()),
            N = ("events_extract_ts", lambda x: x.count()),
        )
    )

    fig, ax = plt.subplots(figsize=(10, 6))    
    ax.bar(check_na['year'], check_na['na'], color="red", label="Odds missing")
    ax.bar(check_na['year'], check_na['N'], color="black", label = "Total events", alpha = 0.2)
    ax.legend()

    return fig