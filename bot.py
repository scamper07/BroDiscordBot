import time

import discord
from discord.ext import commands, tasks
from collections import Counter
from pyKey import press
import random
import aiohttp
import json
import asyncio
import logging
from logging.handlers import TimedRotatingFileHandler
import html
import datetime
from cogs.general import General
from cogs.games.quiz import Quiz


''' Initialize logging '''
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = TimedRotatingFileHandler(filename='discord.log', when="midnight", backupCount=5)
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s', datefmt='%d-%b-%y %H:%M:%S'))
logger.addHandler(handler)

''' read Bot Token from file '''
with open('token') as f:
    TOKEN = f.read()

''' -------Globals variables------- '''
COMMAND_PREFIX = '.'

# Channel info
ALPHA_MALES_GOODIE_BAG_CHANNEL = 573003537609654283
GENERAL_CHANNEL_ID = 698571675754692752
TEST_CHANNEL_ID = 207481917975560192
TEST2_CHANNEL_ID = 573003537609654283


# Game globals
GAME_MODE = False

# Twitch globals
TWITCH_NOT_STREAMING = 0
TWITCH_STARTED_STREAMING = 1
TWITCH_STILL_STREAMING = 2
live_status_dict = {}

# TODO: add command to insert user
streamers = ["swatplayskreede",
             "code_name_47_",
             "bamboozle_heck",
             "kbharathi",
             "supersonic_mk"
             ]  # Twitch user names

for player in streamers:
    live_status_dict.update({player: TWITCH_NOT_STREAMING})

# Misc globals
MEMBER_UPDATE_COUNT = 0
stats_brief = 'Shows random stats about server, {}stats <username> for user'.format(COMMAND_PREFIX)

# Messages/Quotes
WAR_CRY_LIST = ['LET\'S GO BROS!',
                'IT\'S OUR TIME TO SHINE BROS!',
                'Leeeeroy Jenkins!',
                'IT\'S TIME TO KICK ASS BROS!',
                'Carpe diem. Seize the day, bros',
                'Requiescat in pace bros',
                'May the Force be with you bros',
                'Keep your friends close, but your enemies closer bros',
                'Hasta la vista, bros',
                'Fasten your seatbelts. It\'s going to be a bumpy ride bros',
                'To infinity and beyond bros!',
                'The Force will be with you. Always.',
                'The time to fight is now bros.'
                ]


''' ----Bot client object initialization---- '''
client = commands.Bot(command_prefix=COMMAND_PREFIX)


''' -------Event functionality------- '''

@client.event
async def on_ready():
    activity = discord.Activity(name='.help', type=discord.ActivityType.listening)
    # activity = discord.Activity(name='Call of Duty\N{REGISTERED SIGN}: Modern Warfare\N{REGISTERED SIGN}',
    # type=discord.ActivityType.playing)
    await client.change_presence(activity=activity)
    logger.debug("Bot is online!")
    # Register all the cogs when the bot is ready.
    register_cogs(client)

@client.event
async def on_message(message):
    global WAR_CRY_LIST
    if message.author == client.user:
        return

    full_message = message.content.lower()  # has full message in lower case
    full_message_list = full_message.split()  # message is split on spaces

    if 'bro' in full_message_list:
        logging.debug("Sending Bro message")
        await message.channel.send("Bro", tts=False)

    if 'hello' in full_message_list or 'hi' in full_message_list:
        logger.debug("Sending hello message")
        await message.channel.send("Hello {} bro".format(message.author.mention))

    if 'bye' in full_message_list:
        logger.debug("Sending bye message")
        await message.channel.send("Bye Bye {} bro".format(message.author.mention))

    if 'good morning' in full_message or 'gm' in full_message_list:
        logger.debug("Sending gm message")
        await message.channel.send("Good morning bros")

    if 'good night' in full_message or 'gn' in full_message_list:
        logger.debug("Sending gn message")
        await message.channel.send("Good night bros")

    if 'good game' in full_message or 'gg' in full_message_list:
        logger.debug("Sending gn message")
        await message.channel.send("gg bros")

    if "i\'m online" in full_message or "im online" in full_message:
        logger.debug("Sending online message")
        await message.channel.send("I'm online too bro")

    if "tictactoe" in full_message:
        await message.channel.send("Kai is trying to build this. Coming soon..\n P.S : I hope so - Pavan")
        #await ttt.start_game(message)

    '''
    if 'stream' in full_message:  # or 'play' in full_message and '-play' not in full_message:
        logger.debug("Sending stream/play message")
        await message.channel.send("***STREAM STREAM STREAM!***")
        await message.channel.send(random.choice(WAR_CRY_LIST), tts=True)
    '''

    global GAME_MODE
    if GAME_MODE:
        try:
            if message.content[:2].lower() == "up" and int(message.content[-1]):
                for i in range(int(message.content[-1])):
                    press('UP', 0.2)
            elif message.content[:4].lower() == "down" and int(message.content[-1]):
                for i in range(int(message.content[-1])):
                    press('DOWN', 0.2)
            elif message.content[:4].lower() == "left" and int(message.content[-1]):
                for i in range(int(message.content[-1])):
                    press('LEFT', 0.2)
            elif message.content[:5].lower() == "right" and int(message.content[-1]):
                for i in range(int(message.content[-1])):
                    press('RIGHT', 0.2)
            elif message.content.lower() == "a":
                press('z', 0.1)
            elif message.content.lower() == "b":
                press('x', 0.1)
            elif message.content.lower() == "l":
                press('a', 0.1)
            elif message.content.lower() == "r":
                press('s', 0.1)
            elif message.content.lower() == "select":
                press('BKSP', 0.1)
            elif message.content.lower() == "start":
                press('ENTER', 0.1)
            else:
                pass
        except ValueError as vale:
            logger.exception(vale)
            await message.channel.send("```Empty/Invalid entry```")
        except Exception as e:
            logger.exception(e)

    await client.process_commands(message)


