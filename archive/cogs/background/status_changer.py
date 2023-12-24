import discord
from discord.ext import tasks, commands
from base_logger import logger
from config import COMMAND_PREFIX, ADMIN_ID
from itertools import cycle


class StatusChanger(commands.Cog):
    """
    A cog for cycling through statuses of bot
    """
    def __init__(self, bot):
        self.bot = bot
        self.status = cycle([discord.Activity(name=f'{COMMAND_PREFIX}help', type=discord.ActivityType.listening),
                             discord.Activity(name='Game Of The Year', url="https://www.youtube.com/watch?v=oHg5SJYRHA0", type=discord.ActivityType.streaming),
                             discord.Activity(name='Spotify', type=discord.ActivityType.listening),
                             discord.Activity(name=f'{COMMAND_PREFIX}help', type=discord.ActivityType.listening),
                             discord.Activity(name='with fire', type=discord.ActivityType.playing),
                             discord.Activity(name='VALORANT', type=discord.ActivityType.playing),
                             discord.Activity(name='Fall Guys',
                                              url="https://www.youtube.com/watch?v=yBLdQ1a4-JI",
                                              type=discord.ActivityType.streaming),
                             discord.Activity(name='Rocket League', type=discord.ActivityType.playing),
                             discord.Activity(name=f'{COMMAND_PREFIX}help', type=discord.ActivityType.listening),
                             discord.Activity(name=f'Call of Duty\N{REGISTERED SIGN}: Modern Warfare\N{REGISTERED SIGN}', url="https://www.youtube.com/watch?v=yBLdQ1a4-JI",
                                              type=discord.ActivityType.streaming),
                             discord.Activity(name='Apex Legends', type=discord.ActivityType.playing),
                             discord.Activity(name='out for you!', type=discord.ActivityType.watching),
                             discord.Activity(name=f'{COMMAND_PREFIX}help', type=discord.ActivityType.listening),
                             discord.Activity(name=f'Call of Duty\N{REGISTERED SIGN}: Modern Warfare\N{REGISTERED SIGN}', type=discord.ActivityType.playing),
                             discord.Activity(name='Catan', url="https://www.youtube.com/watch?v=yBLdQ1a4-JI",
                                              type=discord.ActivityType.streaming),
                             discord.Activity(name=f'{COMMAND_PREFIX}help', type=discord.ActivityType.listening),
                             discord.Activity(name='VALORANT', url="https://www.youtube.com/watch?v=b1cTSxu8O8c",
                                              type=discord.ActivityType.streaming),
                             discord.Activity(name=f'{COMMAND_PREFIX}help', type=discord.ActivityType.listening),
                             ])
        self.change_status.start()

    def cog_unload(self):
        self.change_status.cancel()

    @tasks.loop(minutes=30)
    async def change_status(self):
        logger.debug("Changing status...")
        await self.bot.change_presence(activity=next(self.status))

    @change_status.before_loop
    async def before(self):
        await self.bot.wait_until_ready()


def setup(bot):
    bot.add_cog(StatusChanger(bot))
