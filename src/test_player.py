class Player:
    def __init__(self, id, name, position):
        """Creates player."""
        self.id = id
        self.name = name
        self.position = position
        self.stats = {}

    def print_player_info(self):
        """Prints player information."""
        print("PLAYER INFO")
        print("- ID:", self.id)
        print("- Name:", self.name)
        print("- Position:", self.position)
        print("- Statistics:", self.stats)


test = {'id': 'ID8475236', 'name': 'Cody Eakin', 'stats': {'faceOffPct': 430.79, 'timeOnIce': 110, 'evenTimeOnIce': 99, 'faceoffTaken': 97, 'faceOffWins': 53, 'shots': 8, 'hits': 8, 'gp': 8, 'plusMinus': 6, 'assists': 4, 'takeaways': 4, 'shortHandedTimeOnIce': 4, 'giveaways': 3, 'blocked': 2, 'goals': 1, 'powerPlayTimeOnIce': 1, 'powerPlayGoals': 0, 'powerPlayAssists': 0, 'penaltyMinutes': 0, 'shortHandedGoals': 0, 'shortHandedAssists': 0}, 'position': 'Center'}

my_play = Player(test['id'], test['name'], test['position'])
my_play.print_player_info()
