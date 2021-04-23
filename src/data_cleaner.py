"""Cleans the scraped data by calculating player statistics."""

import numpy as np
import pandas as pd
import pickle
import math
import itertools
from collections import Counter


class Team:
    def __init__(self, team_name):
        """Creates team."""
        self.team_name = team_name
        self.players = []

    def get_team_name(self):
        return self.team_name

    def print_all_players(self):
        for player in self.players:
            player.print_player_info()

    def add_player(self, new_player):
        self.players.append(new_player)


class Player:
    def __init__(self, id, name, position, team):
        """Creates player."""
        self.id = id
        self.name = name
        self.position = position
        self.team = team
        self.stats = {}

    def get_player_team(self):
        return self.team

    def update_player_team(self, new_team):
        self.team = new_team  # account for trades

    def update_player_stats(self, new_stats):
        """If stats exist, update them. If not, add them."""

        combo = Counter(self.stats)
        combo.update(Counter(new_stats))
        counted_stats = dict(combo)

        if "saves" in self.stats:
            self.position = "Goalie"
        elif "evenTimeOnIce" in self.stats:
            self.position = "Skater"
        else:
            self.position = "Unknown"

        if self.position == "Goalie":
            try:
                counted_stats["evenStrengthSavePercentage"] = (
                    counted_stats["evenSaves"] / counted_stats["evenShotsAgainst"]
                ) * 100
            except:
                pass
            try:
                counted_stats["savePercentage"] = (
                    counted_stats["saves"] / counted_stats["shots"]
                ) * 100
            except:
                pass
            try:
                counted_stats["shortHandedSavePercentage"] = (
                    counted_stats["shortHandedSaves"]
                    / counted_stats["shortHandedShotsAgainst"]
                ) * 100
            except:
                pass
            try:
                counted_stats["powerPlaySavePercentage"] = (
                    counted_stats["powerPlaySaves"] / counted_stats["powerPlayShotsAgainst"]
                ) * 100
            except:
                pass
        else:
            print("SKATER")
            try:
                counted_stats["faceOffPct"] = (
                    counted_stats["faceOffWins"] / counted_stats["faceoffTaken"]
                ) * 100
            except:
                pass
        self.stats = counted_stats

    def print_player_info(self):
        """Prints player information."""
        print("PLAYER INFO")
        print("- ID:", self.id)
        print("- Name:", self.name)
        print("- Team:", self.team)
        print("- Position:", self.position)
        print("- Statistics:", self.stats)


def main():
    """Runs the data cleaner."""

    file_name = input("** Please Enter your '.pkl' filename: ")
    try:
        with open(file_name, "rb") as f:
            game_data = pickle.load(f)
    except:
        print("ERROR IN FILENAME")
        quit()

    players = get_player_data(game_data)
    for player_key in players.keys():
        player = players[player_key]
        player.print_player_info()

    teams = organize_teams(players)
    for team in teams:
        print(team.get_team_name())
        team.print_all_players()

def get_player_data(game_data):
    players = {}

    for data in game_data:
        if "liveData" in data:
            teams = get_game_data(data)

            for team in teams.keys():
                team_name = teams[team]["name"]
                team_players = teams[team]["finalized_roster"]

                for player_key in team_players.keys():
                    player_cur_game_id = team_players[player_key]["id"]
                    player_cur_game_name = team_players[player_key]["name"]
                    player_cur_game_team = team_players[player_key]["team"]
                    player_cur_game_pos = team_players[player_key]["position"]
                    player_cur_game_stats = team_players[player_key]["stats"]

                    if player_key in players.keys():
                        player = players[player_key]
                        player.update_player_stats(player_cur_game_stats)

                        szn_team = player.get_player_team()
                        if (
                            szn_team != player_cur_game_team
                        ):  # player trade/movement has occurred
                            player.update_player_team(player_cur_game_team)
                        else:
                            pass
                    else:
                        player = Player(
                            player_cur_game_id,
                            player_cur_game_name,
                            player_cur_game_pos,
                            player_cur_game_team,
                        )
                        player.update_player_stats(player_cur_game_stats)
                        players[player_key] = player

    return players

