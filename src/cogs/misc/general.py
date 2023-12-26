import json
import random
import aiohttp
import discord

from discord.ext import commands
from base_logger import logger
from constants import BOT_ERROR_GIF, BOT_INTRO_MESSAGE, BOT_INTRO_GIF
from utility import send_embed


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
            await send_embed(
                self, ctx=ctx, title=BOT_INTRO_MESSAGE, image_url=BOT_INTRO_GIF
            )

    @commands.hybrid_command(description="Fetches random xkcd comic")
    async def xkcd(self, ctx: commands.Context) -> None:
        """Sends out a random xkcd comic"""
        async with ctx.typing():
            try:
                session = aiohttp.ClientSession()
                # fetch latest comic
                url = "https://xkcd.com/info.0.json"
                async with session.get(url) as resp:
                    data = await resp.read()
                    json_response = json.loads(data)

                # select random comic from 1 to latest
                comic_number = random.randint(1, json_response["num"])
                logger.debug(f"Comic number: {comic_number}")

                url = f"https://xkcd.com/{comic_number}/info.0.json"
                async with session.get(url) as resp:
                    data = await resp.read()
                    json_response = json.loads(data)

                await send_embed(
                    self,
                    ctx=ctx,
                    title=json_response["title"],
                    image_url=json_response["img"],
                )

            except Exception as err:
                logger.exception(err)
                await send_embed(
                    self,
                    ctx=ctx,
                    color=discord.Color.red(),
                    image_url=BOT_ERROR_GIF,
                )

            finally:
                await session.close()


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(General(bot))
