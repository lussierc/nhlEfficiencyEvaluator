"""Parses through scraped game data to calculate player statistics."""

import numpy as np
import pandas as pd
import pickle
import math
import itertools
from collections import Counter


class League:
    """Holds league statistics."""

    def __init__(self):
        self.all_skaters_avg_stats_df = pd.DataFrame()

    def add_stats(self, stats):
        self.all_skaters_avg_stats_df = self.all_skaters_avg_stats_df.append(
            stats, ignore_index=True
        )

    def print_stats(self):

        self.all_skaters_avg_stats_df = self.all_skaters_avg_stats_df.sort_values(
            by=["Efficiency Value"], ascending=False
        )
        print(
            "\n\n\n--------------------",
            "Average League Statistics",
            "--------------------",
        )
        print(self.all_skaters_avg_stats_df)

        file_name = input(
            "Enter your export file name (EX: filename.csv), to export league stats:"
        )
        self.all_skaters_avg_stats_df.to_csv(file_name)


class Team:
    """Holds a team's information and player objects."""

    def __init__(self, team_name):
        """Creates team."""

        self.team_name = team_name
        self.players = []
        self.skaters_df = pd.DataFrame()
        self.skaters_avg_stats_df = pd.DataFrame()
        self.goalies_df = pd.DataFrame()

    def get_team_name(self):
        return self.team_name

    def get_skaters_avg_stats_df(self):
        return self.skaters_avg_stats_df

    def print_all_players(self):
        """Prints out the team DFs of players."""

        print("--------------------", self.team_name, "--------------------")
        # print skaters on team:
        print("* Printing Skaters:")
        print(self.skaters_df)
        # print goalies on team:
        print("* Printing Goalies:")
        print(self.goalies_df)
        # print average player stats:
        print("* Printing Avg Skater Stats & Efficiency Metric:")

        self.skaters_avg_stats_df = self.skaters_avg_stats_df.sort_values(
            by=["Efficiency Value"], ascending=False
        )
        print(self.skaters_avg_stats_df)

    def add_player(self, new_player):
        """Adds a new player to the team."""

        self.players.append(new_player)  # add player object to team
        if new_player.get_player_position() == "Goalie":
            self.goalies_df = self.goalies_df.append(
                new_player.get_finalized_player_stats_df(), ignore_index=True
            )
        else:
            self.skaters_df = self.skaters_df.append(
                new_player.get_finalized_player_stats_df(), ignore_index=True
            )
            try:
                df = new_player.get_finalized_avg_player_stats_df()
                if "savePercentage" not in df.columns:
                    self.skaters_avg_stats_df = self.skaters_avg_stats_df.append(
                        df, ignore_index=True
                    )
            except Exception:
                pass


class Player:
    """Player class. Holds the general information and stats for an individual player."""

    def __init__(self, id, name, position, team):
        """Creates player."""

        self.id = id
        self.name = name
        self.position = position
        self.team = team
        self.stats = {}
        self.avg_stats = {}

    def get_player_team(self):
        """Returns a player's team."""

        return self.team

    def get_player_position(self):
        """Returns a player's position."""

        return self.position

    def update_player_team(self, new_team):
        """Updates the player's team if they moved during the season."""

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
                    counted_stats["powerPlaySaves"]
                    / counted_stats["powerPlayShotsAgainst"]
                ) * 100
            except:
                pass
        else:
            try:
                counted_stats["faceOffPct"] = (
                    counted_stats["faceOffWins"] / counted_stats["faceoffTaken"]
                ) * 100
            except:
                pass
        self.stats = counted_stats

    def finalize_player_stats_df(self):
        """Puts player info in a DF for future use/displaying."""

        self.stats_df = pd.DataFrame.from_dict([self.stats])

        self.stats_df.insert(loc=0, column="Team", value=[self.team])
        self.stats_df.insert(loc=0, column="Position", value=[self.position])
        self.stats_df.insert(loc=0, column="Name", value=[self.name])
        self.stats_df.insert(loc=0, column="ID", value=[self.id])
        self.stats_df = self.stats_df[sorted(self.stats_df)]

    def get_finalized_player_stats_df(self):
        """Return the finalied player DF."""

        return self.stats_df

    def get_finalized_avg_player_stats_df(self):
        return self.avg_stats_df

    def finalize_player_avg_stats_df(self):
        try:
            self.avg_stats["gp"] = self.stats["gp"]
        except:
            self.avg_stats["gp"] = 0

        if self.avg_stats["gp"] != 0:
            for key in self.stats.keys():
                if key == "gp":
                    pass
                elif key == "plusMinus":
                    pass
                elif key == "faceOffPct":
                    self.avg_stats["faceOffPct"] = self.stats["faceOffPct"]
                else:
                    self.avg_stats[key] = self.stats[key] / self.stats["gp"]

            avg_points = self.avg_stats["goals"] + self.avg_stats["assists"]

            if avg_points != 0:
                eff_points = avg_points * 0.75
            else:
                eff_points = 0

            if self.avg_stats["shots"] != 0:
                eff_shots = self.avg_stats["shots"] * 0.5
            else:
                eff_shots = 0

            try:
                eff_plusminus = 0.2
            except:
                eff_plusminus = self.stats["plusMinus"] * 0.5

            try:
                eff_blocked = self.avg_stats["blocked"] * 0.2
            except:
                eff_blocked = 0

            try:
                eff_hits = self.avg_stats["hits"] * 0.2
            except:
                eff_hits = 0

            eff_value = (
                eff_points + eff_shots + eff_plusminus + eff_blocked + eff_hits
            ) / 5

            self.avg_stats_df = pd.DataFrame.from_dict([self.avg_stats])

            self.avg_stats_df.insert(
                loc=0, column="Efficiency Value", value=[eff_value]
            )
            self.avg_stats_df.insert(loc=0, column="Team", value=[self.team])
            self.avg_stats_df.insert(loc=0, column="Position", value=[self.position])
            self.avg_stats_df.insert(loc=0, column="Name", value=[self.name])
            self.avg_stats_df.insert(loc=0, column="ID", value=[self.id])
            self.avg_stats_df = self.avg_stats_df[sorted(self.avg_stats_df)]
        else:
            pass


