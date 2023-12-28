
# import pandas as pd
# import numpy as np

# from ufc import constants

# def extract_features(cleaned_odds, cleaned_fighters) -> pd.DataFrame():

#     # Drop inf rows
#     odds_df = odds_df[
#         ~(
#             (odds_df["fighter1_odds"] == np.inf) | (odds_df["fighter2_odds"] == np.inf)
#         )
#     ]

#     # Drop draws and no contests
#     odds_df = odds_df[odds_df["result"] != "-"]


# cleaned_events: take weight_class, outcome is more complete for draw and N/C
# cleaned_odds: take favourite, underdog, and odds
#   join to cleaned_events on event_name and winner of fight
# cleaned_fighters: take all fighter attributes

# events_labels = pd.DataFrame(cleaned_events["event_name"].unique(), columns=["events"])
# odds_labels = pd.DataFrame(cleaned_odds["event"].unique(), columns=["odds"])

# pd.concat([events_labels, odds_labels], axis=1)\
#     .to_csv("./data/match_labels.csv", index=False)