from pprint import pprint

from game import (
    Match, Bot,
)

BOT0_SEED = 1048
BOT1_SEED = 3245

bot0 = Bot(BOT0_SEED)
bot1 = Bot(BOT1_SEED)

match = Match(bot0, bot1)
match.run()

pprint(bot0.history)
pprint(bot1.history)

print(match.bot0_winnings)
