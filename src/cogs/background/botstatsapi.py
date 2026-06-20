import asyncio

from aiohttp import web
from discord.ext import commands

from constants import BOTSTATS_API_PORT


class BotStatsAPI(commands.Cog):
    """
    Cog to serve web APIs
    """

    def __init__(self, bot):
        self.bot = bot
        self.site = None
        self._task = None

    async def cog_load(self) -> None:
        self._task = asyncio.create_task(self.webserver())

    async def cog_unload(self) -> None:
        if self._task:
            self._task.cancel()
        if self.site:
            await self.site.stop()

    async def webserver(self):
        async def handler(request):
            data = {
                "status": "Online" if "Bro" in str(self.bot.user) else "Offline",
                "count": str(len(self.bot.guilds)),
            }
            return web.json_response(data)

        app = web.Application()
        app.router.add_get("/", handler)

        runner = web.AppRunner(app)
        await runner.setup()
        self.site = web.TCPSite(runner, "0.0.0.0", BOTSTATS_API_PORT)
        await self.bot.wait_until_ready()
        await self.site.start()


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(BotStatsAPI(bot))
