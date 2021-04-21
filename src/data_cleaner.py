"""Cleans the scraped data by calculating player statistics."""

import numpy as np
import pandas as pd
import pickle
import matplotlib
import matplotlib.pyplot as plt

color_map = plt.cm.winter
from matplotlib.patches import RegularPolygon
import math
import itertools
from collections import Counter
import itertools


def main():
    """Runs the data cleaner."""

    file_name = input("** Please Enter your '.pkl' filename: ")
    try:
        with open(file_name, "rb") as f:
            game_data = pickle.load(f)
    except:
        print("ERROR IN FILENAME")
        quit()

    all_teams = {
        "Anaheim Ducks": {},
        "Arizona Coyotes": {},
        "Boston Bruins": {},
        "Buffalo Sabres": {},
        "Calgary Flames": {},
        "Carolina Hurricanes": {},
        "Chicago Blackhawks": {},
        "Colorado Avalanche": {},
        "Columbus Blue Jackets": {},
        "Dallas Stars": {},
        "Detroit Red Wings": {},
        "Edmonton Oilers": {},
        "Florida Panthers": {},
        "Los Angeles Kings": {},
        "Minnesota Wild": {},
        "Montréal Canadiens": {},
        "Nashville Predators": {},
        "New Jersey Devils": {},
        "New York Islanders": {},
        "New York Rangers": {},
        "Ottawa Senators": {},
        "Philadelphia Flyers": {},
        "Pittsburgh Penguins": {},
        "San Jose Sharks": {},
        "St. Louis Blues": {},
        "Tampa Bay Lightning": {},
        "Toronto Maple Leafs": {},
        "Vancouver Canucks": {},
        "Vegas Golden Knights": {},
        "Washington Capitals": {},
        "Winnipeg Jets": {},
    }

    for data in game_data:
        if "liveData" in data:
            home_team, home_team_name, away_team, away_team_name = get_game_data(data)
            if all_teams[home_team_name]:
                # there is data now we need to converge them
                # if a player key is not in .keys() then you got to add that as a new player on the team
                # if a player is in .keys() we need to find a way to converge them

                for game_player_key in home_team.keys():
                    if game_player_key not in all_teams[home_team_name].keys():
                        # if a player does not exist on team, add them to it:
                        all_teams[home_team_name][game_player_key] = home_team[
                            game_player_key
                        ]
                    elif game_player_key in all_teams[home_team_name].keys():
                        if all_teams[home_team_name][game_player_key]["stats"] == "":
                            # if a player exists but does not have any statistics yet, give them first game stats:
                            all_teams[home_team_name][game_player_key] = home_team[
                                game_player_key
                            ]
                        else:
                            # converge stats from new/current game with season stats
                            season_dict = all_teams[home_team_name][game_player_key][
                                "stats"
                            ]
                            new_game_dict = home_team[game_player_key]["stats"]

                            combo = Counter(season_dict)
                            combo.update(Counter(new_game_dict))

                            all_teams[home_team_name][game_player_key]["stats"] = combo
                    else:
                        print("Error")
            else:
                # there is no current version of the team, add them to their season-long dict of all teams:
                all_teams[home_team_name] = home_team

            if all_teams[away_team_name]:
                # there is data now we need to converge them
                # if a player key is not in .keys() then you got to add that as a new player on the team
                # if a player is in .keys() we need to find a way to converge them

                for game_player_key in away_team.keys():
                    if game_player_key not in all_teams[away_team_name].keys():
                        # if a player does not exist on team, add them to it:
                        all_teams[away_team_name][game_player_key] = away_team[
                            game_player_key
                        ]
                    elif game_player_key in all_teams[away_team_name].keys():
                        if all_teams[away_team_name][game_player_key]["stats"] == "":
                            # if a player exists but does not have any statistics yet, give them first game stats:
                            all_teams[away_team_name][game_player_key] = away_team[
                                game_player_key
                            ]
                        else:
                            # converge stats from new/current game with season stats
                            season_dict = all_teams[away_team_name][game_player_key][
                                "stats"
                            ]
                            new_game_dict = away_team[game_player_key]["stats"]
                            combo = Counter(season_dict)
                            combo.update(Counter(new_game_dict))

                            all_teams[away_team_name][game_player_key]["stats"] = combo
                    else:
                        print("Error")
            else:
                # there is no current version of the team, add them to their season-long dict of all teams:
                all_teams[away_team_name] = away_team

    for key in all_teams.keys():
        print("---------------------------------------")
        print("TEAM: ", key)
        print(all_teams[key])
        print("---------------------------------------\n\n\n\n")


def get_game_data(data):
    if "liveData" in data:
        game_teams = data["liveData"]["boxscore"]["teams"]

        home_team_name = game_teams["home"]["team"]["name"]
        home_team = {}
        home_team_players = game_teams["home"]["players"]

        away_team_name = game_teams["away"]["team"]["name"]
        away_team = {}
        away_team_players = game_teams["away"]["players"]

        teams = {'home_team': {'name': home_team_name, 'players': home_team_players, 'finalized_roster': {}}, 'away_team': {'name': away_team_name, 'players': away_team_players, 'finalized_roster': {}}}

        for team in teams.keys():
            team_name = teams[team]['name']
            team_players = teams[team]['players']

            for key in team_players.keys():
                player = team_players[key]
                player_name = player["person"]["fullName"]
                player_postition = player["position"]["name"]
                player_dict = {
                    "id": key,
                    "name": player_name,
                    "position": player_postition,
                    "stats": "",
                }
                print(player_dict)
                player_stats = player["stats"]

                if player_stats:
                    # not empty perform work
                    if "skaterStats" in player_stats.keys():
                        player_dict["stats"] = player_stats["skaterStats"]

                        player_dict["stats"]["timeOnIce"] = int(
                            player_dict["stats"]["timeOnIce"].split(":")[0]
                        )
                        player_dict["stats"]["evenTimeOnIce"] = int(
                            player_dict["stats"]["evenTimeOnIce"].split(":")[0]
                        )
                        player_dict["stats"]["powerPlayTimeOnIce"] = int(
                            player_dict["stats"]["powerPlayTimeOnIce"].split(":")[0]
                        )
                        player_dict["stats"]["shortHandedTimeOnIce"] = int(
                            player_dict["stats"]["shortHandedTimeOnIce"].split(":")[0]
                        )
                        player_dict["stats"]["gp"] = 1
                    elif "goalieStats" in player_stats.keys():
                        player_dict["stats"] = player_stats["goalieStats"]

                        player_dict["stats"]["timeOnIce"] = int(
                            player_dict["stats"]["timeOnIce"].split(":")[0]
                        )

                        if player_dict["stats"]["decision"] == "L":
                            player_dict["stats"]["losses"] = 1
                        elif player_dict["stats"]["decision"] == "W":
                            player_dict["stats"]["wins"] = 1
                        else:
                            pass
                        player_dict["stats"].pop("decision")

                        player_dict["stats"]["gp"] = 1
                    else:
                        print("ERROR")
                else:
                    pass

                teams[team]['finalized_roster'][key] = player_dict

    home_team = teams['home_team']['finalized_roster']

    away_team = teams['away_team']['finalized_roster']

    return home_team, home_team_name, away_team, away_team_name


main()
