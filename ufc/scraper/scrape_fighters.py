"""Scrape individual fighter info and career statistics"""

import pandas as pd
import numpy as np
import datetime
import string

from ufc import utils

class FighterScraper():
    """Scrape individual fighter info and career stats"""

    def __init__(self, test=False):
        self.test = test
        self.fighters_individual_url = None
        self.curr_time = datetime.datetime.now()

    ### Key methods for pipeline

    def get_all_individual_fighter_urls(self):
        """
        Each page lists all fighters by initial of surnamee
        Iterate through each index page to get urls for all individual fighters
        """

        letters = list(string.ascii_lowercase)
        pages = [
            f"http://ufcstats.com/statistics/fighters?char={letter}&page=all" for letter in letters
        ]

        fighters_individual_url = []

        for page_url in pages:
            soup = utils.get_soup(page_url)
            fighters_individual_url = fighters_individual_url + self._get_individual_fighter_urls(soup)
            utils.sleep_randomly()

        self.fighters_individual_url = fighters_individual_url

    def scrape_individual_fighter_urls(self):
        """Iterate through urls for individual fighters to scrape individual fighter career stats"""

        dfs_list = []

        if self.test:
            fighters_individual_url = self.fighters_individual_url[0:10]
        else: 
            fighters_individual_url = self.fighters_individual_url

        for index, fighter_url in enumerate(fighters_individual_url):
            fighter_stats = pd.DataFrame(
                self._get_fighter_stats(fighter_url),
                index=[0]
            )
            dfs_list.append(fighter_stats)

            print(f"{fighter_stats.name[0]} ✔️ ({index+1} of {len(fighters_individual_url)})")

            utils.sleep_randomly()

        fighter_stats_df = pd.concat(dfs_list).reset_index(drop=True)
        fighter_stats_df["timestamp"] =  self.curr_time

        self.fighter_stats_df = fighter_stats_df

    def write_data(self):
        self.fighter_stats_df.to_csv("./data/fighters_raw.csv", index=False)


    ### Helper methods

    def _get_individual_fighter_urls(self, soup):
        """Scrape individual fighter urls from single index page"""

        # links all underlined
        fighters_individual_url = []

        link_elements = soup.find_all("a", class_="b-link b-link_style_black")
        for link in link_elements:
            if link["href"] not in fighters_individual_url:
                fighters_individual_url.append(link["href"])

        return fighters_individual_url 

    def _get_fighter_stats(self, fighter_url) -> dict:
        """From individual fighter url, scrape key stats"""

        def _clean_fighter_stat_str(string):
            return (
                string
                .text
                .strip()
                .replace("\n", "")
                .replace(" ", "")
                .replace('\\', '')
            )

        soup = utils.get_soup(fighter_url)

        # parse fighter name
        fighter_name = (
            soup.find("span", class_="b-content__title-highlight").text.strip()
        )

        # parse fight record
        fight_record = (
            soup
            .find("span", class_="b-content__title-record")
            .text
            .strip()
            .replace("Record: ", "")
        )

        # parse nickname
        nickname = (
            soup.find("p", class_="b-content__Nickname").text.strip()
        )

        # collect to dict
        fighter_stats_dict = {
            "name": fighter_name,
            "fight_record": fight_record,
            "nickname": nickname,
        }

        # parse all other fighter details
        all = (
            soup
            .find_all("li", class_="b-list__box-list-item b-list__box-list-item_type_block")
        )

        fighter_stats_list = [_clean_fighter_stat_str(x) for x in all]
        add_dict = {item.split(":")[0]: item.split(":")[1] for item in fighter_stats_list if ":" in item}

        # append other fighter details to one dict
        fighter_stats_dict.update(add_dict)

        return fighter_stats_dict
