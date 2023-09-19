import pandas as pd
import numpy as np
import requests
import re
from bs4 import BeautifulSoup

def get_soup(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    return soup

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
        soup
        .find("span", class_="b-content__title-highlight")
        .text
        .strip()
    )

    # parse fight record
    fight_record = (
        soup
        .find("span", class_="b-content__title-record")
        .text
        .strip()
    )

    # parse nickname
    nickname = (
        soup
        .find("p", class_="b-content__Nickname")
        .text
        .strip()
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


# fighters_stats_url = "http://ufcstats.com/statistics/fighters?page=all"
# soup = get_soup(fighters_stats_url)

# fighters_individual_url = get_individual_fighter_urls(soup)

# fighter_url = fighters_individual_url[3]
# fighter_stats = get_fighter_stats(fighter_url)


