from datetime import date

import discord
from discord.ext import tasks, commands

from constants import DAILY_NEWS_TIME, GENERAL_CHANNEL_ID, NEWS_API_URL
from utility import fetch_json, get_secret, sleep_until_time


class DailyNews(commands.Cog):
    """
    Cog to send the top news headlines to the bros every day at a fixed time
    """

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.channel_list = [GENERAL_CHANNEL_ID]
        self.daily_news.start()

    def cog_unload(self) -> None:
        self.daily_news.cancel()

    @tasks.loop(hours=24.0)
    async def daily_news(self) -> None:
        news_api_key = get_secret("NEWS_API")
        data = await fetch_json(NEWS_API_URL.format(news_api_key))
        for channel in self.channel_list:
            message_channel = self.bot.get_channel(channel)
            if not message_channel:
                continue
            await message_channel.send(
                f"**Today's news {date.today().strftime('%d/%m/%Y')}**"
            )
            if data and data.get("articles"):
                embeds = []
                for article in data["articles"][:7]:
                    embed = discord.Embed(
                        title=article["title"],
                        description=article["description"],
                        url=article["url"],
                        colour=discord.Color.darker_grey(),
                    )
                    embed.set_thumbnail(url=article["urlToImage"])
                    embeds.append(embed)
                await message_channel.send(content="```TOP HEADLINES```", embeds=embeds)

    @daily_news.before_loop
    async def before(self) -> None:
        await sleep_until_time(DAILY_NEWS_TIME)
        await self.bot.wait_until_ready()


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(DailyNews(bot))
