from collections import defaultdict


class ResultAnalyser:
    def __init__(self):
        self.results = {}

    def get_worst_results(self):
        return sorted(
            (win, opponent) for opponent, win in self.results.items()
        )[:10]


RESULTS = []
with open('matches/results.csv', 'r') as file:
    file.readline()  # Read header
    RESULTS = [line.rstrip() for line in file]

bots0 = defaultdict(ResultAnalyser)
bots1 = defaultdict(ResultAnalyser)

for match in RESULTS:
    bot0, bot1, win = match.split(';')
    bot0 = int(bot0)
    bot1 = int(bot1)
    win = float(win)

    bots0[bot0].results[bot1] = win
    bots1[bot1].results[bot0] = -win

for bot_id, bot in bots0.items():
    print(bot_id, bot.get_worst_results())
