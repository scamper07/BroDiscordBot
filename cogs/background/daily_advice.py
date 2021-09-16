import os
from discord.ext import tasks, commands
from base_logger import logger
from config import ALPHA_MALES_GOODIE_BAG_CHANNEL, GENERAL_CHANNEL_ID, TEST_CHANNEL_ID, \
    DAILY_ADVICE_TIME
from utils import get_advice, sleep_until_time
from datetime import date


class DailyAdvice(commands.Cog):
    """
    A cog for daily advice
    """
    def __init__(self, bot):
        self.bot = bot
        self.channel_list = [ALPHA_MALES_GOODIE_BAG_CHANNEL, GENERAL_CHANNEL_ID]
        # self.channel_list = [TEST_CHANNEL_ID]
        self.daily_advices.start()

    def cog_unload(self):
        self.daily_advices.cancel()

    @tasks.loop(hours=24.0)
    async def daily_advices(self):
        """Function to send news everyday at DAILY_ADVICE_TIME"""
        for channel in self.channel_list:
            message_channel = self.bot.get_channel(channel)
            await message_channel.send("**Today's advice for the bros**")
            await get_advice(message_channel)

    @daily_advices.before_loop
    async def before(self):
        # Trigger at DAILY_ADVICE_TIME
        await sleep_until_time(DAILY_ADVICE_TIME)
        await self.bot.wait_until_ready()


def setup(bot):
    bot.add_cog(DailyAdvice(bot))
