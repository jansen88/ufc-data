"""
Features for modelling which require additional calculation steps

TODO
- Add fighter record prior to fight as feature

"""

import pandas as pd
import numpy as np

from ufc import constants

def derive_features(df) -> pd.DataFrame:

    df["fighter1_age"] = df["event_date"].dt.year - df["fighter1_dob"].dt.year
    df["fighter2_age"] = df["event_date"].dt.year - df["fighter2_dob"].dt.year

    compare_attributes = [
        'height',
        "age",
        'reach',
        'sig_strikes_landed_pm',
        'sig_strikes_accuracy',
        'sig_strikes_absorbed_pm',
        'sig_strikes_defended',
        'takedown_avg_per15m',
        'takedown_accuracy',
        'takedown_defence',
        'submission_avg_attempted_per15m'
    ]

    # compute delta between fighter1, fighter2 attributes
    for attribute in compare_attributes:
        df[f"delta_{attribute}"] = df[f"fighter1_{attribute}"] - df[f"fighter2_{attribute}"]

    # compute ratio between fighter1, fighter 2 attributes
    for attribute in compare_attributes:
        df[f"ratio_{attribute}"] = df[f"fighter1_{attribute}"] / df[f"fighter2_{attribute}"]

    # TODO - add win/loss for last X fights

    return df
