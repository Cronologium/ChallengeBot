class Pot:
    def __init__(self):
        self.sum = 0
        self.contributions = {}

    def put(self, who, what):
        if who not in self.contributions:
            self.contributions[who] = 0
        self.contributions[who] += what

    def take(self, players, win_order):
        side_pots = []
        max_contrib = max(self.contributions.values())
        while min(self.contributions.values()) != max_contrib:
            v = min(self.contributions.values())
            side_pots.append({})
            for p in self.contributions:
                side_pots[-1][p] = v
                self.contributions[p] -= v
            self.contributions = {k: v for k, v in self.contributions.items() if v > 0}
        side_pots.append(self.contributions)

        awarded = {k: 0 for k in self.contributions.keys()}
        for pot in side_pots:
            f_order = [win_order[x] for x in xrange(len(win_order)) if players[x] in pot]

            winners = [players[x] for x in xrange(len(players)) if players[x] in pot and f_order[x] == max(f_order)]

            s = sum(pot.values())
            each = s / len(winners)
            for w in winners:
                awarded[w] += each
            if each * len(winners) != s:
                awarded[winners[0]] += s - each * len(winners)
        return awarded

    def betting_sum(self):
        return max(v for k, v in self.contributions.items())