"""Scrapes and saves play-by-play NHL data from the NHL API."""

import requests
import pickle

print("ENTER SCRAPING INFO:")
game_data = []  # will hold scraped play-by-play data

# Set up the API call variables:
year = input("* Enter year: ")
print("Season types: 01 = Preseason, 02 = Reg Season, 03 = Postseason/Playoffs")
season_type = input("* Choose season type: ")
max_game_ID = int(input("* Enter max number of games to scrape data for: "))

# year = "2019"  # season/year
# season_type = "02"  # regular season, not pre-season or playoffs
# max_game_ID = 1290  # max num of games

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

with open("./" + year + "meeting_dataset.pkl", "wb") as f:
    pickle.dump(game_data, f, pickle.HIGHEST_PROTOCOL)
