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
                            if game_player_key == "ID8471675":
                                print(game_player_key)
                                print("1", season_dict)
                                print("2", new_game_dict)
                                print("3", combo)

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
                            if game_player_key == "ID8471675":
                                print(game_player_key)
                                print("1", season_dict)
                                print("2", new_game_dict)
                                print("3", combo)

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

        for key in home_team_players.keys():
            player = home_team_players[key]
            player_name = player["person"]["fullName"]
            player_postition = player["position"]["name"]
            cur_player = {
                "name": player_name,
                "stats": "",
                "position": player_postition,
            }
            player_stats = player["stats"]

            if player_stats:
                # not empty perform work
                if "skaterStats" in player_stats.keys():
                    cur_player["stats"] = player_stats["skaterStats"]

                    cur_player["stats"]["timeOnIce"] = int(
                        cur_player["stats"]["timeOnIce"].split(":")[0]
                    )
                    cur_player["stats"]["evenTimeOnIce"] = int(
                        cur_player["stats"]["evenTimeOnIce"].split(":")[0]
                    )
                    cur_player["stats"]["powerPlayTimeOnIce"] = int(
                        cur_player["stats"]["powerPlayTimeOnIce"].split(":")[0]
                    )
                    cur_player["stats"]["shortHandedTimeOnIce"] = int(
                        cur_player["stats"]["shortHandedTimeOnIce"].split(":")[0]
                    )
                    cur_player["stats"]["gp"] = 1
                elif "goalieStats" in player_stats.keys():
                    cur_player["stats"] = player_stats["goalieStats"]

                    cur_player["stats"]["timeOnIce"] = int(
                        cur_player["stats"]["timeOnIce"].split(":")[0]
                    )

                    if cur_player["stats"]["decision"] == "L":
                        cur_player["stats"]["losses"] = 1
                    elif cur_player["stats"]["decision"] == "W":
                        cur_player["stats"]["wins"] = 1
                    else:
                        pass
                    cur_player["stats"].pop("decision")

                    cur_player["stats"]["gp"] = 1
                else:
                    print("ERROR")
            else:
                pass

            home_team[key] = cur_player

        for key in away_team_players.keys():
            player = away_team_players[key]
            player_name = player["person"]["fullName"]
            player_postition = player["position"]["name"]
            cur_player = {
                "name": player_name,
                "stats": "",
                "position": player_postition,
            }
            player_stats = player["stats"]

            if player_stats:
                # not empty perform work
                if "skaterStats" in player_stats.keys():
                    cur_player["stats"] = player_stats["skaterStats"]

                    cur_player["stats"]["timeOnIce"] = int(
                        cur_player["stats"]["timeOnIce"].split(":")[0]
                    )
                    cur_player["stats"]["evenTimeOnIce"] = int(
                        cur_player["stats"]["evenTimeOnIce"].split(":")[0]
                    )
                    cur_player["stats"]["powerPlayTimeOnIce"] = int(
                        cur_player["stats"]["powerPlayTimeOnIce"].split(":")[0]
                    )
                    cur_player["stats"]["shortHandedTimeOnIce"] = int(
                        cur_player["stats"]["shortHandedTimeOnIce"].split(":")[0]
                    )
                    cur_player["stats"]["gp"] = 1
                elif "goalieStats" in player_stats.keys():
                    cur_player["stats"] = player_stats["goalieStats"]

                    cur_player["stats"]["timeOnIce"] = int(
                        cur_player["stats"]["timeOnIce"].split(":")[0]
                    )

                    if cur_player["stats"]["decision"] == "L":
                        cur_player["stats"]["losses"] = 1
                    elif cur_player["stats"]["decision"] == "W":
                        cur_player["stats"]["wins"] = 1
                    else:
                        pass
                    cur_player["stats"].pop("decision")

                    cur_player["stats"]["gp"] = 1

                else:
                    print("ERROR")
            else:
                pass
            away_team[key] = cur_player

    return home_team, home_team_name, away_team, away_team_name


main()
