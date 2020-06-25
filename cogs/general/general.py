import discord
import aiohttp
import json
import random
from discord.ext import commands
from base_logger import logger
from utils import get_advice


class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(brief='Shows brief introduction of Bro Bot')
    async def intro(self, ctx):
        logger.debug("Sending intro message")
        await ctx.send('```Say Bro and I\'ll bro you back```')

    @commands.command(brief='Bro shares random facts!')
    async def facts(self, ctx):
        logger.debug("Generating a fact")
        wait_message = await ctx.send("One interesting fact coming right up...")
        async with ctx.typing():
            try:
                session = aiohttp.ClientSession()
                async with session.get("https://useless-facts.sameerkumar.website/api") as resp:
                    data = await resp.read()
                json_response = json.loads(data)
                await session.close()
                await wait_message.delete()
                await ctx.send("{}".format(json_response['data']))
            except Exception as e:
                logger.exception(e)
                await ctx.send('Sorry can\'t think of anything')

    @commands.command(brief='Puts out random xkcd comic!')
    async def xkcd(self, ctx):
        logger.debug("Generating an xkcd comic")
        wait_message = await ctx.send("Comic time...")
        comic_number = random.randint(1, 2310)  # comic number range TODO:get dynamically
        logger.debug(comic_number)
        async with ctx.typing():
            try:
                session = aiohttp.ClientSession()
                url = "https://xkcd.com/{}/info.0.json".format(comic_number)
                async with session.get(url) as resp:
                    data = await resp.read()
                json_response = json.loads(data)
                await session.close()
                await wait_message.delete()
                embed = discord.Embed(title=json_response['title'])
                embed.set_image(url=json_response['img'])
                await ctx.send(embed=embed)
            except Exception as e:
                logger.exception(e)
                await ctx.send('No xkcd for you')

    @commands.command(brief='Bro gives life advices!')
    async def advice(self, ctx):
        await get_advice(ctx)

    @commands.command(brief='Bro insults')
    async def insult(self, ctx):
        logger.debug("insult")
        wait_message = await ctx.send("Buckle up Butter cup...")
        async with ctx.typing():
            try:
                session = aiohttp.ClientSession()
                url = "https://insult.mattbas.org/api/insult.json"
                async with session.get(url) as resp:
                    data = await resp.read()
                json_response = json.loads(data)
                await session.close()
                await wait_message.delete()
                await ctx.send("{}".format(json_response['insult']))
            except Exception as e:
                logger.exception(e)
                await ctx.send('No insult for you. Get a life')


def setup(bot):
    bot.add_cog(General(bot))
