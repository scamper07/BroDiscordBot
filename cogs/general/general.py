import discord
import discord_slash
from discord.ext import commands
from base_logger import logger
from utils import get_advice, get_news, get_fact, get_insult, get_xkcd, embed_send
from discord_slash import cog_ext, SlashContext, SlashCommand


class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        if not hasattr(bot, "slash"):
            bot.slash = SlashCommand(bot, auto_register=True, override_type=True, auto_delete=True, sync_commands=True)
        self.bot.slash.get_cog_commands(self)

    def cog_unload(self):
        self.bot.slash.remove_cog_commands(self)

    async def _intro(self, ctx):
        logger.debug("Sending intro message")
        embed = discord.Embed(title="Say Bro and I\'ll bro you back")
        embed.set_image(url="https://media.giphy.com/media/l0K45p4XQTVmyClMs/giphy.gif")
        await embed_send(ctx, embed)

    @commands.command(brief='Shows brief introduction of Bro Bot')
    async def intro(self, ctx):
        async with ctx.typing():
            await self._intro(ctx)

    @cog_ext.cog_slash(name="intro",
                       description='Shows brief introduction of Bro Bot',
                       #guild_ids=[207481917975560192, 572648167573684234]
                       )
    async def intros(self, ctx: SlashContext):
        await self._intro(ctx)

    @commands.command(brief='Bro shares random facts!')
    async def fact(self, ctx):
        async with ctx.typing():
            await get_fact(ctx)

    @cog_ext.cog_slash(name="fact",
                       description='Bro shares random facts!',
                       #guild_ids=[207481917975560192, 572648167573684234]
                       )
    async def facts(self, ctx: SlashContext):
        await get_fact(ctx)

    @commands.command(brief='Puts out random xkcd comic!')
    async def xkcd(self, ctx):
        async with ctx.typing():
            await get_xkcd(ctx)

    @cog_ext.cog_slash(name="xkcd",
                       description='Puts out random xkcd comic!',
                       #guild_ids=[207481917975560192, 572648167573684234]
                       )
    async def xkcds(self, ctx: SlashContext):
        await get_xkcd(ctx)

    @commands.command(brief='Bro gives life advices!')
    async def advice(self, ctx):
        async with ctx.typing():
            await get_advice(ctx)

    @cog_ext.cog_slash(name="advice",
                       description='Bro gives life advices!',
                       #guild_ids=[207481917975560192, 572648167573684234]
                       )
    async def advices(self, ctx: SlashContext):
        await get_advice(ctx)

    @commands.command(brief='Get insulted by Bro')
    async def insult(self, ctx):
        async with ctx.typing():
            await get_insult(ctx)

    @cog_ext.cog_slash(name="insult",
                       description='Get insulted by Bro',
                       #guild_ids=[207481917975560192, 572648167573684234]
                       )
    async def insults(self, ctx: SlashContext):
        await get_insult(ctx)

    @commands.command(brief='Bro shares BREAKING NEWS!!!')
    async def news(self, ctx):
        async with ctx.typing():
            await get_news(ctx)

    @cog_ext.cog_slash(name="news",
                       description='Bro shares BREAKING NEWS!!!',
                       #guild_ids=[207481917975560192, 572648167573684234]
                       )
    async def newss(self, ctx: SlashContext):
        await get_news(ctx)


def setup(bot):
    bot.add_cog(General(bot))
