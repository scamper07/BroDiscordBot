import discord
from discord.ext import commands
from base_logger import logger
from config import COMMAND_PREFIX

# List of cogs to load on bot startup
BOT_STARTUP_COGS_LIST = ['cogs.events',
                         'cogs.general.general',
                         'cogs.general.statistics',
                         'cogs.games.quiz',
                         'cogs.background.daily_advice',
                         'cogs.background.twitch_stream_notifier',
                         'cogs.admin.admin_actions',
                         #'cogs.games.gameboy',
                         'cogs.background.daily_news',
                         'cogs.background.f1_calendar',
                         #'cogs.general.music',
                         'cogs.background.status_changer',
                         'cogs.background.sleep_remainder',
                         'cogs.games.tictactoe',
                         ]

intents = discord.Intents.all()
bot = commands.Bot(command_prefix=COMMAND_PREFIX, description='The Bro Bot', intents=intents)

if __name__ == '__main__':
    logger.debug("Bro Bot Startup...")
    
    # load initial cogs
    for cog in BOT_STARTUP_COGS_LIST:
        try:
            logger.debug("Loading cog : {}".format(cog))
            bot.load_extension(cog)
        except Exception as e:
            logger.exception("Failed to load extension {}. ERROR: {}".format(cog, e))

    # read Bot Token from token file in keys folder
    with open('keys/token') as f:
        TOKEN = f.read()

    bot.run(TOKEN, bot=True, reconnect=True)
