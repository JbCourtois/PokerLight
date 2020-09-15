from game import (
    Match, Bot,
    RANGES,
)


matches = []
for seed0 in range(0, 200):
    bot0 = Bot(seed0, RANGES[0])
    for seed1 in range(2000, 2200):
        bot1 = Bot(seed1, RANGES[1])
        match = Match(bot0, bot1)
        match.run()
        matches.append([seed0, seed1, round(match.bot0_winnings, 3)])
    print(seed0)

with open('matches/results.csv', 'w') as file:
    print('Bot 0;Bot 1;Winnings', file=file)
    for match in matches:
        print(*match, sep=';', file=file)
