import asyncio

import discord
from discord.ext import tasks, commands
from discord.utils import get
from base_logger import logger
from config import DAILY_SLEEP_TIME, ADMIN_ID
from utils import sleep_until_time


class SleepRemainder(commands.Cog):
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

        '''
        #user = get(self.bot.get_all_members(), id=ADMIN_ID)
        guild = self.bot.get_guild(572648167573684234)
        user = guild.get_member(ADMIN_ID)
        logger.debug(user)
        if user:
            logger.debug(user)
            logger.debug(user.status)

        
        if user and str(user.status) == "online":
            await user.send('Sleep bro!')

            logger.debug("waiting for 10 min to give another sleep warning")
            await asyncio.sleep(600)
            user = await self.bot.fetch_user(ADMIN_ID)
            if user and user.status == "online":
                await user.send('Malko Guru!')
        '''

    @daily_sleep_alarm.before_loop
    async def before(self):
        # Trigger at 12.30 am IST
        await sleep_until_time(DAILY_SLEEP_TIME)
        await self.bot.wait_until_ready()


def setup(bot):
    bot.add_cog(SleepRemainder(bot))
