import string
import pandas as pd
import datetime

from ufc import utils
from ufc.scraper.scrape_events import EventScraper
from ufc.scraper.scrape_fighters import FighterScraper


if __name__ == "__main__":

    ######## Scrape individual UFC fighter data ########

    print("Running scraper...")
    fighter_scraper = FighterScraper()

    print("-- Scraping individual fighter data...")
    print("---- Fetching individual fighter pages from index pages...")
    fighter_scraper.get_all_individual_fighter_urls()

    print("---- Now scraping from fighter pages...")
    fighter_scraper.scrape_individual_fighter_urls()

    print("-- Writing fighter data...")
    fighter_scraper.write_data()


    ######## Scrape historic UFC events results ########

    print("-- Scraping event result data...")
    event_scraper = EventScraper()

    event_scraper.get_individual_event_urls()
    event_scraper.scrape_all_event_urls()

    print("-- Writing event data...")
    event_scraper.write_data()
