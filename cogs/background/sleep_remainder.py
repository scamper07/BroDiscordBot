import asyncio
import discord
from discord.ext import tasks, commands
from discord.utils import get
from base_logger import logger
from config import DAILY_SLEEP_TIME, ADMIN_ID
from utils import sleep_until_time


class SleepRemainder(commands.Cog):
    """
    A cog for sleep remainder functionality
    """
    def __init__(self, bot):
        self.bot = bot
        self.daily_sleep_alarm.start()

    def cog_unload(self):
        self.daily_sleep_alarm.cancel()

    @tasks.loop(hours=24.0)
    async def daily_sleep_alarm(self):
        user = await self.bot.fetch_user(ADMIN_ID)
        logger.debug("daily_sleep_alarm")
        logger.debug(user)
        await user.send('Sleep bro!')

    @daily_sleep_alarm.before_loop
    async def before(self):
        # Trigger at DAILY_SLEEP_TIME
        await sleep_until_time(DAILY_SLEEP_TIME)
        await self.bot.wait_until_ready()


def setup(bot):
    bot.add_cog(SleepRemainder(bot))
