from collections import Counter
import itertools

class Team:
    def __init__(self, team_name):
        """Creates team."""
        self.team_name = team_name
        self.players = {} # {PLAYERID: {PlayerObject}}

    def get_all_players(self):
        print(self.players)    

class Player:
    def __init__(self, id, name, position):
        """Creates player."""
        self.id = id
        self.name = name
        self.position = position
        self.stats = {}

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
            counted_stats['faceOffPct'] = (counted_stats['faceOffWins'] / counted_stats['faceoffTaken']) * 100
        self.stats = counted_stats

    def print_player_info(self):
        """Prints player information."""
        print("PLAYER INFO")
        print("- ID:", self.id)
        print("- Name:", self.name)
        print("- Position:", self.position)
        print("- Statistics:", self.stats)


test = {'id': 'ID8475236', 'name': 'Cody Eakin', 'stats': {'faceOffPct': 430.79, 'timeOnIce': 110, 'evenTimeOnIce': 99, 'faceoffTaken': 97, 'faceOffWins': 53, 'shots': 8, 'hits': 8, 'gp': 8, 'plusMinus': 6, 'assists': 4, 'takeaways': 4, 'shortHandedTimeOnIce': 4, 'giveaways': 3, 'blocked': 2, 'goals': 1, 'powerPlayTimeOnIce': 1, 'powerPlayGoals': 0, 'powerPlayAssists': 0, 'penaltyMinutes': 0, 'shortHandedGoals': 0, 'shortHandedAssists': 0}, 'position': 'Center'}
test2 = {'id': 'ID8475236', 'name': 'Laurent Brossoit', 'stats': {'evenStrengthSavePercentage': 1710.0631072547787, 'savePercentage': 1694.1859904719947, 'powerPlaySavePercentage': 1221.6666666666665, 'timeOnIce': 981, 'shortHandedSavePercentage': 875.0, 'shots': 512, 'saves': 458, 'evenShotsAgainst': 430, 'evenSaves': 389, 'powerPlayShotsAgainst': 64, 'powerPlaySaves': 52, 'gp': 19, 'shortHandedShotsAgainst': 18, 'shortHandedSaves': 17, 'losses': 8, 'wins': 6, 'assists': 0, 'goals': 0, 'pim': 0}, 'position': 'Goalie'}

my_play = Player(test2['id'], test2['name'], test2['position'])
my_play.print_player_info()
my_play.update_player_stats(test2['stats'])

my_play.print_player_info()
