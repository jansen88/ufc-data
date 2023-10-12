from ufc import load_data, constants
from ufc.preprocessing import clean_scraped_data as clean_data
from ufc.preprocessing import prep_data, feature_eng

if __name__ == "__main__":

    raw_events = load_data.read_scraped_events()
    cleaned_events = clean_data.clean_events(raw_events)
    cleaned_events.to_csv("./data/cleaned_events.csv", index=False)
    
    raw_fighters = load_data.read_scraped_fighters()
    cleaned_fighters = clean_data.clean_fighters(raw_fighters)
    cleaned_events.to_csv("./data/cleaned_fighters.csv", index=False)
    
    prepped_data = prep_data.prep_data_for_modelling(cleaned_events, cleaned_fighters)
    
    final_df = feature_eng.derive_features(prepped_data)

    final_df.to_csv("./data/prepped_ufc_data.csv", index=False)
