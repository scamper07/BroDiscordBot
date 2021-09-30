import datetime
import aiohttp
import json
import discord_slash
import os
import asyncio
import random
import discord
import subprocess
from discord import Webhook, AsyncWebhookAdapter
from base_logger import logger
from config import BRO_NEWS_WEBHOOK_URL, OUTPUT_WORLD_FILE
from constants import ERROR_GIF
from pathlib import Path


async def get_advice(message_channel):
    """Function used to get a random advice from the internet"""
    try:
        session = aiohttp.ClientSession()
        async with session.get("https://api.adviceslip.com/advice") as resp:
            data = await resp.read()
            json_response = json.loads(data)
        await session.close()
        embed = discord.Embed(title=json_response['slip']['advice'])
        await embed_send(message_channel, embed)

    except Exception as e:
        logger.exception(e)
        await send_error_message(message_channel)


async def get_fact(message_channel):
    """Function used to get a random fact from the internet"""
    try:
        session = aiohttp.ClientSession()
        async with session.get("https://useless-facts.sameerkumar.website/api") as resp:
            data = await resp.read()
            json_response = json.loads(data)
        await session.close()
        embed = discord.Embed(title=json_response['data'])
        await embed_send(message_channel, embed)
    except Exception as e:
        logger.exception(e)
        await send_error_message(message_channel)


async def get_insult(message_channel):
    """Function used to get a random insult from the internet"""
    try:
        session = aiohttp.ClientSession()
        async with session.get("https://insult.mattbas.org/api/insult.json") as resp:
            data = await resp.read()
            json_response = json.loads(data)
        await session.close()
        embed = discord.Embed(title=json_response['insult'])
        await embed_send(message_channel, embed)

    except Exception as e:
        logger.exception(e)
        await send_error_message(message_channel)


async def get_xkcd(message_channel):
    """Function used to get a random xkcd comic"""
    comic_number = random.randint(1, 2310)  # comic number range TODO:get dynamically
    logger.debug(comic_number)
    try:
        session = aiohttp.ClientSession()
        url = "https://xkcd.com/{}/info.0.json".format(comic_number)
        async with session.get(url) as resp:
            data = await resp.read()
            json_response = json.loads(data)
        await session.close()
        embed = discord.Embed(title=json_response['title'])
        embed.set_image(url=json_response['img'])
        await embed_send(message_channel, embed)

    except Exception as e:
        logger.exception(e)
        await send_error_message(message_channel)


async def get_news(message_channel):
    """Function used to get a latest news"""
    logger.debug("news")
    try:
        session = aiohttp.ClientSession()

        # read Bot Token from token file in secrets folder
        if os.environ.get('RUNNING_DOCKER_COMPOSE'):
            key_file_path = os.environ.get("NEWS_API")
            with open(key_file_path, 'r') as key_file:
                news_api_key = key_file.read().strip()
        else:
            news_api_key = os.environ.get("NEWS_API")

        news_url = "https://newsapi.org/v2/top-headlines?sources=bbc-news&language=en&apiKey={}".format(news_api_key)
        async with session.get(news_url) as resp:
            data = await resp.read()
            json_response = json.loads(data)
        await session.close()

        embed_list = []
        news_message = ""
        for index in range(7):
            embed = discord.Embed(title=json_response['articles'][index]['title'],
                                  description=json_response['articles'][index]['description'],
                                  url=json_response['articles'][index]['url'],
                                  colour=discord.Color.darker_grey())
            embed.set_thumbnail(url=json_response['articles'][index]['urlToImage'])
            embed_list.append(embed)
            news_message += "{}. {}\n".format(index + 1, json_response['articles'][index]['title'])

        if isinstance(message_channel, discord.ext.commands.context.Context):
            """when triggered through prefix command"""
            embed = discord.Embed(title="TOP HEADLINES",
                                  description=news_message)
            await embed_send(message_channel, embed)
            # await message_channel.send(content="```TOP HEADLINES:\n{}```".format(news_message))
        elif isinstance(message_channel, discord.channel.TextChannel):
            """when triggered automatically at a particular time, example daily news"""
            async with aiohttp.ClientSession() as session:
                webhook = Webhook.from_url(
                    BRO_NEWS_WEBHOOK_URL,
                    adapter=AsyncWebhookAdapter(session))

                await webhook.send(content="```TOP HEADLINES```", embeds=embed_list)
        elif isinstance(message_channel, discord_slash.context.SlashContext):
            """when triggered through slash command"""
            await message_channel.send(content="```TOP HEADLINES```", embeds=embed_list)
        else:
            logger.error("invalid ctx type: {}".format(type(message_channel)))
            await send_error_message(message_channel)
    except Exception as e:
        logger.exception(e)
        await send_error_message(message_channel)


