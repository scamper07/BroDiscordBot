import os
import asyncio

from discord.ext import tasks, commands
from base_logger import logger
from config import ALPHA_MALES_GOODIE_BAG_CHANNEL, DEBUG_FLAG_FILE, GENERAL_CHANNEL_ID, TEST_CHANNEL_ID, DAILY_NEWS_TIME
from utils import get_advice, get_news, sleep_until_time
from datetime import date


class DailyNews(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.channel_list = [ALPHA_MALES_GOODIE_BAG_CHANNEL, GENERAL_CHANNEL_ID]
        # self.channel_list = [TEST_CHANNEL_ID]
        self.daily_news.start()

    def cog_unload(self):
        self.daily_news.cancel()

    @tasks.loop(hours=24.0)
    async def daily_news(self):
        # Create DEBUG_FLAG_FILE file to avoid spamming group while testing/disable this cog
        if os.path.exists(DEBUG_FLAG_FILE):
            return

        for channel in self.channel_list:
            message_channel = self.bot.get_channel(channel)
            await message_channel.send("**Today's news ({})**".format(date.today().strftime("%d/%m/%Y")))
            await get_news(message_channel)

    @daily_news.before_loop
    async def before(self):
        # Trigger at 8.30 am IST
        await sleep_until_time(DAILY_NEWS_TIME)
        await self.bot.wait_until_ready()


def setup(bot):
    bot.add_cog(DailyNews(bot))