def organize_teams(players):
    all_team_names = [
        "Anaheim Ducks",
        "Arizona Coyotes",
        "Boston Bruins",
        "Buffalo Sabres",
        "Calgary Flames",
        "Carolina Hurricanes",
        "Chicago Blackhawks",
        "Colorado Avalanche",
        "Columbus Blue Jackets",
        "Dallas Stars",
        "Detroit Red Wings",
        "Edmonton Oilers",
        "Florida Panthers",
        "Los Angeles Kings",
        "Minnesota Wild",
        "Montréal Canadiens",
        "Nashville Predators",
        "New Jersey Devils",
        "New York Islanders",
        "New York Rangers",
        "Ottawa Senators",
        "Philadelphia Flyers",
        "Pittsburgh Penguins",
        "San Jose Sharks",
        "St. Louis Blues",
        "Tampa Bay Lightning",
        "Toronto Maple Leafs",
        "Vancouver Canucks",
        "Vegas Golden Knights",
        "Washington Capitals",
        "Winnipeg Jets",
    ]

    teams = []
    for team_name in all_team_names:
        team = Team(team_name)
        teams.append(team)

    for team in teams:
        for player_key in players.keys():
            player = players[player_key]
            player_team = player.get_player_team()
            team_name = team.get_team_name()

            if player_team == team_name:
                team.add_player(player)
            else:
                pass

    return teams

def get_game_data(data):
    if "liveData" in data:
        game_teams = data["liveData"]["boxscore"]["teams"]

        home_team_name = game_teams["home"]["team"]["name"] # get home team attributes
        home_team_players = game_teams["home"]["players"]
        away_team_name = game_teams["away"]["team"]["name"] # get away team attributes
        away_team_players = game_teams["away"]["players"]

        teams = {
            "home_team": {
                "name": home_team_name,
                "players": home_team_players,
                "finalized_roster": {},
            },
            "away_team": {
                "name": away_team_name,
                "players": away_team_players,
                "finalized_roster": {},
            },
        } # create teams dict to hold all info for both teams for given game

        for team in teams.keys():
            team_name = teams[team]["name"] # get current team name
            team_players = teams[team]["players"] # get current team roster

            for key in team_players.keys():
                player = team_players[key] # get the current player on the team
                player_name = player["person"]["fullName"] # get player name
                player_postition = player["position"]["name"] # get player position
                player_stats = player["stats"] # get player stats for the game
                player_dict = {
                    "id": key,
                    "name": player_name,
                    "team": team_name,
                    "position": player_postition,
                    "stats": "",
                } # will hold all player info for the game


                if player_stats: # if not empty, perform stat preparation work
                    if "skaterStats" in player_stats.keys():
                        player_dict["stats"] = player_stats["skaterStats"]

                        # integerize time on ice (playing time):
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

                        player_dict["stats"]["gp"] = 1 # add game played
                    elif "goalieStats" in player_stats.keys():
                        player_dict["stats"] = player_stats["goalieStats"]

                        player_dict["stats"]["timeOnIce"] = int(
                            player_dict["stats"]["timeOnIce"].split(":")[0]
                        ) # integerize time on ice

                        if player_dict["stats"]["decision"] == "L":
                            player_dict["stats"]["losses"] = 1
                        elif player_dict["stats"]["decision"] == "W":
                            player_dict["stats"]["wins"] = 1
                        else:
                            pass

                        player_dict["stats"].pop("decision") # remove now unnecessary var

                        player_dict["stats"]["gp"] = 1 # add game played
                    else:
                        print("ERROR")
                else:
                    pass

                teams[team]["finalized_roster"][key] = player_dict # add finalized player to team for the game

    return teams


main()
