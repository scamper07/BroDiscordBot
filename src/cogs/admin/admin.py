import discord
from discord.ext import commands
from base_logger import logger
from constants import BOT_ERROR_GIF
from utility import send_embed


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
            await send_embed(self, ctx=ctx, title="Command tree synced!", dm=True)
        except discord.ext.commands.NotOwner as err:
            logger.exception(err)
            await send_embed(
                self,
                ctx=ctx,
                title="Failed to sync command tree, try again later",
                color=discord.Color.red(),
                image_url=BOT_ERROR_GIF,
                dm=True,
            )


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(AdminOnly(bot))
