from collections import OrderedDict
from random import Random

RANDOM_BITS = 256

STACK = 20
POT_SIZES = {
    '1/3': 1 / 3,
    '2/3': 2 / 3,
    'Pot': 1,
    'All-in': STACK,
}
POT_SIZE_CHOICES = list(POT_SIZES)


def get_initial_ranges():
    RANGES = [
        [1, 3, 5, 7],
        [2, 4, 6, 7],
    ]

    return [
        {
            card: 1 / len(player_range)
            for card in player_range
        }
        for player_range in RANGES
    ]


class Match:
    def __init__(self, bot0, bot1):
        self.bots = [bot0, bot1]
        self.active_bot_id = 0
        self.pot = [1, 2]  # TODO: Allow check
        self.ranges = get_initial_ranges()

        for bot, card_range in zip(self.bots, self.ranges):
            bot.range = list(card_range)

        self.bot0_winnings = 0

    def run(self):
        opp_raise = None
        branch_prob = 1
        while self.pot[self.active_bot_id] < STACK:
            active_bot = self.bots[self.active_bot_id]
            opp_id = 1 - self.active_bot_id

            if opp_raise is not None:
                active_bot.receive_raise(opp_raise)

            action = active_bot.get_raise_probabilities()
            raise_size = action["size"]

            # Update winnings and ranges
            winnings = 0
            active_range = self.ranges[self.active_bot_id]
            chances = iter_win_chance(self.ranges[opp_id])
            next(chances)
            ev_fold = -self.pot[self.active_bot_id]
            for player_hand, player_prob in active_range.items():
                chance = chances.send(player_hand)
                ev_call = 2 * self.pot[opp_id] * (chance - 0.5)

                raise_prob = (
                    0 if self.pot[opp_id] == STACK
                    else action["range"].get(player_hand, 1)
                )

                winnings += (
                    player_prob
                    * (1 - raise_prob)
                    * max(ev_call, ev_fold)
                )
                active_range[player_hand] *= raise_prob

            self.bot0_winnings += (
                branch_prob
                * winnings
                * (1 - 2 * self.active_bot_id)
            )

            # Normalize range
            total_prob = sum(active_range.values())
            branch_prob *= total_prob
            if total_prob > 0:
                for player_hand, player_prob in active_range.items():
                    active_range[player_hand] /= total_prob

            self.pot[self.active_bot_id] = min(
                STACK,
                (1 + 2 * POT_SIZES[raise_size]) * self.pot[opp_id])
            self.active_bot_id = opp_id


class Bot:
    def __init__(self, seed):
        self.rng = Random(seed)
        self.range = [1]
        self.history = []

    def receive_raise(self, pot_size):
        self.history.append(['Received raise', pot_size])

        new_seed = str((self.rng.getrandbits(RANDOM_BITS), pot_size))
        self.rng.seed(new_seed)

    def get_raise_probabilities(self):
        action = {
            "size": self.rng.choice(POT_SIZE_CHOICES),
            "range": OrderedDict([
                (card, self.rng.random())
                for card in self.range[:-1]
            ]),
        }
        self.history.append(['Action', action])
        return action


def iter_win_chance(opp_range):
    """Compute the accumulated winning chances for increasing plyaer hands.

    How to use it:

    >>> opp_range = {1: 0.2, 5: 0.5, 7: 0.3}
    >>> player_hands = [0, 1, 2, 5, 6, 7, 10, 12]

    >>> chances = iter_win_chance(opp_range)
    >>> next(chances)

    >>> [chances.send(hand) for hand in player_hands]
    [0, 0.1, 0.2, 0.45, 0.7, 0.85, 1.0, 1.0]
    """
    win_chance = 0
    player_card = (yield None)
    for opp_card, opp_prob in sorted(opp_range.items()):
        while player_card < opp_card:
            player_card = (yield win_chance)

        if player_card == opp_card:
            player_card = (yield win_chance + opp_prob / 2)

        win_chance += opp_prob

    while True:
        player_card = yield win_chance