def run_data_cleaner():
    """Runs the data cleaner."""

    file_name = input("** Please Enter your '.pkl' filename: ")
    try:
        with open(file_name, "rb") as f:
            game_data = pickle.load(f)
    except:
        print("ERROR IN FILENAME")
        quit()

    players = get_player_data(game_data)

    teams, league = organize_teams(players)
    for team in teams:
        print(team.get_team_name())
        team.print_all_players()

    league.print_stats()


def get_player_data(game_data):
    """Goes thru each individual game's data and gets key player statistics."""

    players = {}  # base players dictionary that will hold all player info

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
    """Creates team objects and puts players on their respective teams."""

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
    league = League()
    for team_name in all_team_names:
        team = Team(team_name)
        teams.append(team)

    for team in teams:
        for player_key in players.keys():
            player = players[player_key]
            player_team = player.get_player_team()
            team_name = team.get_team_name()

            if player_team == team_name:
                ### TODO: FINALIZE CODE HERE TO MAKE PLAYER DF
                player.finalize_player_stats_df()
                if player.get_player_position() != "Goalie":
                    player.finalize_player_avg_stats_df()
                team.add_player(player)
                ###
            else:
                pass
        league.add_stats(team.get_skaters_avg_stats_df())

    return teams, league


def get_game_data(data):
    """Parses thru an individual game's data to gather player statistics."""

    if "liveData" in data:
        game_teams = data["liveData"]["boxscore"]["teams"]

        home_team_name = game_teams["home"]["team"]["name"]  # get home team attributes
        home_team_players = game_teams["home"]["players"]
        away_team_name = game_teams["away"]["team"]["name"]  # get away team attributes
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
        }  # create teams dict to hold all info for both teams for given game

        for team in teams.keys():
            team_name = teams[team]["name"]  # get current team name
            team_players = teams[team]["players"]  # get current team roster

            for key in team_players.keys():
                player = team_players[key]  # get the current player on the team
                player_name = player["person"]["fullName"]  # get player name
                player_postition = player["position"]["name"]  # get player position
                player_stats = player["stats"]  # get player stats for the game
                player_dict = {
                    "id": key,
                    "name": player_name,
                    "team": team_name,
                    "position": player_postition,
                    "stats": "",
                }  # will hold all player info for the game

                if player_stats:  # if not empty, perform stat preparation work
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

                        player_dict["stats"]["gp"] = 1  # add game played
                    elif "goalieStats" in player_stats.keys():
                        player_dict["stats"] = player_stats["goalieStats"]

                        player_dict["stats"]["timeOnIce"] = int(
                            player_dict["stats"]["timeOnIce"].split(":")[0]
                        )  # integerize time on ice

                        if player_dict["stats"]["decision"] == "L":
                            player_dict["stats"]["losses"] = 1
                        elif player_dict["stats"]["decision"] == "W":
                            player_dict["stats"]["wins"] = 1
                        else:
                            pass

                        player_dict["stats"].pop(
                            "decision"
                        )  # remove now unnecessary var

                        player_dict["stats"]["gp"] = 1  # add game played
                    else:
                        print("ERROR")
                else:
                    pass

                teams[team]["finalized_roster"][
                    key
                ] = player_dict  # add finalized player to team for the game

    return teams
