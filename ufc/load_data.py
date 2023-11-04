import pandas as pd

def read_scraped_events():
    return pd.read_csv("./data/events_raw.csv")

def read_scraped_fighters():
    return pd.read_csv("./data/fighters_raw.csv")

def read_prepped_data():
    return pd.read_csv("./data/all_data_final.csv")