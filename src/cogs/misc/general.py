import json
import random
import aiohttp
import discord

from discord.ext import commands
from base_logger import logger
from constants import (
    ADVICE_API_URL,
    BOT_ERROR_GIF,
    BOT_INTRO_MESSAGE,
    BOT_INTRO_GIF,
    FACT_API_URL,
    INSULT_API_URL,
    NEWS_API_URL,
    XKCD_COMIC_URL,
    XKCD_LATEST_URL,
)
from utility import fetch_json, get_secret, send_embed


class General(commands.Cog):
    """
    Cog to handle general commands
    """

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.hybrid_command(description="Shows bot intro")
    async def intro(self, ctx: commands.Context) -> None:
        """Sends out the bot introduction message"""
        async with ctx.typing():
            await send_embed(ctx=ctx, title=BOT_INTRO_MESSAGE, image_url=BOT_INTRO_GIF)

    @commands.hybrid_command(description="Fetches random xkcd comic")
    async def xkcd(self, ctx: commands.Context) -> None:
        """Sends out a random xkcd comic"""
        async with ctx.typing():
            json_response = await UtilGeneral.get_xkcd_comic()
            if json_response:
                await send_embed(
                    ctx=ctx,
                    title=json_response["title"],
                    image_url=json_response["img"],
                )
            else:
                await send_embed(
                    ctx=ctx,
                    title="Failed to fetch comic, try again later",
                    color=discord.Color.red(),
                    image_url=BOT_ERROR_GIF,
                )

    @commands.hybrid_command(description="Bro shares a random fact")
    async def fact(self, ctx: commands.Context) -> None:
        """Sends out a random fact"""
        async with ctx.typing():
            data = await fetch_json(FACT_API_URL)
            if data and data.get("fact"):
                await send_embed(ctx=ctx, title=data["fact"])
            else:
                await UtilGeneral.send_error(ctx)

    @commands.hybrid_command(description="Bro gives a life advice")
    async def advice(self, ctx: commands.Context) -> None:
        """Sends out a random advice"""
        async with ctx.typing():
            data = await fetch_json(ADVICE_API_URL)
            if data and data.get("slip"):
                await send_embed(ctx=ctx, title=data["slip"]["advice"])
            else:
                await UtilGeneral.send_error(ctx)

    @commands.hybrid_command(description="Get insulted by Bro")
    async def insult(self, ctx: commands.Context) -> None:
        """Sends out a random insult"""
        async with ctx.typing():
            data = await fetch_json(INSULT_API_URL)
            if data and data.get("insult"):
                await send_embed(ctx=ctx, title=data["insult"])
            else:
                await UtilGeneral.send_error(ctx)

    @commands.hybrid_command(description="Bro shares BREAKING NEWS!")
    async def news(self, ctx: commands.Context) -> None:
        """Sends out the top news headlines"""
        async with ctx.typing():
            news_api_key = get_secret("NEWS_API")
            if not news_api_key:
                await send_embed(
                    ctx=ctx,
                    title="News is not configured (set NEWS_API)",
                    color=discord.Color.red(),
                    image_url=BOT_ERROR_GIF,
                )
                return
            data = await fetch_json(NEWS_API_URL.format(news_api_key))
            if data and data.get("articles"):
                headlines = ""
                for index, article in enumerate(data["articles"][:7], start=1):
                    headlines += f"{index}. {article['title']}\n"
                await send_embed(ctx=ctx, title="TOP HEADLINES", description=headlines)
            else:
                await UtilGeneral.send_error(ctx)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(General(bot))


class UtilGeneral:
    """
    Utility helpers for the General cog
    """

    @staticmethod
    async def send_error(ctx):
        """Send a generic error embed"""
        await send_embed(
            ctx=ctx,
            title="Sorry, try again later",
            color=discord.Color.red(),
            image_url=BOT_ERROR_GIF,
        )

    @staticmethod
    async def get_xkcd_comic():
        """Fetch a random xkcd comic"""
        json_response = None
        session = aiohttp.ClientSession()
        try:
            # fetch latest comic to get the last (latest) index
            async with session.get(XKCD_LATEST_URL) as resp:
                data = await resp.read()

            # select a random comic from 1 to latest
            comic_number = random.randint(1, json.loads(data)["num"])
            logger.debug(f"Comic number: {comic_number}")

            async with session.get(XKCD_COMIC_URL.format(comic_number)) as resp:
                data = await resp.read()
                json_response = json.loads(data)
        except Exception as err:
            logger.exception(err)
        finally:
            await session.close()

        return json_response
