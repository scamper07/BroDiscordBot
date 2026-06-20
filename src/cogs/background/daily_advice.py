import discord
from discord.ext import tasks, commands

from constants import (
    ADVICE_API_URL,
    ALPHA_MALES_GOODIE_BAG_CHANNEL,
    DAILY_ADVICE_TIME,
    GENERAL_CHANNEL_ID,
)
from utility import fetch_json, sleep_until_time


class DailyAdvice(commands.Cog):
    """
    Cog to send a daily advice to the bros at a fixed time
    """

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.channel_list = [ALPHA_MALES_GOODIE_BAG_CHANNEL, GENERAL_CHANNEL_ID]
        self.daily_advices.start()

    def cog_unload(self) -> None:
        self.daily_advices.cancel()

    @tasks.loop(hours=24.0)
    async def daily_advices(self) -> None:
        data = await fetch_json(ADVICE_API_URL)
        for channel in self.channel_list:
            message_channel = self.bot.get_channel(channel)
            if not message_channel:
                continue
            await message_channel.send("**Today's advice for the bros**")
            if data:
                await message_channel.send(
                    embed=discord.Embed(title=data["slip"]["advice"])
                )

    @daily_advices.before_loop
    async def before(self) -> None:
        await sleep_until_time(DAILY_ADVICE_TIME)
        await self.bot.wait_until_ready()


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(DailyAdvice(bot))
