from aiohttp import web
import asyncio
from discord.ext import commands


class BotStatsAPI(commands.Cog):
    """
    Cog to serve web APIs
    """

    def __init__(self, bot):
        self.bot = bot

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
        self.site = web.TCPSite(runner, "0.0.0.0", 8999)
        await self.bot.wait_until_ready()
        await self.site.start()

    def __unload(self):
        asyncio.ensure_future(self.site.stop())


async def setup(bot: commands.Bot) -> None:
    api = BotStatsAPI(bot)
    await bot.add_cog(api)
    bot.loop.create_task(api.webserver())
