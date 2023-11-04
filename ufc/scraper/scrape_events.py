"""Scrape historic event info"""

import pandas as pd
import numpy as np
import datetime
from ufc import utils


class EventScraper():
    """Scrape historic UFC event info"""

    def __init__(self, test=False):
        self.test = test
        self.completed_events_url = "http://ufcstats.com/statistics/events/completed?page=all"
        self.event_links = None
        self.event_results = None
        self.curr_time = datetime.datetime.now()


    def get_individual_event_urls(self):
        """Scrape index page for all events for individual event urls"""

        soup = utils.get_soup(self.completed_events_url)

        link_elements = soup.find_all("a", class_="b-link b-link_style_black")
        event_links = [i["href"] for i in link_elements]
        # event_names = [i.text.strip() for i in link_elements]

        self.event_links = event_links

    def scrape_all_event_urls(self):

        ## Scrape event results from each page
        results_list = []

        if self.test:
            event_links = self.event_links[0:10]
        else:
            event_links = self.event_links

        for index, event_url in enumerate(event_links):
            raw = self._get_raw_event_data(event_url)
            clean = self._clean_raw_event_results(raw)

            results_list.append(clean)

            print(f"{clean.event_name[0]} ✔️ ({index+1} of {len(self.event_links)})")

            utils.sleep_randomly()

        event_results = pd.concat(results_list).reset_index(drop=True)

        event_results["timestamp"] = self.curr_time

        self.event_results = event_results

    def write_data(self):
        self.event_results.to_csv("./data/events_raw.csv", index=False)

    def _get_raw_event_data(self, event_url) -> pd.DataFrame:
        """From individual event url, scrape raw event data to df"""

        soup = utils.get_soup(event_url)

        # parse event name
        event_name = soup.find("span", class_="b-content__title-highlight").text.strip()

        # parse event date and location
        fight_details = soup.find_all("li", class_="b-list__box-list-item")

        event_date = (
            fight_details[0]
            .text
            .replace("\n", "")
            .replace("Date:" , "")
            .replace(",", "")
            .strip()
        )

        event_location = (
            fight_details[1]
            .text
            .replace("\n", "")
            .replace("Location:" , "")
            .strip()
        )

        ### parse event results - table to pandas DataFrame
        table = soup.find("table", "b-fight-details__table")

        table_data = []

        # get table header
        col_names = []
        for header in table.find_all("th", class_="b-fight-details__table-col"):
            col_names.append(header.text.strip())

        # get table rows
        for row in table.find_all('tr'):
            row_data = []
            for cell in row.find_all('td'):
                row_data.append(
                    cell.text.strip().replace("\n", "")
                )
            table_data.append(row_data)

        # collect to pandas DataFrame
        table_data[0] = col_names
        event_results = pd.DataFrame(table_data)
        event_results.columns = event_results.iloc[0]
        event_results = event_results[1:]

        # add event details
        event_details = pd.DataFrame({
            "event_name": event_name,
            "event_date": event_date,
            "event_location": event_location
        }, index=[0])

        event_results["key"] = 0
        event_details["key"] = 0

        raw_event_results = event_details.merge(
            event_results,
            on="key"
        )

        raw_event_results.drop("key", axis=1, inplace=True)

        return raw_event_results

    def _clean_raw_event_results(self, raw_event_results) -> pd.DataFrame:

        event_results = raw_event_results.copy()

        # split Fighter col into two
        event_results[["fighter1", "fighter2"]] =\
            event_results["Fighter"].str.split("                          ", expand=True)

        event_results["outcome"] = np.select(
            condlist=[
                event_results["W/L"] == "win",
                event_results["W/L"] == "drawdraw",
                event_results["W/L"] == "ncnc"
            ],
            choicelist=[
                "fighter1",
                "Draw",
                "No contest"
            ],
            default=None
        )

        return event_results[[
            "event_name", "event_date", "event_location", "Weight class", "fighter1", "fighter2", "outcome",
            "Kd", "Str", "Td", "Sub", "Method", "Round", "Time"
        ]]

