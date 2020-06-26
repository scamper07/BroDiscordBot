import discord
from discord.ext import commands
from base_logger import logger
from config import COMMAND_PREFIX, WAR_CRY_LIST, MEMBER_UPDATE_COUNT
# from pyKey import press


class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        # Changes the bot's status
        activity = discord.Activity(name=f'{COMMAND_PREFIX}help', type=discord.ActivityType.listening)
        await self.bot.change_presence(activity=activity)
        logger.debug('Bot is online!')

    @commands.Cog.listener()
    async def on_message(self, message):
        logger.debug(message.content)
        if message.author == self.bot.user:
            return

        full_message = message.content.lower()  # has full message in lower case
        full_message_list = full_message.split()  # message is split on spaces

        if 'bro' in full_message_list:
            logger.debug("Sending Bro message")
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
            # await ttt.start_game(message)

        '''
        if 'stream' in full_message:  # or 'play' in full_message and '-play' not in full_message:
            logger.debug("Sending stream/play message")
            await message.channel.send("***STREAM STREAM STREAM!***")
            await message.channel.send(random.choice(WAR_CRY_LIST), tts=True)
        '''
        '''
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
        '''
        # await self.bot.process_commands(message)

    '''
    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        if MEMBER_UPDATE_COUNT == 0:
            if str(after.display_name) == "darshan_ar":
                if str(before.status) == "offline" and str(after.status) == "online":
                    logger.debug("JOIN THE VOICE CHANNEL {}!".format(after.display_name))
                    channel = bot.get_channel(GENERAL_CHANNEL_ID)
                    MEMBER_UPDATE_COUNT += 1
                    await channel.send("JOIN THE VOICE CHANNEL {}!".format(after.mention))

        if MEMBER_UPDATE_COUNT == 1:
            MEMBER_UPDATE_COUNT = 0
    '''


def setup(bot):
    bot.add_cog(Events(bot))
