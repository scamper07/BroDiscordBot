import asyncio

import discord
from aiohttp import web
from discord.ext import commands

from base_logger import logger
from constants import (
    BOT_NAME,
    F1_DISCUSSION_CHANNEL_ID,
    F1_WEBHOOK_PORT,
    GOODIE_BAG_OFFICIAL_GENERAL_CHANNEL,
)

# substring (lower-case) found in the event title -> formula1.com track icon name
GP_PLACE_MAP = {
    "austria": "Austria",
    "styria": "Styria",
    "hungar": "Hungar",
    "brit": "Great%20Britain",
    "anniversary": "70th%20Anniversary",
    "spanish": "Spain",
    "spain": "Spain",
    "belg": "Belgium",
    "ital": "Italy",
    "toscan": "Tuscany",
    "romagna": "Emilia%20Romagna",
    "turk": "Turkey",
    "bahrain": "Bahrain",
    "sakhir": "Sakhir",
    "abu": "Abu%20Dhab",
    "mexic": "Mexico",
    "brazi": "Brazil",
    "qatar": "Qatar",
    "arabi": "Saudi%20Arabia",
}


class WebHookListener(commands.Cog):
    """
    Cog that listens for F1 calendar webhooks and announces upcoming events
    """

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.channel_list = [
            F1_DISCUSSION_CHANNEL_ID,
            GOODIE_BAG_OFFICIAL_GENERAL_CHANNEL,
        ]
        self.site = None
        self._task = None

    async def cog_load(self) -> None:
        self._task = asyncio.create_task(self.webserver())

    @staticmethod
    def _gp_place(title: str) -> str:
        title = title.lower()
        for needle, place in GP_PLACE_MAP.items():
            if needle in title:
                return place
        return ""

    async def webserver(self) -> None:
        async def handler(request):
            logger.debug(request)
            try:
                res = await request.json()
                logger.info(res)

                embed = discord.Embed(
                    title=res.get("title"),
                    description="Event in 15 minutes",
                    colour=discord.Color.red(),
                )
                embed.set_author(
                    name=BOT_NAME, icon_url=self.bot.user.display_avatar.url
                )
                if "title" in res:
                    gp_place = self._gp_place(res["title"])
                    embed.set_image(
                        url="https://www.formula1.com/content/dam/fom-website/"
                        "2018-redesign-assets/Track%20icons%204x3/"
                        f"{gp_place}%20carbon.png.transform/8col/image.png"
                    )
                if "starts" in res:
                    embed.add_field(
                        name="Date", value=res["starts"] + " IST", inline=False
                    )
                if "location" in res:
                    embed.add_field(name="Track", value=res["location"], inline=True)
                embed.set_footer(text="Hope that was helpful, bye!")
                for channel in self.channel_list:
                    message_channel = self.bot.get_channel(channel)
                    if message_channel:
                        await message_channel.send(embed=embed)
            except Exception as err:
                logger.exception(err)
            return web.Response(text="Success")

        app = web.Application()
        app.router.add_get("/", handler)
        runner = web.AppRunner(app)
        await runner.setup()
        self.site = web.TCPSite(runner, "0.0.0.0", F1_WEBHOOK_PORT)
        await self.bot.wait_until_ready()
        await self.site.start()

    async def cog_unload(self) -> None:
        if self._task:
            self._task.cancel()
        if self.site:
            await self.site.stop()


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(WebHookListener(bot))
