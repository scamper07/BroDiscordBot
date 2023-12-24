import discord

from discord.ext import commands


class General(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        await self.bot.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.watching, name="my guts being removed"))


    @commands.hybrid_command(name="intro")
    async def intro(self, ctx: commands.Context) -> None:
        await ctx.send("Hello!")


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(General(bot))
