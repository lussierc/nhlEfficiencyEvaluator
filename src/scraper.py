"""Scrapes and saves play-by-play NHL data from the NHL API."""

import requests
import pickle


def run_scraper():
    """Get user scraping settings."""

    print("ENTER SCRAPING INFO:")

    # Set up the API call variables:
    year = input("* Enter year: ")
    print("Season types: 01 = Preseason, 02 = Reg Season, 03 = Postseason/Playoffs")
    season_type = input("* Choose season type: ")
    max_game_ID = int(input("* Enter max number of games to scrape data for: "))
    export_file_name = input("* Enter the name of your export (.pkl) file: ")

    # examples: # year = "2019"  # season_type = "02" # max_game_ID = 1290

    scrape_data(year, season_type, max_game_ID, export_file_name)


def scrape_data(year, season_type, max_game_ID, export_file_name):
    """Scrapes data."""

    game_data = []  # will hold scraped play-by-play data

    print("SCRAPING YOUR DATA")

    # Loop over the counter and format the API call
    for i in range(0, max_game_ID):

        # TODO: add progres bar for scraping
        r = requests.get(
            url="http://statsapi.web.nhl.com/api/v1/game/"
            + year
            + season_type
            + str(i).zfill(4)
            + "/feed/live"
        )
        data = r.json()
        game_data.append(data)

    print("DATA HAS BEEN SCRAPED")

    print("SAVING YOUR DATA")

    with open(export_file_name, "wb") as f:
        pickle.dump(game_data, f, pickle.HIGHEST_PROTOCOL)


run_scraper()  # runs the scraper
