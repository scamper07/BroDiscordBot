import os
import discord

from dotenv import load_dotenv
from discord.ext import commands
from constants import COMMAND_PREFIX, COGS
from base_logger import logger

# Load environment variables from a local .env file when present
load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(intents=intents, command_prefix=COMMAND_PREFIX, help_command=None)
bot.remove_command("help")


@bot.event
async def setup_hook() -> None:
    loaded = 0
    for cog in COGS:
        logger.info(f"Loading cog : {cog}")
        try:
            await bot.load_extension(cog)
            loaded += 1
        except Exception as err:
            logger.exception(f"Failed to load cog {cog}. ERROR: {err}")

    logger.info(f"Loaded {loaded}/{len(COGS)} cogs")


token = os.environ.get("DISCORD_BOT_TOKEN")
if not token:
    raise SystemExit(
        "DISCORD_BOT_TOKEN is not set. Add it to a .env file or your environment."
    )

bot.run(token)
