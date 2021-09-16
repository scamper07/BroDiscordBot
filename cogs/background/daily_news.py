import os
import aiohttp
import discord
from discord.ext import tasks, commands
from base_logger import logger
from config import ALPHA_MALES_GOODIE_BAG_CHANNEL, GENERAL_CHANNEL_ID, TEST_CHANNEL_ID, DAILY_NEWS_TIME
from utils import get_news, sleep_until_time
from datetime import date
from discord import Webhook, AsyncWebhookAdapter


class DailyNews(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # self.channel_list = [ALPHA_MALES_GOODIE_BAG_CHANNEL, GENERAL_CHANNEL_ID]
        self.channel_list = [GENERAL_CHANNEL_ID]
        self.daily_news.start()

    def cog_unload(self):
        self.daily_news.cancel()

    @tasks.loop(hours=24.0)
    async def daily_news(self):
        for channel in self.channel_list:
            message_channel = self.bot.get_channel(channel)
            await message_channel.send("**Today's news **".format(date.today().strftime("%d/%m/%Y")))
            logger.debug("PRE: {}".format(type(message_channel)))
            await get_news(message_channel)

    @daily_news.before_loop
    async def before(self):
        # Trigger at 8.30 am IST
        await sleep_until_time(DAILY_NEWS_TIME)
        await self.bot.wait_until_ready()


def setup(bot):
    bot.add_cog(DailyNews(bot))