'''
@client.event
async def on_member_update(before, after):
    global MEMBER_UPDATE_COUNT
    if MEMBER_UPDATE_COUNT == 0:
        if str(after.display_name) == "darshan_ar":
            if str(before.status) == "offline" and str(after.status) == "online":
                logger.debug("JOIN THE VOICE CHANNEL {}!".format(after.display_name))
                channel = client.get_channel(GENERAL_CHANNEL_ID)
                MEMBER_UPDATE_COUNT += 1
                await channel.send("JOIN THE VOICE CHANNEL {}!".format(after.mention))

    if MEMBER_UPDATE_COUNT == 1:
        MEMBER_UPDATE_COUNT = 0
'''

''' -------Command functionality------- '''

@client.command(brief=stats_brief, description='Shows stats for server or members')
async def stats(ctx, user: discord.Member = None):
    wait_message = await ctx.send("Processing... Please wait. This might take sometime")
    async with ctx.typing():
        if not user:
            embed = discord.Embed(
                title="Stats",
                description="Showing random stats for this server",
                colour=discord.Color.blue()
            )
            embed.set_footer(text="Hope that was helpful, bye!")
            embed.set_author(name="Bro Bot", icon_url=client.user.avatar_url)
            embed.set_thumbnail(url=ctx.guild.icon_url)

            server = ctx.message.author.guild
            server_name = server.name
            server_owner = server.owner.mention
            server_create_date = server.created_at.__format__('%d/%B/%Y')
            server_member_count = server.member_count
            logger.debug("*****************************")
            logger.debug("Server name: {}\nserver owner: {}\nserver created at: {}\nTotal number of members: {}".format(
                server_name,
                server_owner,
                server_create_date,
                server_member_count)
            )
            embed.add_field(name="Server Name", value=server_name, inline=False)
            embed.add_field(name="Server Owner", value=server_owner, inline=True)
            embed.add_field(name="Server Create Date", value=server_create_date, inline=True)
            embed.add_field(name="Total Members", value=server_member_count, inline=True)

            # channel = client.get_channel(GENERAL_CHANNEL_ID)
            # messages = await channel.history(limit=None).flatten()
            messages = await ctx.channel.history(limit=None).flatten()
            logger.debug("Total messages: {}".format(len(messages)))
            embed.add_field(name="Total messages", value=str(len(messages)), inline=False)
            authors_count = Counter()
            word_count = Counter()
            message_list = list()
            bro_in_message_count = 0
            for message in messages:
                if "bro" in str(message.content).lower():
                    bro_in_message_count += 1
                authors_count.update({message.author.name: 1})
                message_list += str(message.content).split()
            word_count.update(message_list)

            top = authors_count.most_common(1)
            logger.debug("Most talkative bro: {} talked {} times".format(top[0][0], top[0][1]))
            value = str(top[0][0] if ctx.guild.get_member_named(top[0][0]) is None else ctx.guild.get_member_named(
                top[0][0]).mention) + " (" + str(top[0][1]) + " messages)"
            logger.debug(value)
            embed.add_field(name="Most Talkative Bro", value=value, inline=False)

            low = min(authors_count, key=authors_count.get)
            logger.debug("Least talkative bro: {} talked {} time(s)".format(low, authors_count[low]))
            value = str(low if ctx.guild.get_member_named(low) is None else ctx.guild.get_member_named(
                low).mention) + " (" + str(authors_count[low]) + " messages)"
            embed.add_field(name="Least Talkative Bro", value=value, inline=True)

            top_authors = ""
            if len(authors_count) >= 5:
                logger.debug("Top 5 talkative Bros")
                for author, message_count in authors_count.most_common(5):
                    logger.debug("{}: {} times".format(author, message_count))
                    top_authors += str(
                        author if ctx.guild.get_member_named(author) is None else ctx.guild.get_member_named(
                            author).mention) + " (" + str(message_count) + " messages) \n"

            embed.add_field(name="Top 5 Talkative Bros", value=top_authors, inline=False)

            top_string = ""
            if len(word_count) >= 5:
                logger.debug("Top five words used here are:")
                for word, count in word_count.most_common(5):
                    logger.debug("{}: {} times".format(word, count))
                    top_string += str(word) + " (" + str(count) + " times) \n"

            embed.add_field(name="Top 5 words used here", value=top_string, inline=False)

            logger.debug("Bro was mentioned {} times!".format(bro_in_message_count))
            embed.add_field(name="Bro Count", value=str(bro_in_message_count), inline=False)

            logger.debug("*****************************")
        else:
            embed = discord.Embed(
                title="Stats",
                description="Showing random stats for user",
                colour=discord.Color.purple()
            )
            embed.set_footer(text="Hope that was helpful, bye!")
            embed.set_author(name="Bro Bot", icon_url=client.user.avatar_url)
            embed.set_thumbnail(url=user.avatar_url)

            logger.debug("*****************************")
            logger.debug("user name: {}".format(user.mention))
            logger.debug("user join date: {}".format(user.joined_at.__format__('%d/%B/%Y @%H:%M:%S')))
            embed.add_field(name="User Name", value=user.mention, inline=False)
            embed.add_field(name="User Join Date", value=user.joined_at.__format__('%d/%B/%Y'), inline=False)

            messages = await ctx.channel.history(limit=None).flatten()
            message_list = list()
            word_count = Counter()
            for message in messages:
                if user == message.author:
                    message_list += str(message.content).split()

            word_count.update(message_list)
            top_string = ""
            if len(word_count) >= 5:
                logger.debug("Top five words used by {}:".format(user.display_name))
                top_name = "Top 5 words used by {} in this server:".format(user.display_name)
                for word, count in word_count.most_common(5):
                    logger.debug("{}: {} times".format(word, count))
                    top_string += str(word) + "(" + str(count) + ") \n"

                embed.add_field(name=top_name, value=top_string, inline=False)
            logger.debug("*****************************")

    await wait_message.delete()
    await ctx.send(embed=embed)

