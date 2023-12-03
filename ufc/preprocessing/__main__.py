from ufc import load_data, constants
from ufc.preprocessing import clean_raw_data as clean_data
from ufc.preprocessing import feature_extraction, feature_engineering

if __name__ == "__main__":

    raw_events = load_data.read_scraped_events()
    cleaned_events = clean_data.clean_events(raw_events)
    # cleaned_events.to_csv("./data/cleaned_events.csv", index=False)
    
    raw_fighters = load_data.read_scraped_fighters()
    cleaned_fighters = clean_data.clean_fighters(raw_fighters)
    # cleaned_events.to_csv("./data/cleaned_fighters.csv", index=False)

    raw_odds = load_data.read_scraped_odds()
    cleaned_odds = clean_data.clean_odds(raw_odds)
    # cleaned_odds.to_csv("./data/cleaned_odds.csv", index=False)
    
    prepped_data = feature_extraction.prep_data_for_modelling(cleaned_events, cleaned_fighters)
    
    final_df = feature_engineering.derive_features(prepped_data)

    final_df.to_csv("./data/all_data_final.csv", index=False)
