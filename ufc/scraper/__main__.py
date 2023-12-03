import string
import pandas as pd
import datetime
import argparse

from ufc import utils
from ufc.scraper.scrape_events import EventScraper
from ufc.scraper.scrape_fighters import FighterScraper
from ufc.scraper.scrape_odds import OddsScraper

def arg_parser():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--events",
        action="store_true",
        help="Run events scraper"
    )
    parser.add_argument(
        "--fighters",
        action="store_true",
        help="Run fighter scraper"
    )
    parser.add_argument(
        "--odds",
        action="store_true",
        help="Run odds scraper"
    )

    args = parser.parse_args()

    return args


if __name__ == "__main__":

    args = arg_parser()

    ######## Scrape individual UFC fighter data ########

    if args.fighters:
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

    if args.events:
        print("-- Scraping event result data...")
        event_scraper = EventScraper()

        event_scraper.get_individual_event_urls()
        event_scraper.scrape_all_event_urls()

        print("-- Writing event data...")
        event_scraper.write_data()


    ######## Scrape historic UFC odds ########

    if args.odds:
        print("-- Scraping odds data...")
        odds_scraper = OddsScraper()
        odds_scraper.get_individual_event_urls()
        odds_scraper.scrape_all_event_odds()

        print("-- Writing odds data...")
        odds_scraper.write_data()

