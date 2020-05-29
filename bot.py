import discord
from discord.ext import commands

from collections import Counter
from pyKey import press

import random
import aiohttp
import json
import asyncio

''' read Bot Token from file '''
with open('token') as f:
    TOKEN = f.read()

''' -------Globals variables------- '''
COMMAND_PREFIX = '.'
GENERAL_CHANNEL_ID = 698571675754692752
TEST_CHANNEL_ID = 207481917975560192
MEMBER_UPDATE_COUNT = 0
GAME_MODE = False
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


    print("Bot is online!")


@client.event
async def on_message(message):
    global WAR_CRY_LIST
    if message.author == client.user:
        return
    full_message = message.content.lower()
    if 'bro' in full_message:
        print("Sending Bro message")
        await message.channel.send("Bro", tts=False)

    if 'hello' in full_message or 'hi ' in full_message:
        print("Sending hello message")
        await message.channel.send("Hello {} Bro".format(message.author.mention))

    if 'bye' in full_message:
        print("Sending bye message")
        await message.channel.send("Bye Bye {} Bro".format(message.author.mention))

    if "good morning" in full_message:
        print("Sending gm message")
        await message.channel.send("Good morning Bros")

    if "good night" in full_message:
        print("Sending gn message")
        await message.channel.send("Good night Bros")

    if "i\'m online" in full_message or "im online" in full_message:
        print("Sending online message")
        await message.channel.send("I'm online too Bro")

    '''
    if 'stream' in full_message:  # or 'play' in full_message and '-play' not in full_message:
        print("Sending stream/play message")
        await message.channel.send("***STREAM STREAM STREAM!***")
        await message.channel.send(random.choice(WAR_CRY_LIST), tts=True)
    '''

    if 'stop bro' in full_message or 'shut up bro' in full_message:
        print("Sending sorry message")
        await message.channel.send("Sorry bro *cries in the corner*")

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
            print(vale)
            await message.channel.send("```Empty/Invalid entry```")
        except Exception as e:
            print(e)
    await client.process_commands(message)

'''
@client.event
async def on_member_update(before, after):
    global MEMBER_UPDATE_COUNT
    if MEMBER_UPDATE_COUNT == 0:
        if str(after.display_name) == "darshan_ar":
            if str(before.status) == "offline" and str(after.status) == "online":
                print("JOIN THE VOICE CHANNEL {}!".format(after.display_name))
                channel = client.get_channel(GENERAL_CHANNEL_ID)
                MEMBER_UPDATE_COUNT += 1
                await channel.send("JOIN THE VOICE CHANNEL {}!".format(after.mention))

    if MEMBER_UPDATE_COUNT == 1:
        MEMBER_UPDATE_COUNT = 0
'''

''' -------Command functionality------- '''


