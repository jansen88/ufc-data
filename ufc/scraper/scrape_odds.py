"""
Scrape historic UFC odds from betmma.tips

The work below draws upon another data scientist's work here in identifying an appropriate site to scrape
odds from as well as some logic to scrape required elements.
    https://github.com/jasonchanhku/web_scraping/blob/master/MMA%20Project/favourite_vs_underdogs.R

This required significant effort of my own to rewrite in Python (instead of R) and also convert to 
appropriate pipeline-ready code, as well as significant updates to logic which was no longer working correctly 
for latest event pages - i.e., updating the logic to correctly fetch fighter1, fighter2 and result.

Known issues:
    - Takes loooong time to run for newer pages, which record how punters from the site performed in
        addition to the match results we care about
"""

import pandas as pd
import datetime

import requests
from bs4 import BeautifulSoup

from ufc import utils

class OddsScraper():
    """Scrape historic odds from betmma.tips"""
    def __init__(self, test=False):
        self.test = test
        self.all_url = "http://www.betmma.tips/mma_betting_favorites_vs_underdogs.php?Org=1"
        self.event_links = None
        self.event_odds = None
        self.curr_time = datetime.datetime.now()

    def get_individual_event_urls(self):
        """Get all individual urls"""
        response = requests.get(self.all_url)
        soup = BeautifulSoup(response.text, 'html.parser')

        links = [f"http://www.betmma.tips/{a['href']}" for a in soup.select("td td td td a")]

        self.event_links = links

    def scrape_all_event_odds(self):
        """Iterate over all individual urls to scrape odds"""

        scraped_results = []

        for i, event_url in enumerate(self.event_links):

            print(f"{i+1}/{len(self.event_links)} - {event_url}")

            results = self._scrape_event_odds_page(event_url)
            scraped_results.append(results)

            utils.sleep_randomly()

        odds_df = pd.concat(scraped_results).reset_index(drop=True)

        odds_df["timestamp"] = self.curr_time

        self.event_odds = odds_df

    def write_data(self):
        self.event_odds.to_csv("./data/odds_raw.csv", index=False)

    def _scrape_event_odds_page(self, link):

        sub_response = requests.get(link)
        sub_soup = BeautifulSoup(sub_response.text, 'html.parser')

        event = []
        fighter1 = []
        fighter2 = []
        fighter1_odds = []
        fighter2_odds = []
        result = []

        # Get fighter names and winner from a tags - no ids or classes to work with
        # so have to do this way
        # - Get all fighter profile links
        # - First one should be fighter1
        # - Second one should be fighter2
        # - Next should give result - but where it is neither fighter1 or fighter2 
        #   and is a new fighter, this is because a draw or N/C was returned
        #   so assume it is a new fighter1
        fighters = [a.get_text() for a in sub_soup.select("a") \
                    if "fighter_profile" in a.get("href")]

        increment = "fighter1"

        for i in fighters:
            
            if increment == "fighter1":
                fighter1.append(i)
                increment = "fighter2"

            elif increment == "fighter2":
                fighter2.append(i)
                increment = "result"
            else:
                # draw - skip to next fight
                if (i not in fighter1) and (i not in fighter2):
                    result.append("-")
                    fighter1.append(i)
                    increment = "fighter2"
                else:
                    result.append(i)
                    increment = "fighter1"

        # Handling for edge case - last fight on list is a draw
        if len(result) == len(fighter1) - 1:
            print("Edge case - appending '-' to result")
            result.append("-")

        # Event
        event_t = sub_soup.select("td h1")[0].get_text()
        event.extend([event_t] * len(fighter1))

        # Label
        # Known issue - for later pages, this takes a loooong time (10mins+)
        # as many tags to search through
        label_t = [td.get_text() for td in sub_soup.select("td td td td tr~ tr+ tr td")]
        label_cleansed = [t.replace("@", "").strip() for t in label_t]

        # Fighter1 odds
        fighter1_odds_t = label_cleansed[0::2]
        fighter1_odds.extend(fighter1_odds_t)

        # Fighter2 odds
        fighter2_odds_t = label_cleansed[1::2]
        fighter2_odds.extend(fighter2_odds_t)

        return pd.DataFrame({
            "event": event,
            "fighter1": fighter1,
            "fighter2": fighter2,
            "fighter1_odds": fighter1_odds,
            "fighter2_odds": fighter2_odds,
            "result": result
        })



