"""
Scrape historic UFC odds from betmma.tips

The work below draws lightly upon another data scientist's work here in identifying an appropriate site to 
scrape odds from as well as some logic to scrape required elements.
    https://github.com/jasonchanhku/web_scraping/blob/master/MMA%20Project/favourite_vs_underdogs.R

This required significant additional effort of my own to rewrite in Python (instead of R), scrape from a 
different page (above work scrapes from a page missing some events), write appropriate pipeline-ready code, 
as well as significant updates to logic which was no longer working correctly  for latest event pages 
- e.g., updating the logic to correctly fetch fighter1, fighter2 and result, improve logic to run faster

"""

import pandas as pd
import numpy as np
import datetime

import requests
from bs4 import BeautifulSoup

from ufc import utils

class OddsScraper():
    """Scrape historic odds from betmma.tips"""
    def __init__(self, test=False):
        self.test = test
        self.all_url = "https://www.betmma.tips/past_mma_handicapper_performance_all.php?Org=1"
        self.event_links = None
        self.event_odds = None
        self.curr_time = datetime.datetime.now()

    def get_individual_event_urls(self):
        """Get all individual urls"""
        response = requests.get(self.all_url)
        soup = BeautifulSoup(response.text, 'html.parser')

        links = [
                    f"http://www.betmma.tips/{a['href']}" for a in soup.select("td td td td a")
                ]
        
        # Also scrape full table to fetch dates as well - we need this
        # to join back onto UFC events as names don't match
        table = pd.read_html(response.text)[8] # FIXME - hard coded 8

        # set first row as col headers
        table.columns = table.iloc[0]
        table = table[1:-1]
        table["url"] = links
        table = table[["Date", "Event", "url"]]

        # filter to UFC events only
        table = table[
            table.Event.str.contains("UFC") &
            ~table.Event.str.contains("Road to UFC")
        ].reset_index()

        self.event_links = table

    def scrape_all_event_odds(self):
        """Iterate over all individual urls to scrape odds"""

        scraped_results = []

        table = self.event_links

        for i, row in table.iterrows():
            print(f"{i+1}/{len(table)} - {row.Date} - {row.url}")

            results = self._scrape_event_odds_page(row.url)
            results["link"] = row.url
            results["date"] = row.Date
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
        # Exact match is sub_soup.select("td td td td tr~ tr+ tr td") but this
        # is very slow especially on large pages
        # This is less precise but works on pages I tested
        label_t = [
                    td.get_text() for td in sub_soup.select("td tr+ tr td") \
                    if (len(td.get_text()) <= 7) and \
                        "@" in td.get_text()
                ]


        label_cleansed = [t.replace("@", "").strip() for t in label_t]

        # Fighter1 odds
        fighter1_odds_t = label_cleansed[0::2]
        fighter1_odds.extend(fighter1_odds_t)

        # Fighter2 odds
        fighter2_odds_t = label_cleansed[1::2]
        fighter2_odds.extend(fighter2_odds_t)

        return pd.DataFrame({
            "link": np.nan,
            "date": np.nan,
            "event": event,
            "fighter1": fighter1,
            "fighter2": fighter2,
            "fighter1_odds": fighter1_odds,
            "fighter2_odds": fighter2_odds,
            "result": result
        })



