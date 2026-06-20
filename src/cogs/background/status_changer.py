from itertools import cycle

import discord
from discord.ext import tasks, commands

from base_logger import logger
from constants import COMMAND_PREFIX


class StatusChanger(commands.Cog):
    """
    Cog to cycle through the bot's presence statuses
    """

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        listening_help = discord.Activity(
            name=f"{COMMAND_PREFIX}help", type=discord.ActivityType.listening
        )
        self.status = cycle(
            [
                listening_help,
                discord.Activity(
                    name="Game Of The Year",
                    url="https://www.youtube.com/watch?v=oHg5SJYRHA0",
                    type=discord.ActivityType.streaming,
                ),
                discord.Activity(name="Spotify", type=discord.ActivityType.listening),
                listening_help,
                discord.Activity(name="with fire", type=discord.ActivityType.playing),
                discord.Activity(name="VALORANT", type=discord.ActivityType.playing),
                discord.Activity(
                    name="Rocket League", type=discord.ActivityType.playing
                ),
                listening_help,
                discord.Activity(
                    name="Apex Legends", type=discord.ActivityType.playing
                ),
                discord.Activity(
                    name="out for you!", type=discord.ActivityType.watching
                ),
                listening_help,
            ]
        )
        self.change_status.start()

    def cog_unload(self) -> None:
        self.change_status.cancel()

    @tasks.loop(minutes=30)
    async def change_status(self) -> None:
        logger.debug("Changing status...")
        await self.bot.change_presence(activity=next(self.status))

    @change_status.before_loop
    async def before(self) -> None:
        await self.bot.wait_until_ready()


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(StatusChanger(bot))
