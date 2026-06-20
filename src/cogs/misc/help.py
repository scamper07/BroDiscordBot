import discord
from discord.ext import commands

from constants import (
    BOT_GITHUB_URL,
    BOT_NAME,
    COMMAND_PREFIX,
    HELP_HIDDEN_COGS,
)
from utility import send_embed


class Help(commands.Cog):
    """
    Cog to handle custom help message
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(description="Displays supported commands")
    async def help(self, ctx):
        """Displays supported commands"""

        embed = discord.Embed(
            title="Help!",
            color=discord.Colour.purple(),
            description="Help information about supported commands",
        )

        # one field per cog, listing its visible commands (embeds allow max 25 fields)
        for cog in self.bot.cogs:
            if cog in HELP_HIDDEN_COGS:
                continue
            visible = [
                command
                for command in self.bot.get_cog(cog).get_commands()
                if not command.hidden
            ]
            if not visible:
                continue
            value = "".join(
                f"`{COMMAND_PREFIX}{command.name:<10}` {command.help}\n"
                for command in visible
            )
            embed.add_field(name=cog, value=value, inline=False)

        # adding info about creator
        embed.add_field(
            name="About",
            value=f"\nVisit {BOT_GITHUB_URL} to submit ideas or issues.",
        )

        embed.set_author(name=BOT_NAME, icon_url=self.bot.user.display_avatar.url)

        await send_embed(ctx, embed)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Help(bot))
