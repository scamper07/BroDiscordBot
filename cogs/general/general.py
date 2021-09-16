import discord
import discord_slash
from constants import *
from discord.ext import commands
from base_logger import logger
from utils import get_advice, get_news, get_fact, get_insult, get_xkcd, embed_send, get_intro
from discord_slash import cog_ext, SlashContext, SlashCommand


class General(commands.Cog):
    """
    A cog for random general commands
    """
    def __init__(self, bot):
        self.bot = bot
        if not hasattr(bot, "slash"):
            bot.slash = SlashCommand(bot, auto_register=True, override_type=True, auto_delete=True, sync_commands=True)
        self.bot.slash.get_cog_commands(self)

    def cog_unload(self):
        self.bot.slash.remove_cog_commands(self)

    @commands.command(brief=DESCRIPTION_INTRO)
    async def intro(self, ctx):
        """prefix command for _intro"""
        async with ctx.typing():
            await get_intro(ctx)

    @cog_ext.cog_slash(name="intro",
                       description=DESCRIPTION_INTRO,
                       )
    async def intros(self, ctx: SlashContext):
        """slash command for _intro"""
        await get_intro(ctx)

    @commands.command(brief=DESCRIPTION_FACT)
    async def fact(self, ctx):
        """prefix command for getting a random fact"""
        async with ctx.typing():
            await get_fact(ctx)

    @cog_ext.cog_slash(name="fact",
                       description=DESCRIPTION_FACT,
                       )
    async def facts(self, ctx: SlashContext):
        """slash command for getting a random fact"""
        await get_fact(ctx)

    @commands.command(brief=DESCRIPTION_XKCD)
    async def xkcd(self, ctx):
        async with ctx.typing():
            """prefix command for getting a random xkcd comic"""
            await get_xkcd(ctx)

    @cog_ext.cog_slash(name="xkcd",
                       description=DESCRIPTION_XKCD,
                       )
    async def xkcds(self, ctx: SlashContext):
        """slash command for getting a random xkcd comic"""
        await get_xkcd(ctx)

    @commands.command(brief=DESCRIPTION_ADVICE)
    async def advice(self, ctx):
        """prefix command for getting a random advice"""
        async with ctx.typing():
            await get_advice(ctx)

    @cog_ext.cog_slash(name="advice",
                       description=DESCRIPTION_ADVICE,
                       )
    async def advices(self, ctx: SlashContext):
        """slash command for getting a random advice"""
        await get_advice(ctx)

    @commands.command(brief=DESCRIPTION_INSULT)
    async def insult(self, ctx):
        async with ctx.typing():
            """slash command for getting a random insult"""
            await get_insult(ctx)

    @cog_ext.cog_slash(name="insult",
                       description=DESCRIPTION_INSULT,
                       )
    async def insults(self, ctx: SlashContext):
        """slash command for getting a random insult"""
        await get_insult(ctx)

    @commands.command(brief=DESCRIPTION_NEWS)
    async def news(self, ctx):
        """prefix command for getting news"""
        async with ctx.typing():
            await get_news(ctx)

    @cog_ext.cog_slash(name="news",
                       description=DESCRIPTION_NEWS,
                       )
    async def newss(self, ctx: SlashContext):
        """slash command for getting news"""
        await get_news(ctx)


def setup(bot):
    bot.add_cog(General(bot))
