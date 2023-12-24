import os
import discord

from discord.ext import commands
from constants import COGS

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(intents=intents, command_prefix=".")


@bot.event
async def setup_hook() -> None:
    for cog in COGS:
        await bot.load_extension(cog)


@bot.command()
async def sync(ctx):
    print("sync command")
    await bot.tree.sync()
    await ctx.send("Command tree synced.")


bot.run(os.environ.get("DISCORD_BOT_TOKEN"))
