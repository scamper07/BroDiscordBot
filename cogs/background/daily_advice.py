from discord.ext import tasks, commands
from base_logger import logger
from config import ALPHA_MALES_GOODIE_BAG_CHANNEL
from utils import get_advice


class DailyAdvice(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.daily_advices.start()

    def cog_unload(self):
        self.daily_advices.cancel()

    @tasks.loop(hours=24.0)
    async def daily_advices(self):
        message_channel = self.bot.get_channel(ALPHA_MALES_GOODIE_BAG_CHANNEL)
        await get_advice(message_channel)

    @daily_advices.before_loop
    async def before(self):
        await self.bot.wait_until_ready()


def setup(bot):
    bot.add_cog(DailyAdvice(bot))
