import pandas as pd
import numpy as np
import requests
import re
from bs4 import BeautifulSoup
import string
import random
import time

def get_soup(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    return soup

def sleep_randomly():
    """Sleep for some random time between requests"""
    sleep_time = np.random.uniform(2,4)
    time.sleep(sleep_time)

############## Scrape individual fighter info and career statistics ##############

def get_individual_fighter_urls(soup):
    """Scrape individual fighter urls from all fighters stats page"""

    # links all underlined
    fighters_individual_url = []

    link_elements = soup.find_all("a", class_="b-link b-link_style_black")
    for link in link_elements:
        if link["href"] not in fighters_individual_url:
            fighters_individual_url.append(link["href"])

    return fighters_individual_url 

def get_fighter_stats(fighter_url):
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

    soup = get_soup(fighter_url)

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


# TODO - move to a pipeline
# Each page lists all fighters by initial of surname
## Iterate through each index page to get urls for all individual fighters
letters = list(string.ascii_lowercase)
pages = [
    f"http://ufcstats.com/statistics/fighters?char={letter}&page=all" for letter in letters
]

fighters_individual_url = []

for page_url in pages:
    soup = get_soup(page_url)
    fighters_individual_url = fighters_individual_url + get_individual_fighter_urls(soup)
    sleep_randomly()

## Iterate through urls for individual fighters to scrape individual fighter career stats
dfs_list = []

for index, fighter_url in enumerate(fighters_individual_url[145:245]):
    fighter_stats = pd.DataFrame(
        get_fighter_stats(fighter_url),
        index=[0]
    )
    dfs_list.append(fighter_stats)

    print(f"{fighter_stats.name[0]} ✔️ ({index+1} of {len(fighters_individual_url)})")

    sleep_randomly()

fighter_stats_df = pd.concat(dfs_list)


############## Scrape historic event info ##############

def get_individual_event_urls(url):
    """Scrape index page for all events for individual event urls"""

    soup = get_soup(completed_events_url)

    link_elements = soup.find_all("a", class_="b-link b-link_style_black")
    event_links = [i["href"] for i in link_elements]
    # event_names = [i.text.strip() for i in link_elements]

    return event_links

def get_raw_event_data(event_url):
    """From individual event url, scrape raw event data to df"""

    soup = get_soup(event_url)

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

def clean_raw_event_results(raw_event_results):

    event_results = raw_event_results.copy()

    # split Fighter col into two
    event_results[["fighter1", "fighter2"]] =\
        event_results["Fighter"].str.split("                          ", expand=True)
    
    return event_results


completed_events_url = "http://ufcstats.com/statistics/events/completed?page=all"
event_links = get_individual_event_urls(completed_events_url)

event_url = event_links[0]
raw_event_results = get_raw_event_data(event_url)




