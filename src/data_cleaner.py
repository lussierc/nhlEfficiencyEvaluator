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

class Team:
    def __init__(self, team_name):
        """Creates team."""
        self.team_name = team_name
        self.players = []

    def get_team_name(self):
        return self.team_name

    def print_all_players(self):
        for player in self.players:
            print(player.print_player_info())

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
        self.team = new_team # account for trades

    def update_player_stats(self, new_stats):
        """If stats exist, update them. If not, add them."""

        combo = Counter(self.stats)
        combo.update(Counter(new_stats))
        counted_stats = dict(combo)

        if self.position == "Goalie":
            print("GOALIE")
            counted_stats['evenStrengthSavePercentage'] = (counted_stats['evenSaves'] / counted_stats['evenShotsAgainst']) * 100
            counted_stats['savePercentage'] = (counted_stats['saves'] / counted_stats['shots']) * 100
            counted_stats['shortHandedSavePercentage'] = (counted_stats['shortHandedSaves'] / counted_stats['shortHandedShotsAgainst']) * 100
            counted_stats['powerPlaySavePercentage'] = (counted_stats['powerPlaySaves'] / counted_stats['powerPlayShotsAgainst']) * 100
        else:
            print("SKATER")
            try:
                counted_stats['faceOffPct'] = (counted_stats['faceOffWins'] / counted_stats['faceoffTaken']) * 100
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

    all_team_names = ["Anaheim Ducks", "Arizona Coyotes", "Boston Bruins", "Buffalo Sabres", "Calgary Flames", "Carolina Hurricanes", "Chicago Blackhawks", "Colorado Avalanche", "Columbus Blue Jackets", "Dallas Stars", "Detroit Red Wings", "Edmonton Oilers", "Florida Panthers", "Los Angeles Kings", "Minnesota Wild", "Montréal Canadiens", "Nashville Predators", "New Jersey Devils", "New York Islanders", "New York Rangers", "Ottawa Senators", "Philadelphia Flyers", "Pittsburgh Penguins", "San Jose Sharks", "St. Louis Blues", "Tampa Bay Lightning", "Toronto Maple Leafs", "Vancouver Canucks", "Vegas Golden Knights", "Washington Capitals", "Winnipeg Jets"]

    players = {}

    for data in game_data:
        if "liveData" in data:
            teams = get_game_data(data)

            for team in teams.keys():
                team_name = teams[team]['name']
                team_players = teams[team]['finalized_roster']
                print(team_name)
                print(team_players)
                #'ID8475834': {'id': 'ID8475834', 'name': 'Marcus Sorensen', 'team': 'San Jose Sharks', 'position': 'Left Wing', 'stats': {'timeOnIce': 16, 'assists': 0, 'goals': 0, 'shots': 0, 'hits': 1, 'powerPlayGoals': 0, 'powerPlayAssists': 0, 'penaltyMinutes': 0, 'faceOffWins': 0, 'faceoffTaken': 0, 'takeaways': 0, 'giveaways': 0, 'shortHandedGoals': 0, 'shortHandedAssists': 0, 'blocked': 0, 'plusMinus': -3, 'evenTimeOnIce': 14, 'powerPlayTimeOnIce': 0, 'shortHandedTimeOnIce': 1, 'gp': 1}}
                for player_key in team_players.keys():
                    player_cur_game_id = team_players[player_key]['id']
                    player_cur_game_name = team_players[player_key]['name']
                    player_cur_game_team = team_players[player_key]['team']
                    player_cur_game_pos = team_players[player_key]['position']
                    player_cur_game_stats = team_players[player_key]['stats']

                    if player_key in players.keys():
                        player = players[player_key]
                        player.update_player_stats(player_cur_game_stats)

                        szn_team = player.get_player_team()
                        if szn_team != player_cur_game_team: # player trade/movement has occurred
                            player.update_player_team(player_cur_game_team)
                        else:
                            pass
                    else:
                        player = Player(player_cur_game_id, player_cur_game_name, player_cur_game_team, player_cur_game_pos)
                        player.update_player_stats(player_cur_game_stats)
                        players[player_key] = player

    for player_key in players.keys():
        player = players[player_key]
        player.print_player_info()

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

    for team in teams:
        print(team.get_team_name())
        team.print_all_players()
                #all_teams[team_name][game_player_key]["stats"]
                # for player_key in team_players.keys():
                #     if player_key in players:
                #         player = players[player_key]
                #         player.update_player_stats(new_stats)

def get_game_data(data):
    if "liveData" in data:
        game_teams = data["liveData"]["boxscore"]["teams"]

        team_name = game_teams["home"]["team"]["name"]
        home_team = {}
        home_team_players = game_teams["home"]["players"]

        away_team_name = game_teams["away"]["team"]["name"]
        away_team = {}
        away_team_players = game_teams["away"]["players"]

        teams = {'home_team': {'name': team_name, 'players': home_team_players, 'finalized_roster': {}}, 'away_team': {'name': away_team_name, 'players': away_team_players, 'finalized_roster': {}}}

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
                    "team": team_name,
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
    return teams


main()
