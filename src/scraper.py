import requests
import pickle

# Set up the API call variables
game_data = []
year = "2019"
season_type = "02"
max_game_ID = 1290

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

with open("./" + year + "my_dataset.pkl", "wb") as f:
    pickle.dump(game_data, f, pickle.HIGHEST_PROTOCOL)
