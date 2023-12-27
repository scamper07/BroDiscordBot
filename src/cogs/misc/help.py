import discord
from discord.ext import commands

from constants import (
    BOT_CREATOR_NAME,
    BOT_GITHUB_URL,
    COMMAND_PREFIX,
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

        # adding module and commands list and description
        for cog in self.bot.cogs:
            if cog != "Help":
                commands = self.bot.get_cog(cog).get_commands()
                if commands:
                    embed.add_field(name=cog, value="", inline=False)
                    for command in commands:
                        if not command.hidden:
                            command_desc = (
                                f" `{COMMAND_PREFIX}{command.name:<8}`"
                                f"  {command.help}\n"
                            )
                            embed.add_field(name=command_desc, value="", inline=False)

        # adding info about creator
        embed.add_field(
            name="About",
            value=f"This bot is developed by {BOT_CREATOR_NAME}"
            f"\nVisit {BOT_GITHUB_URL} to submit ideas or issues.",
        )
        # embed.set_thumbnail(url=self.bot.user.avatar.url)

        await send_embed(self, ctx, embed)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Help(bot))