async def sleep_until_time(trigger_time):
    """Function used to get sleep until a particular trigger time"""
    # trigger_time needs be in hh:mm 24-hr format
    # ex: 12:30
    hour = int(trigger_time.split(':')[0])
    minute = int(trigger_time.split(':')[1])
    t = datetime.datetime.today()
    future = datetime.datetime(t.year, t.month, t.day, hour, minute)
    if t.hour >= hour:
        future += datetime.timedelta(days=1)
    logger.debug("Sleeping for {} seconds...".format((future - t).seconds))
    await asyncio.sleep((future - t).seconds)


async def get_public_url():
    """Function used to get a ngrok public url of host"""
    session = aiohttp.ClientSession()
    url = "http://localhost:4040/api/tunnels/"
    async with session.get(url) as resp:
        data = await resp.read()
        data_json = json.loads(data)
    await session.close()

    msg = ""
    for i in data_json['tunnels']:
        msg = msg + i['public_url'] + '\n'
    return msg


async def embed_send(ctx, embed, edit_flag=0):
    """Function used to get a send embeds based on the type of message object"""
    if isinstance(ctx, discord.ext.commands.context.Context) or isinstance(ctx, discord.message.Message) or isinstance(ctx, discord.channel.TextChannel):
        if edit_flag:
            await ctx.edit(content="", embed=embed)
        else:
            await ctx.send(embed=embed)
    elif isinstance(ctx, discord_slash.context.SlashContext):
        await ctx.send(embeds=[embed])
    else:
        logger.error("invalid ctx type: {}".format(type(ctx)))
        await ctx.send(ERROR_GIF)


async def get_intro(ctx):
    """Sends out a bot introduction message"""
    embed = discord.Embed(title="Say Bro and I\'ll bro you back")
    embed.set_image(url="https://media.giphy.com/media/l0K45p4XQTVmyClMs/giphy.gif")
    await embed_send(ctx, embed)


async def send_error_message(ctx, title='Sorry, try again later'):
    """Function used to send an error message"""
    embed = discord.Embed(title=title,
                          color=discord.Color.red())
    embed.set_image(url=ERROR_GIF)
    await embed_send(ctx, embed)


async def get_terraria_url():
    """Function used to get a terraria server public url"""
    session = aiohttp.ClientSession()
    url = "http://localhost:4040/api/tunnels/"
    async with session.get(url) as resp:
        data = await resp.read()
        data_json = json.loads(data)
    await session.close()

    msg = ""
    for i in data_json['tunnels']:
        if i['name'] == 'terraria':
            msg = i['public_url']
    return msg


async def backup_world_file(ctx):
    try:
        embed = discord.Embed(title="Generating file...Please wait...")
        await embed_send(ctx, embed)
        ret = subprocess.call(['sh', '/home/pi/misc/world_file_generate.sh'])
        if ret == 0:
            my_file = Path(OUTPUT_WORLD_FILE)
            if my_file.is_file():
                await ctx.send(file=discord.File(OUTPUT_WORLD_FILE))
            else:
                embed = discord.Embed(title="Failed, try again later...")
                await embed_send(ctx, embed)
                subprocess.call(['sh', '/home/pi/misc/world_file_remove.sh'])
        else:
            embed = discord.Embed(title="Zip process failed, try again later...")
            await embed_send(ctx, embed)
    except Exception as e:
        logger.exception(e)
