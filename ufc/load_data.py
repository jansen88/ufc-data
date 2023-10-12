import pandas as pd

def read_scraped_events():
    return pd.read_csv("./data/event_results.csv")

def read_scraped_fighters():
    return pd.read_csv("./data/fighter_stats.csv")

def read_prepped_data():
    return pd.read_csv("./data/prepped_ufc_data.csv")