import filecmp
import glob
import os
import subprocess
from pathlib import Path
from shutil import copyfile

import aiohttp
import discord
from discord.ext import tasks, commands

from base_logger import logger
from constants import (
    DAILY_TERRARIA_BACKUP_TIME,
    NGROK_TUNNELS_URL,
    OUTPUT_WORLD_FILE,
    TERRARIA_BACKUP_CHANNEL_ID,
    TERRARIA_WORLDS_BACKUP_DIR,
    TERRARIA_WORLDS_DIR,
)
from utility import send_embed, sleep_until_time

CHECK_RUNNING = (
    '/home/pi/misc/check_running.sh "/bin/bash '
    '/home/pi/misc/server-start-terraria.sh"'
)


class Terraria(commands.Cog):
    """
    Cog to control the Terraria server on the host (requires the Terraria role)
    """

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.daily_world_file_backup.start()

    def cog_unload(self) -> None:
        self.daily_world_file_backup.cancel()

    @commands.command(aliases=["start"], brief="Starts terraria server")
    @commands.has_role("Terraria")
    async def startserver(self, ctx: commands.Context) -> None:
        """Starts the Terraria server"""
        res = subprocess.check_output(CHECK_RUNNING, shell=True)
        if res.decode("UTF-8").strip() == "Running":
            await send_embed(ctx=ctx, title="Server is already running...")
            url = await UtilTerraria.get_terraria_url()
            await send_embed(ctx=ctx, title="URL: " + url)
        else:
            subprocess.Popen(
                ["/home/pi/misc/server-start-screen.sh"], stdout=subprocess.PIPE
            )
            url = await UtilTerraria.get_terraria_url()
            await send_embed(
                ctx=ctx,
                title="Server started, connect after 30 seconds...\nURL: " + url[6:],
            )

    @commands.command(aliases=["stop"], brief="Stops terraria server")
    @commands.has_role("Terraria")
    async def stopserver(self, ctx: commands.Context) -> None:
        """Stops the Terraria server"""
        subprocess.Popen(
            ["/home/pi/misc/server-stop-terraria.sh"], stdout=subprocess.PIPE
        )
        await send_embed(ctx=ctx, title="Stopping Server... Bye!")

    @commands.command(aliases=["url"], brief="Gets terraria server url")
    @commands.has_role("Terraria")
    async def serverurl(self, ctx: commands.Context) -> None:
        """Gets the Terraria server url"""
        res = subprocess.check_output(CHECK_RUNNING, shell=True)
        if res.decode("UTF-8").strip() == "Not Running":
            await send_embed(
                ctx=ctx,
                title="Server is not running, start server and try again...",
            )
        else:
            url = await UtilTerraria.get_terraria_url()
            await send_embed(ctx=ctx, title="URL: " + url[6:])

    @commands.command(aliases=["gwf"], brief="gets world files")
    @commands.has_role("Terraria")
    async def getworldfile(self, ctx: commands.Context) -> None:
        """Generates and sends the latest world file backup"""
        await UtilTerraria.generate_backup_and_send(ctx)

    @tasks.loop(hours=168)
    async def daily_world_file_backup(self) -> None:
        message_channel = self.bot.get_channel(TERRARIA_BACKUP_CHANNEL_ID)
        if message_channel:
            await UtilTerraria.backup_world_file(message_channel)

    @daily_world_file_backup.before_loop
    async def before(self) -> None:
        await sleep_until_time(DAILY_TERRARIA_BACKUP_TIME)
        await self.bot.wait_until_ready()


class UtilTerraria:
    """
    Utility helpers for the Terraria cog
    """

    @staticmethod
    async def get_terraria_url():
        """Fetches the terraria server's public ngrok url"""
        session = aiohttp.ClientSession()
        try:
            async with session.get(NGROK_TUNNELS_URL) as resp:
                data_json = await resp.json()
        finally:
            await session.close()

        msg = ""
        for tunnel in data_json["tunnels"]:
            if tunnel["name"] == "terraria":
                msg = tunnel["public_url"]
        return msg

    @staticmethod
    async def backup_world_file(ctx):
        """Backs up the world files, regenerating the archive if they changed"""
        try:
            backup_files = {}
            for bworld_file in glob.glob(TERRARIA_WORLDS_BACKUP_DIR + "*.wld"):
                backup_files[bworld_file] = os.path.join(
                    TERRARIA_WORLDS_BACKUP_DIR, bworld_file
                )

            latest_files = {}
            for world_file in glob.glob(TERRARIA_WORLDS_DIR + "*.wld"):
                latest_files[world_file] = os.path.join(TERRARIA_WORLDS_DIR, world_file)
                if not backup_files:
                    # first seed
                    if not os.path.exists(TERRARIA_WORLDS_BACKUP_DIR):
                        os.makedirs(TERRARIA_WORLDS_BACKUP_DIR)
                    copyfile(
                        latest_files[world_file],
                        os.path.join(TERRARIA_WORLDS_BACKUP_DIR, world_file),
                    )

            if backup_files:
                for file in latest_files:
                    if file in backup_files:
                        result = filecmp.cmp(
                            latest_files[file], backup_files[file], shallow=False
                        )
                        # current files become the new backup
                        for f in backup_files:
                            os.remove(backup_files[f])
                            copyfile(
                                latest_files[f],
                                os.path.join(TERRARIA_WORLDS_BACKUP_DIR, f),
                            )
                        if result:
                            # files unchanged, nothing to send
                            return 1
            await UtilTerraria.generate_backup_and_send(ctx)
            return 0
        except Exception as err:
            logger.exception(err)

    @staticmethod
    async def generate_backup_and_send(ctx):
        """Zips the world files and sends the archive to the channel"""
        try:
            await send_embed(ctx=ctx, title="Generating file...Please wait...")
            ret = subprocess.call(["sh", "/home/pi/misc/world_file_generate.sh"])
            if ret == 0:
                if Path(OUTPUT_WORLD_FILE).is_file():
                    await ctx.send(file=discord.File(OUTPUT_WORLD_FILE))
                else:
                    await send_embed(ctx=ctx, title="Failed, try again later...")
                    subprocess.call(["sh", "/home/pi/misc/world_file_remove.sh"])
            else:
                await send_embed(
                    ctx=ctx, title="Zip process failed, try again later..."
                )
        except Exception as err:
            logger.exception(err)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Terraria(bot))
