from discord.ext import tasks, commands

from base_logger import logger
from constants import DAILY_SLEEP_TIME
from utility import get_secret, sleep_until_time


class SleepRemainder(commands.Cog):
    """
    Cog to remind the admin to sleep at a fixed time every day
    """

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.daily_sleep_alarm.start()

    def cog_unload(self) -> None:
        self.daily_sleep_alarm.cancel()

    @tasks.loop(hours=24.0)
    async def daily_sleep_alarm(self) -> None:
        admin_id = get_secret("ADMIN_ID")
        if not admin_id:
            logger.debug("ADMIN_ID not configured, skipping sleep reminder")
            return
        user = await self.bot.fetch_user(int(admin_id))
        logger.debug(f"daily_sleep_alarm for {user}")
        await user.send("Sleep bro!")

    @daily_sleep_alarm.before_loop
    async def before(self) -> None:
        await sleep_until_time(DAILY_SLEEP_TIME)
        await self.bot.wait_until_ready()


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(SleepRemainder(bot))
