from backend.game.abstract_game import Game
from backend.game._shelved_g003_poker.exceptions.turnOver import TurnOver
from backend.game._shelved_g003_poker.playerCircle import PlayerCircle
from backend.game._shelved_g003_poker.pokerPlayer import PokerPlayer
from backend.game._shelved_g003_poker.pot import Pot
from backend.game.playbox.decks.playing_cards_basic_deck import PlayingCardsBasicDeck
from backend.game.playbox.enums.card_suits import CardSuits
from backend.game.status import Status


class PokerGame(Game):
    def __init__(self, debug_logger, logger, server, players):
        self.money = 10000
        self.deck = PlayingCardsBasicDeck()
        super(PokerGame, self).__init__(debug_logger, logger, server,
                                        [[PokerPlayer(player[0], player[1], self.money / len(players)) for player in players]],
                                        turns=1)

        self.playing = PlayerCircle(self.players.keys())
        self.dealer = 0
        self.visible_cards = [None, None, None, None, None]
        self.pot = None
        self.small_blind = 5
        self.big_blind = 10
        self.bet_minimum = 0

    def give_ranking(self, all_cards):
        ranking = 0
        for x in xrange(7):
            for y in xrange(x + 1, 7):
                ranking = max(ranking, self.rank_hand([all_cards[i] for i in xrange(7) if i != x and i != y]))
        return ranking

    def rank_hand(self, hand):
        '''
        base_rank = {
            'pair':         10000000,
            'two pair':     20000000,
            'triple':       30000000,
            'straight':     40000000,
            'flush':        50000000,
            'full house':   60000000,
            'quad':         70000000,
            'straight flush':80000000,
        }
        '''

        suits = {
            CardSuits.HEARTS: sum([card for card in hand if card.suit == CardSuits.HEARTS]),
            CardSuits.SPADES: sum([card for card in hand if card.suit == CardSuits.SPADES]),
            CardSuits.DIAMONDS: sum([card for card in hand if card.suit == CardSuits.DIAMONDS]),
            CardSuits.CLUBS: sum([card for card in hand if card.suit == CardSuits.CLUBS])
        }
        number = {}
        mapping = {}
        card_numbers = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        for n in card_numbers:
            number[n] = sum([card for card in hand if card.number == n])
            mapping[n] = card_numbers.index(n) + 1

        f = [0 for x in xrange(14)]
        for card in hand:
            f[mapping[card.number]] += 1
        f[0] = f[13]

        flush = None
        straight = None
        quad = []
        triple = []
        pair = []

        for suit in suits:
            if suits[suit] > 4:
                flush = suit

        for x in xrange(9):
            if f[x] and f[x+1] and f[x+2] and f[x+3] and f[x+4]:
                straight = x

        for n in number:
            if number[n] == 4:
                quad.append(mapping[n])
            if number[n] == 3 :
                triple.append(mapping[n])
            if number[n] == 2:
                pair.append(mapping[n])

        if flush and straight:
            return 80000000 + straight
        if len(quad):
            return 70000000 + quad[0] * 13 + sum([mapping[n] for n in number if number[n] == 1])
        if len(triple) and len(pair):
            return 60000000 + triple[0] * 13 + pair[0]
        if flush:
            rank = 0
            multiplier = 1
            for x in xrange(1, 14):
                if f[x] > 0:
                    rank += multiplier * (x - 1)
                    multiplier *= 13
            return 50000000 + rank
        if straight:
            return 40000000 + straight
        if len(triple):
            rank = 0
            multiplier = 1
            for x in xrange(1, 14):
                if f[x] == 1:
                    rank += multiplier * (x - 1)
                    multiplier *= 13
            return 30000000 + rank
        if len(pair) == 2:
            rank = 0
            multiplier = 1
            for x in xrange(1, 14):
                if f[x] == 1:
                    rank += multiplier * (x - 1)
                    multiplier *= 13
            return 20000000 + rank
        if len(pair):
            rank = 0
            multiplier = 1
            for x in xrange(1, 14):
                if f[x] == 1:
                    rank += multiplier * (x - 1)
                    multiplier *= 13
            return 10000000 + rank
        rank = 0
        multiplier = 1
        for x in xrange(1, 14):
            if f[x] == 1:
                rank += multiplier * (x - 1)
                multiplier *= 13
        return rank

    def deal_cards(self):
        self.deck.shuffle()
        for k in xrange(1, len(self.playing) * 2 + 1):
            self.players[self.playing.get(k)].deal_card(self.deck.draw())

    def broadcast(self, skip, player, action, sum=''):
        for player_name in self.playing:
            if player_name != skip:
                self.players[player_name].announce(player + ' ' + action + ' ' + sum)

    def build_message(self, player_name):
        cards_string = ' '.join([str(card) for card in self.visible_cards if card is not None])
        if cards_string is None:
            cards_string = ''
        msg = str(self.players[player_name].money) + ' | ' + str(self.bet_minimum) + ' | ' + self.players[player_name].get_cards() + ' | ' + cards_string
        announcements = self.players[player_name].get_messages()
        if announcements != '':
            msg += announcements
        return msg

    def current_player_folds(self):
        self.logger.log(self.playing.get() + ' folds')
        self.deck.put_cards(self.players[self.playing.get()].fold())

    def log_player_command(self, data):
        self.logger.log(self.playing.get() + ': ' + ' '.join(data))

    def put_pot(self, chips):
        self.logger.log(self.playing.get() + ' puts ' + str(chips))
        self.pot.put(self.playing.get(), self.players[self.playing.get()].bet(chips))

    def do_betting(self):
        reach = self.playing.get_pos(-1)
        while self.playing.get_pos() != reach and len([p for p in self.playing if self.players[p].folded is False]) > 1:
            if self.players[self.playing.get()].folded:
                self.playing.next()
                continue
            if self.players[self.playing.get(0)].money == 0:
                self.playing.next()
                continue

            msg = self.server.send_and_receive(self.playing.get(0), self.build_message(self.playing.get(0)))

            if msg is None:
                self.current_player_folds()
            else:
                data = msg.split(' ')
                self.log_player_command(data)
                if len(data) > 3:
                    self.current_player_folds()
                if data[0] not in ['check', 'bet', 'fold', 'call', 'allin']:
                    self.current_player_folds()
                if data[0] == 'check' and (self.bet_minimum > 0 or len(data) > 1):
                    self.current_player_folds()
                if data[0] == 'bet':
                    try:
                        if len(data) > 2:
                            raise Exception
                        chips = int(data[1])
                        if chips > self.players[self.playing.get()].money:
                            data = ['allin']
                            reach = self.playing.get_pos()
                            self.bet_minimum = self.players[self.playing.get()].money
                        else:
                            if chips < self.bet_minimum * 2:
                                raise Exception
                            self.pot.put(self.players[self.playing.get()].bet(chips))
                            reach = self.playing.get_pos()
                            self.put_pot(chips)
                            self.bet_minimum *= 2
                    except Exception:
                        self.current_player_folds()
                if data[0] == 'fold':
                    self.current_player_folds()
                if data[0] == 'call':
                    if len(data) > 1:
                        self.current_player_folds()
                    else:
                        if self.bet_minimum >= self.players[self.playing.get()].money:
                            data = ['allin']
                        else:
                            self.put_pot(self.bet_minimum)
                if data[0] == 'allin':
                    if len(data) > 1:
                        self.current_player_folds()
                    self.put_pot(self.players[self.playing.get()].money)
            self.playing.next()

    def gather_cards(self):
        self.deck.put_cards([card for card in self.visible_cards if card is not None])
        for player_name in self.playing:
            if self.players[player_name].folded is not False:
                self.deck.put_cards(self.players[player_name].fold())

    def determine_winners(self):
        playing = [p for p in self.playing if self.players[p].folded is False]
        if len(playing) == 1:
            return playing, [1]
        else:
            return [player for player in playing], [self.give_ranking(self.players[player].cards + self.visible_cards) for player in playing]

    def should_determine_winner(self):
        if len([player for player in self.players if self.players[player].folded is False]) == 1:
            return True

    def award(self, pot_money):
        for p in pot_money:
            self.players[p].win(pot_money[p])

    def turn(self):
        self.deal_cards()
        self.pot = Pot()

        self.playing.set_pos(self.dealer)
        self.pot.put(self.playing.get(1), self.players[self.playing.get(1)].bet(self.small_blind))
        self.pot.put(self.playing.get(2), self.players[self.playing.get(2)].bet(self.small_blind))
        self.bet_minimum = self.big_blind
        self.playing.skip(3)
        try:

            self.do_betting()

            if self.should_determine_winner():
                raise TurnOver

            self.bet_minimum = 0
            for x in xrange(3):
                self.visible_cards[x] = self.deck.draw()
            self.playing.set_pos(self.dealer)
            self.playing.skip(1)
            self.do_betting()

            if self.should_determine_winner():
                raise TurnOver

            self.bet_minimum = 0
            self.visible_cards[3] = self.deck.draw()
            self.playing.set_pos(self.dealer)
            self.playing.skip(1)
            self.do_betting()

            if self.should_determine_winner():
                raise TurnOver

            self.bet_minimum = 0
            self.visible_cards[4] = self.deck.draw()
            self.playing.set_pos(self.dealer)
            self.playing.skip(1)
            self.do_betting()

        finally:
            players, order = self.determine_winners()
            self.award(self.pot.take(players, order))
        self.dealer = (self.dealer + 1) % len(self.playing)

    def check(self):
        for player in self.players:
            if self.players[player].money == 0:
                self.players[player].status = Status.LOSER
        self.playing.exclude([player for player in self.playing if self.players[player].status == Status.LOSER])

        super(PokerGame, self).check()