@client.command(brief='Shows brief introduction of Bro Bot')
async def intro(ctx):
    print("Sending intro message")
    await ctx.send('```Say Bro and I\'ll bro you back```')


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
            print("*****************************")
            print("Server name: {}\nserver owner: {}\nserver created at: {}\nTotal number of members: {}".format(server_name,
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
            print("Most talkative bro: {} talked {} times".format(top[0][0], top[0][1]))
            value = str(top[0][0] if ctx.guild.get_member_named(top[0][0]) is None else ctx.guild.get_member_named(top[0][0]).mention) + " (" + str(top[0][1]) + " messages)"
            print(value)
            embed.add_field(name="Most Talkative Bro", value=value, inline=False)

            low = min(authors_count, key=authors_count.get)
            print("Least talkative bro: {} talked {} time(s)".format(low, authors_count[low]))
            value = str(low if ctx.guild.get_member_named(low) is None else ctx.guild.get_member_named(low).mention) + " (" + str(authors_count[low]) + " messages)"
            embed.add_field(name="Least Talkative Bro", value=value, inline=True)

            top_authors = ""
            if len(authors_count) >= 5:
                print("Top 5 talkative Bros")
                for author, message_count in authors_count.most_common(5):
                    print("{}: {} times".format(author, message_count))
                    top_authors += str(author if ctx.guild.get_member_named(author) is None else ctx.guild.get_member_named(author).mention) + " (" + str(message_count) + " messages) \n"

            embed.add_field(name="Top 5 Talkative Bros", value=top_authors, inline=False)

            top_string = ""
            if len(word_count) >= 5:
                print("Top five words used here are:")
                for word, count in word_count.most_common(5):
                    print("{}: {} times".format(word, count))
                    top_string += str(word) + " (" + str(count) + " times) \n"

            embed.add_field(name="Top 5 words used here", value=top_string, inline=False)

            print("Bro was mentioned {} times!".format(bro_in_message_count))
            embed.add_field(name="Bro Count", value=str(bro_in_message_count), inline=False)

            print("*****************************")
        else:
            embed = discord.Embed(
                title="Stats",
                description="Showing random stats for user",
                colour=discord.Color.purple()
            )
            embed.set_footer(text="Hope that was helpful, bye!")
            embed.set_author(name="Bro Bot", icon_url=client.user.avatar_url)
            embed.set_thumbnail(url=user.avatar_url)

            print("*****************************")
            print("user name: {}".format(user.mention))
            print("user join date: {}".format(user.joined_at.__format__('%d/%B/%Y @%H:%M:%S')))
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
                print("Top five words used by {}:".format(user.display_name))
                top_name = "Top 5 words used by {} in this server:".format(user.display_name)
                for word, count in word_count.most_common(5):
                    print("{}: {} times".format(word, count))
                    top_string += str(word) + "(" + str(count) + ") \n"

                embed.add_field(name=top_name, value=top_string, inline=False)
            print("*****************************")

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
    print("Powering on PC")
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
    message = ' '.join(args)
    print("{} {}".format(len(args), message))
    channel = client.get_channel(GENERAL_CHANNEL_ID)
    await channel.send(message)


@client.command(brief='Bro gives life advices!')
async def advice(ctx):
    print("advice")
    wait_message = await ctx.send("Let me think...")
    async with ctx.typing():
        try:
            session = aiohttp.ClientSession()
            async with session.get("https://api.adviceslip.com/advice") as resp:
                data = await resp.read()
            json_response = json.loads(data)
            await session.close()
            await wait_message.delete()
            await ctx.send('*\"{}\"*'.format(json_response['slip']['advice']))
        except Exception as e:
            print(e)
            await ctx.send('Sorry can\'t think of anything')


@client.command(brief='Bro shares random facts!')
async def facts(ctx):
    print("facts")
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
            print(e)
            await ctx.send('Sorry can\'t think of anything')


@client.command(brief='Puts out random xkcd comic!')
async def xkcd(ctx):
    print("xkcd")
    wait_message = await ctx.send("Comic time...")
    comic_number = random.randint(1, 2310)  # comic number range TODO:get dynamically
    print(comic_number)
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
            print(e)
            await ctx.send('No xkcd for you')


''' ------Background tasks------ '''


async def twitch_live_status():
    await client.wait_until_ready()
    with open('twitch_client_id') as f:
        client_id = f.read().strip()

    with open('twitch_app_access') as f:
        app_access_token = f.read().strip()

    streamers = ["suhan525",
                 "bamboozle_heck",
                 "code_name_47_",
                 "charlesleclerc",
                 "drdisrespect",
                 ]  # Twitch user names

    url = "https://api.twitch.tv/helix/streams?user_login="    # Twitch get streams api
    games_url = "https://api.twitch.tv/helix/games?id="  # Twitch get game api
    headers = {'Client-ID': client_id,
               'Authorization': 'Bearer '+app_access_token,
               }
    data = ""
    game_data = ""
    # Total 550-600 bytes of data fetched
    live_status_dict = {}
    for streamer in streamers:
        live_status_dict.update({streamer: 0})

    print(live_status_dict)
    session = aiohttp.ClientSession()
    while True:
        for streamer in streamers:
            twitch_url = url+streamer
            try:
                async with session.get(twitch_url, headers=headers) as resp:
                    data = await resp.read()
                    json_response = json.loads(data)
                    print(json_response)

                    if json_response['data']:
                        if live_status_dict[streamer] == 0:
                            game_id = json_response['data'][0]['game_id']
                            async with session.get(games_url + game_id, headers=headers) as resp:
                                game_data = await resp.read()
                                game_response = json.loads(game_data)
                                print(game_response)  # size: 140 bytes
                                print("https://www.twitch.tv/{}".format(json_response['data'][0]['user_name']))

                                channel = client.get_channel(GENERAL_CHANNEL_ID)
                                await channel.send("**{} is live on Twitch playing {}!**".format(json_response['data'][0]['user_name'], game_response['data'][0]['name']))
                                await channel.send("https://www.twitch.tv/{}".format(json_response['data'][0]['user_name']))
                            live_status_dict[streamer] = 1
                        else:
                            print("still live. not sending")
                            live_status_dict[streamer] = 2
                    else:
                        print("not live")
                        if live_status_dict[streamer] == 1 or live_status_dict[streamer] == 2:
                            await channel.send("{}\'s stream has ended.".format(streamer))
                            live_status_dict[streamer] = 0
            except Exception as e:
                print(e)
                # await session.close()
            await asyncio.sleep(2)
        await asyncio.sleep(60)
    # await session.close()

client.loop.create_task(twitch_live_status())
client.run(TOKEN)
