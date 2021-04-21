from collections import Counter
import itertools

class Team:
    def __init__(self, team_name):
        """Creates team."""
        self.team_name = team_name
        self.players = {} # {PLAYERID: {PlayerObject}}

    def get_all_players(self):
        return self.players

    def set_all_players(self, new_players):
        self.players = new_players

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


test = {'id': 'ID8475236', 'name': 'Cody Eakin', 'stats': {'faceOffPct': 430.79, 'timeOnIce': 110, 'evenTimeOnIce': 99, 'faceoffTaken': 97, 'faceOffWins': 53, 'shots': 8, 'hits': 8, 'gp': 8, 'plusMinus': 6, 'assists': 4, 'takeaways': 4, 'shortHandedTimeOnIce': 4, 'giveaways': 3, 'blocked': 2, 'goals': 1, 'powerPlayTimeOnIce': 1, 'powerPlayGoals': 0, 'powerPlayAssists': 0, 'penaltyMinutes': 0, 'shortHandedGoals': 0, 'shortHandedAssists': 0}, 'position': 'Center'}
test2 = {'id': 'ID8475236', 'name': 'Cody Eakin', 'team': 'Winnipeg Jets', 'position': 'Center', 'stats': {'faceOffPct': 430.79, 'timeOnIce': 110, 'evenTimeOnIce': 99, 'faceoffTaken': 97, 'faceOffWins': 53, 'shots': 8, 'hits': 8, 'gp': 8, 'plusMinus': 6, 'assists': 4, 'takeaways': 4, 'shortHandedTimeOnIce': 4, 'giveaways': 3, 'blocked': 2, 'goals': 1, 'powerPlayTimeOnIce': 1, 'powerPlayGoals': 0, 'powerPlayAssists': 0, 'penaltyMinutes': 0, 'shortHandedGoals': 0, 'shortHandedAssists': 0}}

p2 = Player(test2['id'], test2['name'], test2['position'], test2['team'])
p2.print_player_info()
p2.update_player_stats(test2['stats'])
p2.print_player_info()
