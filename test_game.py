from game import (
    Match, Bot,
)

BOT0_SEED = 4
BOT1_SEED = 1

bot0 = Bot(BOT0_SEED)
bot1 = Bot(BOT1_SEED)

match = Match(bot0, bot1)
match.run()

print(bot0.history, end='\n\n')
print(bot1.history, end='\n\n')

print(match.bot0_winnings)
