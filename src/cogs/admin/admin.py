import os
import subprocess
from typing import Literal

import aiohttp
import discord
from discord.ext import commands
from base_logger import logger
from constants import (
    BOT_ERROR_GIF,
    BOT_NAME,
    GENERAL_CHANNEL_ID,
    NGROK_TUNNELS_URL,
    TEST_CHANNEL_ID,
    TEST2_CHANNEL_ID,
)
from utility import get_secret, send_embed


class AdminOnly(commands.Cog):
    """
    Cog to handle admin only commands
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(hidden=True)
    @commands.is_owner()
    async def sync(self, ctx):
        """Syncs all slash commands"""
        try:
            await self.bot.tree.sync()
            logger.debug("Command tree synced!")
            await send_embed(ctx=ctx, title="Command tree synced!", dm=True)
        except discord.ext.commands.NotOwner as err:
            logger.exception(err)
            await send_embed(
                ctx=ctx,
                title="Failed to sync command tree, try again later",
                color=discord.Color.red(),
                image_url=BOT_ERROR_GIF,
                dm=True,
            )


class Admin(commands.Cog):
    """
    Cog to handle host machine admin commands
    """

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.hybrid_command(description="Turns on/off my Master's PC")
    @commands.is_owner()
    async def power(self, ctx: commands.Context, arg: Literal["on", "off"]) -> None:
        """Powers my Master's PC on or off (owner only)"""
        try:
            admin_id = get_secret("ADMIN_ID")
            if ctx.author.id != int(admin_id):
                await send_embed(ctx=ctx, title="Only my master can use this command")
                return

            if arg.lower() == "on":
                master_mac = get_secret("MASTER_MAC")
                logger.debug("Powering on PC")
                os.system(f"wakeonlan {master_mac}")
                await send_embed(ctx=ctx, title="Powering on PC")
            else:
                master_ip = get_secret("MASTER_IP")
                logger.debug("Shutting down PC")
                os.system(f"ssh preetham@{master_ip} shutdown /s")
                await send_embed(ctx=ctx, title="Shutting down PC")
        except Exception as err:
            logger.exception(err)
            await send_embed(
                ctx=ctx,
                title="Sorry, try again later",
                color=discord.Color.red(),
                image_url=BOT_ERROR_GIF,
            )

    @commands.command(hidden=True)
    @commands.is_owner()
    async def post(self, ctx: commands.Context, *args) -> None:
        """Posts a message to a channel as the bot (owner only)"""
        if args and args[0] == "gb":
            channel = self.bot.get_channel(TEST2_CHANNEL_ID)
            message = " ".join(args[1:])
        elif args and args[0] == "test":
            channel = self.bot.get_channel(TEST_CHANNEL_ID)
            message = " ".join(args[1:])
        else:
            channel = self.bot.get_channel(GENERAL_CHANNEL_ID)
            message = " ".join(args)
        logger.debug(f"{len(args)} {message}")
        await channel.send(message)

    @commands.hybrid_command(description="Shows my host hardware-software info")
    async def sysinfo(self, ctx: commands.Context) -> None:
        """Shows my host hardware/software information"""
        async with ctx.typing():
            try:
                embed = discord.Embed(
                    title="System Info",
                    description="Showing my host hardware/software information",
                    colour=discord.Color.gold(),
                )
                embed.set_footer(text="Hope that was helpful, bye!")
                embed.set_author(
                    name=BOT_NAME, icon_url=self.bot.user.display_avatar.url
                )
                if ctx.guild and ctx.guild.icon:
                    embed.set_thumbnail(url=ctx.guild.icon.url)

                result = subprocess.Popen(
                    ["neofetch", "--stdout"], stdout=subprocess.PIPE
                )
                for line in result.stdout:
                    line = line.decode("utf-8").strip("\n").split(":")
                    if len(line) == 2:
                        inline = line[0] not in ("OS", "Host")
                        embed.add_field(name=line[0], value=line[1], inline=inline)

                # Raspberry Pi only extras
                if os.uname()[1] == "anton":
                    temp = subprocess.Popen(
                        ["/opt/vc/bin/vcgencmd", "measure_temp"],
                        stdout=subprocess.PIPE,
                    )
                    for line in temp.stdout:
                        line = line.decode("utf-8").strip("\n").split("=")
                        if len(line) == 2:
                            embed.add_field(name="CPU Temp", value=line[1], inline=True)

                    url = await Admin.get_public_url()
                    embed.add_field(name="Public URL", value=url, inline=False)

                await send_embed(ctx=ctx, embed=embed)
            except Exception as err:
                logger.exception(err)
                await send_embed(
                    ctx=ctx,
                    title="Sorry, try again later",
                    color=discord.Color.red(),
                    image_url=BOT_ERROR_GIF,
                )

    @commands.command(hidden=True)
    @commands.is_owner()
    async def runcmd(self, ctx: commands.Context, *args) -> None:
        """Runs a shell command on the host and returns its output (owner only)"""
        logger.debug(args)
        try:
            result = subprocess.Popen(args, stdout=subprocess.PIPE)
            out = ""
            for line in result.stdout:
                out += line.decode("utf-8")
            logger.debug(out)
            await send_embed(ctx=ctx, title=out)
        except Exception as err:
            logger.exception(err)
            await send_embed(
                ctx=ctx,
                title="Sorry, try again later",
                color=discord.Color.red(),
                image_url=BOT_ERROR_GIF,
            )

    @staticmethod
    async def get_public_url():
        """Fetch the ngrok public url of the host"""
        session = aiohttp.ClientSession()
        try:
            async with session.get(NGROK_TUNNELS_URL) as resp:
                data_json = await resp.json()
        finally:
            await session.close()

        return "\n".join(tunnel["public_url"] for tunnel in data_json["tunnels"])


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(AdminOnly(bot))
    await bot.add_cog(Admin(bot))
