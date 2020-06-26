import asyncio
import os

import discord
from discord.ext import commands
from config import COMMAND_PREFIX, GAMEBOY_TEST_CHANNEL_ID
from base_logger import logger
from utils import VirtualKeyboard, take_screenshot


class Gameboy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.game_mode = False
        self.keyboard = VirtualKeyboard()

    @commands.command(brief='Play a 1 fps Pokemon GameBoy game with friends')
    async def game(self, ctx, arg=None):
        if not arg:
            await ctx.send('```Usage:\n'
                           '{}game on : to activate game mode\n'
                           '{}game off : to deactivate game mode\n'
                           '{}game savestate : to save game state\n'
                           '{}game loadstate : to load game state\n```'.format(COMMAND_PREFIX,
                                                                               COMMAND_PREFIX,
                                                                               COMMAND_PREFIX,
                                                                               COMMAND_PREFIX))
            return

        if arg.lower() == "on":
            if not self.game_mode:
                async with ctx.typing():
                    await ctx.send("Starting game. Please wait. This might take upto a minute")
                    self.game_mode = True
                    logger.debug("Starting game")
                    await self.keyboard.send_keyboard_input("emulationstation", True)
                    logger.debug("Starting game engine...")
                    await asyncio.sleep(30)
                    logger.debug("Done")
                    await asyncio.sleep(1)
                    logger.debug("Starting GBA...")
                    await self.keyboard.send_keyboard_input("z")
                    logger.debug("Done")
                    await asyncio.sleep(1)
                    logger.debug("Starting Pokemon...")
                    await self.keyboard.send_keyboard_input("z")
                    await asyncio.sleep(25)
                    logger.debug("Done")
                    await self.load_game_state()
                    await asyncio.sleep(1)
                    logger.debug("Taking screenshot...")
                    take_screenshot("gb.png")
                    logger.debug("Game ready to play")
                    await ctx.send("Game ready to play")
                    await asyncio.sleep(1)
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
                    # game_channel = self.bot.get_channel(GAMEBOY_TEST_CHANNEL_ID)
                    await ctx.send(file=discord.File('gb.png'))
                    logger.debug("Done")
            else:
                await ctx.send("Game is already running")
        elif arg.lower() == "off":
            if self.game_mode:
                async with ctx.typing():
                    await ctx.send('Stopping game safely. Please wait.')
                    await self.save_game_state()
                    logger.debug("Stopping game")
                    await self.keyboard.send_keyboard_shortcut(['M', 'C'])
                    logger.debug("Done")
                    await asyncio.sleep(10)
                    logger.debug("Stopping Retropie")
                    '''
                    send_keyboard_input("v")  # Menu
                    await asyncio.sleep(1)
                    send_keyboard_input("UP")  # up
                    await asyncio.sleep(1)
                    send_keyboard_input("v")  # QUIT
                    await asyncio.sleep(1)
                    send_keyboard_input("UP")  # QUIT emu
                    await asyncio.sleep(1)
                    send_keyboard_input("v")  #
                    await asyncio.sleep(1)
                    logger.debug("Done")
                    await asyncio.sleep(10)
                    '''
                    logger.debug("Killing retroarch")
                    os.system("sudo kill $(pidof retroarch)")
                    logger.debug("Done")
                    await asyncio.sleep(10)
                    logger.debug("Killing emulationstation")
                    os.system("sudo kill $(pidof emulationstation)")
                    logger.debug("Done")
                    await asyncio.sleep(10)
                    # logger.debug("Taking screenshot...")
                    # take_screenshot("gb.png")
                    self.game_mode = False
                    logger.debug("Done")
                    await ctx.send('```GAME MODE DEACTIVATED, BYE!```')
            else:
                await ctx.send("Game is not running.")
        elif arg.lower() == "loadstate":
            if self.game_mode:
                await self.load_game_state()
                await ctx.send('Loaded game from previously saved state')
                take_screenshot("gb.png")
                await ctx.send(file=discord.File('gb.png'))
            else:
                await ctx.send('Game is not running. ')
        elif arg.lower() == "savestate":
            if self.game_mode:
                await self.save_game_state()
                await ctx.send('Game saved!')
                take_screenshot("gb.png")
                await ctx.send(file=discord.File('gb.png'))
            else:
                await ctx.send('Game is not running. ')
        else:
            await ctx.send('```Invalid entry```')
            await ctx.send('```Usage:\n'
                           '{}game on : to activate game mode\n'
                           '{}game off : to deactivate game mode\n'
                           '{}game savestate : to save game state\n'
                           '{}game loadstate : to load game state\n```'.format(COMMAND_PREFIX,
                                                                               COMMAND_PREFIX,
                                                                               COMMAND_PREFIX,
                                                                               COMMAND_PREFIX))

    async def save_game_state(self):
        # m + f2
        logger.debug("saving game state")
        await self.keyboard.send_keyboard_shortcut(['M', 'F2'])
        logger.debug("done")

    async def load_game_state(self):
        # m + f4
        logger.debug("loading game state")
        await self.keyboard.send_keyboard_shortcut(['M', 'F4'])
        logger.debug("done")

    @commands.Cog.listener()
    async def on_message(self, message):
        logger.debug(message.content)
        if message.author == self.bot.user:
            return

        if self.game_mode:
            invalid_input_flag = False
            try:
                if message.content[:2].lower() == "up" and int(message.content[-1]):
                    for i in range(int(message.content[-1])):
                        await self.keyboard.send_keyboard_input("UP")
                elif message.content[:4].lower() == "down" and int(message.content[-1]):
                    for i in range(int(message.content[-1])):
                        await self.keyboard.send_keyboard_input("DOWN")
                elif message.content[:4].lower() == "left" and int(message.content[-1]):
                    for i in range(int(message.content[-1])):
                        await self.keyboard.send_keyboard_input("LEFT")
                elif message.content[:5].lower() == "right" and int(message.content[-1]):
                    for i in range(int(message.content[-1])):
                        await self.keyboard.send_keyboard_input("RIGHT")
                elif message.content.lower() == "a":
                    await self.keyboard.send_keyboard_input("z")
                elif message.content.lower() == "b":
                    await self.keyboard.send_keyboard_input("x")
                elif message.content.lower() == "l":
                    await self.keyboard.send_keyboard_input("a")
                elif message.content.lower() == "r":
                    await self.keyboard.send_keyboard_input("s")
                elif message.content.lower() == "select":
                    await self.keyboard.send_keyboard_input("v")
                elif message.content.lower() == "start":
                    await self.keyboard.send_keyboard_input("c")
                else:
                    logger.debug("Invalid game input!")
                    invalid_input_flag = True
                await asyncio.sleep(0.4)

                # m +c - exit
                if not invalid_input_flag:
                    take_screenshot("gb.png")
                    await message.channel.send(file=discord.File('gb.png'))
                # game_channel = self.bot.get_channel(GAMEBOY_TEST_CHANNEL_ID)
                # await game_channel.send(file=discord.File('gb.png'))
            except ValueError as vale:
                logger.exception(vale)
                await message.channel.send("```Empty/Invalid entry```")
            except Exception as e:
                logger.exception(e)


def setup(bot):
    bot.add_cog(Gameboy(bot))
