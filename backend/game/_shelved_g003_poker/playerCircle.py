class PlayerCircle:
    def __init__(self, players):
        self.players = [player for player in players]
        self.current = 0

    def next(self):
        self.current = (self.current + 1) % len(self.players)

    def set(self, player_name):
        self.current = self.players.index(player_name)

    def set_pos(self, pos):
        self.current = pos
        self.current = (self.current + len(self.players)) % len(self.players)

    def skip(self, skips=0):
        skips = skips % len(self.players)
        for i in xrange(skips):
            self.next()

    def exclude(self, excluded_players):
        while self.players[self.current] in excluded_players:
            self.next()
        current_name = self.players[self.current]
        self.players = [player for player in self.players if player not in excluded_players]
        self.set(current_name)

    def get(self, no=0):
        no = (no + len(self.players)) % len(self.players)
        return self.players[(self.current + no + len(self.players)) % len(self.players)]

    def get_pos(self, no=0):
        no = (no + len(self.players)) % len(self.players)
        return (self.current + len(self.players) + no) % len(self.players)

    def __len__(self):
        return len(self.players)

    def __iter__(self):
        for player_name in self.players:
            yield player_name
        raise StopIteration