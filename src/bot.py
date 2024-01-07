import os
import discord

from discord.ext import commands
from constants import COMMAND_PREFIX, COGS
from base_logger import logger

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(intents=intents, command_prefix=COMMAND_PREFIX, help_command=None)
bot.remove_command("help")


@bot.event
async def setup_hook() -> None:
    try:
        for cog in COGS:
            logger.info(f"Loading cog : {cog}")
            await bot.load_extension(cog)

        logger.info("All cogs loaded successfully")
    except Exception as err:
        logger.exception(f"Failed to load cog {cog}. ERROR: {err}")


bot.run(os.environ.get("DISCORD_BOT_TOKEN"))
