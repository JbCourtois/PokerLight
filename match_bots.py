from game import (
    Match, Bot,
)

SEEDS = 2000


matches = []
for seed0 in range(SEEDS):
    for seed1 in range(SEEDS, 2 * SEEDS):
        bot0 = Bot(seed0)
        bot1 = Bot(seed1)
        match = Match(bot0, bot1)
        match.run()
        matches.append([seed0, seed1, round(match.bot0_winnings, 3)])
    print(seed0)

with open('matches/results.csv', 'w') as file:
    print('Bot 0;Bot 1;Winnings', file=file)
    for match in matches:
        print(*match, sep=';', file=file)
