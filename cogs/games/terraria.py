import discord
from discord.ext import commands
from utils import embed_send, get_terraria_url, backup_world_file
from base_logger import logger
import subprocess
from pathlib import Path
from asyncio import sleep
import asyncio
from subprocess import Popen


class Terraria(commands.Cog):
    """
    A cog for terraria server control commands
    """
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["start"], brief='Starts terraria server')
    @commands.has_role("Terraria")
    async def startserver(self, ctx):
        # check if server is already running
        res = subprocess.check_output(
            "/home/pi/misc/check_running.sh \"/bin/bash /home/pi/misc/server-start-terraria.sh\"", shell=True)
        if res.decode('UTF-8').strip() == "Running":
            embed = discord.Embed(title="Server is already running...")
            await embed_send(ctx, embed)
            url = await get_terraria_url()
            embed = discord.Embed(title="URL: " + url)
            await embed_send(ctx, embed)
        else:
            subprocess.Popen(["/home/pi/misc/server-start-screen.sh"], stdout=subprocess.PIPE)
            url = await get_terraria_url()
            embed = discord.Embed(title="Server started, connect after 30 seconds...\nURL: "+url)
            await embed_send(ctx, embed)

    @commands.command(aliases=["stop"], brief='Stops terraria server')
    @commands.has_role("Terraria")
    async def stopserver(self, ctx):
        subprocess.Popen(["/home/pi/misc/server-stop-terraria.sh"], stdout=subprocess.PIPE)
        embed = discord.Embed(title="Stopping Server... Bye!")
        await embed_send(ctx, embed)

    @commands.command(aliases=["url"], brief='Gets terraria server url')
    @commands.has_role("Terraria")
    async def serverurl(self, ctx):
        res = subprocess.check_output(
            "/home/pi/misc/check_running.sh \"/bin/bash /home/pi/misc/server-start-terraria.sh\"", shell=True)
        if res.decode('UTF-8').strip() == "Not Running":
            embed = discord.Embed(title="Server is not running, start server and try again...")
            await embed_send(ctx, embed)
        else:
            url = await get_terraria_url()
            embed = discord.Embed(title="URL: "+url[6:])
            await embed_send(ctx, embed)

    @commands.command(aliases=["gwf"], brief='gets world files')
    @commands.has_role("Terraria")
    async def getworldfile(self, ctx):
        await backup_world_file(ctx)


def setup(bot):
    bot.add_cog(Terraria(bot))
