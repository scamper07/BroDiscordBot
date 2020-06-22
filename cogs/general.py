from discord.ext import commands
import discord
import asyncio
import aiohttp
import json
import random
import logging
from logging.handlers import TimedRotatingFileHandler

import logging
from logging.handlers import TimedRotatingFileHandler

''' Initialize logging '''
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = TimedRotatingFileHandler(filename='discord.log', when="midnight", backupCount=5)
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s', datefmt='%d-%b-%y %H:%M:%S'))
logger.addHandler(handler)

class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command(brief='Shows brief introduction of Bro Bot')
    async def intro(self, ctx):
        logger.debug("Sending intro message")
        await ctx.send('```Say Bro and I\'ll bro you back```')

    @commands.command(brief='Bro shares random facts!')
    async def facts(self, ctx):
        logger.debug("facts")
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
        logger.debug("xkcd")
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