@stats.error
async def info_error(ctx, error):
    if isinstance(error, commands.BadArgument):
        await ctx.send('```Member not found...```')
        await ctx.send(
            '```Command usage:\n {}stats  : for server stats\n {}stats <username> : for user stats```'.format(
                COMMAND_PREFIX, COMMAND_PREFIX))

@client.command(brief='Allows you to play a GameBoy game with friends')
async def game(ctx, arg=None):
    global GAME_MODE
    if not arg:
        await ctx.send('```Usage:\n'
                       '{}game on : to activate game mode\n'
                       '{}game off : to deactivate game mode\n```'.format(COMMAND_PREFIX, COMMAND_PREFIX))
        return

    if arg.lower() == "on":
        GAME_MODE = True
        await ctx.send('```GAME MODE ACTIVATED!```')
        await ctx.send(
            '```Available Keys:\n'
            '   up <number>: to move up\n'
            '   down <number>: to move down\n'
            '   left <number>: to move left\n'
            '   right <number>: to move right\n'
            '   a : to press A\n'
            '   b : to press B\n'
            '   select: to press Select\n'
            '   start: to press Start\n```'.format(COMMAND_PREFIX))
    elif arg.lower() == "off":
        GAME_MODE = False
        await ctx.send('```GAME MODE DEACTIVATED, BYE!```')
    else:
        await ctx.send('```Invalid entry```')
        await ctx.send('```Usage:\n'
                       '{}game on : to activate game mode\n'
                       '{}game off : to deactivate game mode\n```'.format(COMMAND_PREFIX, COMMAND_PREFIX))

