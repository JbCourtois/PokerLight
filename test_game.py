from game import (
    Match, Bot,
)

BOT0_SEED = 4
BOT1_SEED = 1

bot0 = Bot(BOT0_SEED)
bot1 = Bot(BOT1_SEED)

match = Match(bot0, bot1)
match.run()

bot0 = Bot(BOT0_SEED)
bot1 = Bot(BOT1_SEED)

print(bot0.get_raise_probabilities(), end='\n\n')
print(bot1.get_raise_probabilities(), end='\n\n')

print(match.bot0_winnings)
