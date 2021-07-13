import datetime
import aiohttp
import json
import discord_slash
import uinput
import os
import asyncio
import random
import discord
from discord import Webhook, AsyncWebhookAdapter

from base_logger import logger
from config import BRO_NEWS_WEBHOOK_URL


async def get_advice(message_channel):
    logger.debug("advice")
    wait_message = await message_channel.send("Let me think...")

    try:
        session = aiohttp.ClientSession()
        async with session.get("https://api.adviceslip.com/advice") as resp:
            data = await resp.read()
            json_response = json.loads(data)
        await session.close()
        await wait_message.edit(content='*\"{}\"*'.format(json_response['slip']['advice']))
    except Exception as e:
        logger.exception(e)
        await message_channel.send('Sorry can\'t think of anything')


async def get_fact(message_channel):
    logger.debug("advice")
    wait_message = await message_channel.send("One interesting fact coming right up...")

    try:
        session = aiohttp.ClientSession()
        async with session.get("https://useless-facts.sameerkumar.website/api") as resp:
            data = await resp.read()
            json_response = json.loads(data)
        await session.close()
        await wait_message.edit(content='*\"{}\"*'.format(json_response['data']))
    except Exception as e:
        logger.exception(e)
        await message_channel.send('Sorry can\'t think of anything')


async def get_insult(message_channel):
    logger.debug("advice")
    wait_message = await message_channel.send("Buckle up Butter cup...")

    try:
        session = aiohttp.ClientSession()
        async with session.get("https://insult.mattbas.org/api/insult.json") as resp:
            data = await resp.read()
            json_response = json.loads(data)
        await session.close()
        await wait_message.edit(content='*\"{}\"*'.format(json_response['insult']))
    except Exception as e:
        logger.exception(e)
        await message_channel.send('No insult for you.')


async def get_xkcd(message_channel):
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
        await message_channel.send('No comic for you')


class VirtualKeyboard:
    def __init__(self):
        self.device = uinput.Device((uinput.KEY_A,
                                     uinput.KEY_B,
                                     uinput.KEY_C,
                                     uinput.KEY_D,
                                     uinput.KEY_E,
                                     uinput.KEY_F,
                                     uinput.KEY_G,
                                     uinput.KEY_H,
                                     uinput.KEY_I,
                                     uinput.KEY_J,
                                     uinput.KEY_K,
                                     uinput.KEY_L,
                                     uinput.KEY_M,
                                     uinput.KEY_N,
                                     uinput.KEY_O,
                                     uinput.KEY_P,
                                     uinput.KEY_Q,
                                     uinput.KEY_R,
                                     uinput.KEY_S,
                                     uinput.KEY_T,
                                     uinput.KEY_U,
                                     uinput.KEY_V,
                                     uinput.KEY_W,
                                     uinput.KEY_X,
                                     uinput.KEY_Y,
                                     uinput.KEY_Z,
                                     uinput.KEY_ENTER,
                                     uinput.KEY_UP,
                                     uinput.KEY_DOWN,
                                     uinput.KEY_LEFT,
                                     uinput.KEY_RIGHT,
                                     uinput.KEY_F2,
                                     uinput.KEY_F4,
                                     ))

    async def send_keyboard_input(self, string, press_enter_after_string=False):
        try:
            string = string.upper()
            logger.debug(string)
            # Special keys
            if string in ["UP", "DOWN", "LEFT", "RIGHT"]:
                key = getattr(uinput, "KEY_" + string)
                self.device.emit(key, 1)
                await asyncio.sleep(0.4)
                self.device.emit(key, 0)
                await asyncio.sleep(0.4)
            else:
                for i in string:
                    logger.debug("Clicking {}".format(i))
                    key = getattr(uinput, "KEY_" + i)
                    self.device.emit(key, 1)
                    await asyncio.sleep(0.4)
                    self.device.emit(key, 0)
                    await asyncio.sleep(0.4)

            if press_enter_after_string:
                self.device.emit(uinput.KEY_ENTER, 1)
                await asyncio.sleep(0.4)
                self.device.emit(uinput.KEY_ENTER, 0)
                await asyncio.sleep(0.4)

        except Exception as e:
            logger.exception(e)

    async def send_keyboard_shortcut(self, list_of_keys):
        try:
            logger.debug(list_of_keys)
            for i in list_of_keys:
                logger.debug("Holding {}".format(i))
                key = getattr(uinput, "KEY_" + i.upper())
                self.device.emit(key, 1)
                await asyncio.sleep(0.4)

            for i in list_of_keys:
                logger.debug("Releasing {}".format(i))
                key = getattr(uinput, "KEY_" + i)
                self.device.emit(key, 0)
                await asyncio.sleep(0.4)

        except Exception as e:
            logger.exception(e)


def take_screenshot(filename="test.png"):
    logger.debug("taking screenshot")
    os.system("raspi2png -p {}".format(filename))
    return 0


async def get_news(message_channel):
    logger.debug("news")
    # wait_message = await message_channel.send("Bringing you the latest BREAKING NEWS!")

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
        embed = ""
        news_message = ""
        for index in range(7):
            embed = discord.Embed(title=json_response['articles'][index]['title'],
                                  description=json_response['articles'][index]['description'],
                                  url=json_response['articles'][index]['url'],
                                  colour=discord.Color.darker_grey())
            embed.set_thumbnail(url=json_response['articles'][index]['urlToImage'])
            embed_list.append(embed)
            news_message += "{}. {}\n".format(index + 1, json_response['articles'][index]['title'])

        # await wait_message.edit(content="```TOP HEADLINES:\n```".format(news_message))
        if isinstance(message_channel, discord.ext.commands.context.Context) or isinstance(message_channel, discord.channel.TextChannel):
            # await message_channel.send(content="```TOP HEADLINES:\n{}```".format(news_message))
            async with aiohttp.ClientSession() as session:
                webhook = Webhook.from_url(
                    BRO_NEWS_WEBHOOK_URL,
                    adapter=AsyncWebhookAdapter(session))

                await webhook.send(content="```TOP HEADLINES```", embeds=embed_list)
        elif isinstance(message_channel, discord_slash.context.SlashContext):
            await message_channel.send(content="```TOP HEADLINES```", embeds=embed_list)
        else:
            logger.error("invalid ctx type: {}".format(type(message_channel)))
            await message_channel.send("ZZZzzzz")
    except Exception as e:
        logger.exception(e)
        await message_channel.send("No news for you.")


async def sleep_until_time(trigger_time):
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


# checks ctx type and sends embed accordingly
async def embed_send(ctx, embed):
    if isinstance(ctx, discord.ext.commands.context.Context):
        await ctx.send(embed=embed)
    elif isinstance(ctx, discord_slash.context.SlashContext):
        await ctx.send(embeds=[embed])
    else:
        logger.error("invalid ctx type: {}".format(type(ctx)))
        await ctx.send("ZZZzzzz")