@client.command(brief='Turns on my Master\'s PC')
async def switchon(ctx):
    logger.debug("Powering on PC")
    if ctx.message.author.name == "Diego Delavega":
        session = aiohttp.ClientSession()
        data = {"action": "on"}
        ''' read API endpoint from file '''
        with open('api') as f:
            pc_api = f.read().strip()
        res = await session.post(pc_api, data=json.dumps(data), headers={'content-type': 'application/json'})
        await session.close()
        await ctx.send('```Done```')
    else:
        await ctx.send('```Only my master can use this command.```')

@client.command(brief='', hidden=True)
async def post(ctx, *args):
    if args[0] == 'gb':
        channel = client.get_channel(TEST2_CHANNEL_ID)
        message = ' '.join(args[1:])
    else:
        channel = client.get_channel(GENERAL_CHANNEL_ID)
        message = ' '.join(args)
    logger.debug("{} {}".format(len(args), message))
    await channel.send(message)

@client.command(brief='Bro gives life advices!')
async def advice(ctx):
    await get_advice(ctx)


''' ------Background tasks------ '''

@tasks.loop(minutes=5)
async def twitch_live_status():
    await client.wait_until_ready()
    with open('twitch_client_id') as f:
        client_id = f.read().strip()

    with open('twitch_app_access') as f:
        app_access_token = f.read().strip()

    url = "https://api.twitch.tv/helix/streams?user_login="  # Twitch get streams api
    games_url = "https://api.twitch.tv/helix/games?id="  # Twitch get game api
    headers = {'Client-ID': client_id,
               'Authorization': 'Bearer ' + app_access_token,
               }

    # Total 550-600 bytes of data fetched
    global live_status_dict, streamers
    logger.debug(live_status_dict)

    session = aiohttp.ClientSession()
    try:
        for streamer in streamers:
            twitch_url = url + streamer

            async with session.get(twitch_url, headers=headers) as resp:
                data = await resp.read()
                json_response = json.loads(data)
                logger.debug(json_response)

                # if data not empty, user is streaming
                if json_response['data']:
                    if live_status_dict[streamer] == TWITCH_NOT_STREAMING:
                        game_id = json_response['data'][0]['game_id']

                        # get info on game the user is playing
                        async with session.get(games_url + game_id, headers=headers) as resp:
                            game_data = await resp.read()
                            game_response = json.loads(game_data)
                            logger.debug(game_response)  # size: 140 bytes
                            logger.debug("https://www.twitch.tv/{}".format(json_response['data'][0]['user_name']))

                            channel = client.get_channel(GENERAL_CHANNEL_ID)
                            await channel.send(
                                "**{} is live on Twitch playing {}!**".format(json_response['data'][0]['user_name'],
                                                                              game_response['data'][0]['name']))
                            await channel.send(
                                "https://www.twitch.tv/{}".format(json_response['data'][0]['user_name']))
                        live_status_dict[streamer] = TWITCH_STARTED_STREAMING
                    else:
                        logger.debug("{} is still live. not sending".format(streamer))
                        live_status_dict[streamer] = TWITCH_STILL_STREAMING
                else:
                    logger.debug("{} is not live".format(streamer))
                    if live_status_dict[streamer] == TWITCH_STARTED_STREAMING or live_status_dict[streamer] == TWITCH_STILL_STREAMING:
                        await channel.send("{}\'s stream has ended.".format(streamer))
                        live_status_dict[streamer] = TWITCH_NOT_STREAMING
            await asyncio.sleep(2)
    except Exception as e:
        logger.exception(e)
    finally:
        await session.close()

@twitch_live_status.before_loop
async def before():
    await client.wait_until_ready()
    print("Finished waiting")

@tasks.loop(hours=24.0)
async def daily_advices():
    message_channel = client.get_channel(ALPHA_MALES_GOODIE_BAG_CHANNEL)
    await get_advice(message_channel)

@daily_advices.before_loop
async def before():
    await client.wait_until_ready()
    print("Finished waiting")


''' ------utils------ '''

async def get_advice(message_channel):
    logger.debug("advice")
    wait_message = await message_channel.send("Let me think...")

    try:
        session = aiohttp.ClientSession()
        async with session.get("https://api.adviceslip.com/advice") as resp:
            data = await resp.read()
        json_response = json.loads(data)
        await session.close()
        await wait_message.delete()
        await message_channel.send('*\"{}\"*'.format(json_response['slip']['advice']))
    except Exception as e:
        logger.exception(e)
        await message_channel.send('Sorry can\'t think of anything')

def register_cogs(bot):
    cog_list = [General(bot), Quiz(bot)]
    for cog in cog_list:
        bot.add_cog(cog)

twitch_live_status.start()
daily_advices.start()


client.run(TOKEN)
