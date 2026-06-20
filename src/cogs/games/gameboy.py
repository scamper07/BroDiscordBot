import asyncio
import os

import discord
from discord.ext import commands

from base_logger import logger
from constants import (
    COMMAND_PREFIX,
    GAMEBOY_A,
    GAMEBOY_B,
    GAMEBOY_DOWN,
    GAMEBOY_HOTKEY,
    GAMEBOY_L,
    GAMEBOY_LEFT,
    GAMEBOY_R,
    GAMEBOY_RIGHT,
    GAMEBOY_SELECT,
    GAMEBOY_START,
    GAMEBOY_UP,
)

# uinput and raspi2png are only available on the Raspberry Pi host
try:
    import uinput
except ImportError:
    uinput = None


class VirtualKeyboard:
    """Emits key presses through a virtual uinput device (Raspberry Pi only)"""

    def __init__(self):
        if uinput is None:
            raise RuntimeError("uinput is not available on this host")
        keys = [getattr(uinput, "KEY_" + chr(c)) for c in range(ord("A"), ord("Z") + 1)]
        keys += [
            uinput.KEY_ENTER,
            uinput.KEY_UP,
            uinput.KEY_DOWN,
            uinput.KEY_LEFT,
            uinput.KEY_RIGHT,
            uinput.KEY_F2,
            uinput.KEY_F4,
        ]
        self.device = uinput.Device(tuple(keys))

    async def send_keyboard_input(self, string, press_enter_after_string=False):
        try:
            string = string.upper()
            if string in ["UP", "DOWN", "LEFT", "RIGHT"]:
                key = getattr(uinput, "KEY_" + string)
                self.device.emit(key, 1)
                await asyncio.sleep(0.4)
                self.device.emit(key, 0)
                await asyncio.sleep(0.4)
            else:
                for i in string:
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
        except Exception as err:
            logger.exception(err)

    async def send_keyboard_shortcut(self, list_of_keys):
        try:
            for i in list_of_keys:
                key = getattr(uinput, "KEY_" + i.upper())
                self.device.emit(key, 1)
                await asyncio.sleep(0.4)
            for i in list_of_keys:
                key = getattr(uinput, "KEY_" + i.upper())
                self.device.emit(key, 0)
                await asyncio.sleep(0.4)
        except Exception as err:
            logger.exception(err)


def take_screenshot(filename="test.png"):
    """Takes a screenshot of the Pi framebuffer using raspi2png"""
    logger.debug("taking screenshot")
    os.system(f"raspi2png -p {filename}")
    return 0


USAGE = (
    "```Usage:\n"
    f"{COMMAND_PREFIX}game on : to activate game mode\n"
    f"{COMMAND_PREFIX}game off : to deactivate game mode\n"
    f"{COMMAND_PREFIX}game savestate : to save game state\n"
    f"{COMMAND_PREFIX}game loadstate : to load game state\n```"
)


class Gameboy(commands.Cog):
    """
    Cog to play a 1 fps Pokemon GameBoy game with friends (Raspberry Pi host only)
    """

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.game_mode = False
        try:
            self.keyboard = VirtualKeyboard()
        except Exception as err:
            logger.warning(f"Gameboy virtual keyboard unavailable: {err}")
            self.keyboard = None

    @commands.command(brief="Play a 1 fps Pokemon GameBoy game with friends")
    async def game(self, ctx: commands.Context, arg: str = None) -> None:
        """Controls the GameBoy emulator (on/off/savestate/loadstate)"""
        if self.keyboard is None:
            await ctx.send("```Game controls are not available on this host```")
            return

        if not arg:
            await ctx.send(USAGE)
            return

        arg = arg.lower()
        if arg == "on":
            await self._start_game(ctx)
        elif arg == "off":
            await self._stop_game(ctx)
        elif arg == "loadstate":
            if self.game_mode:
                await self.load_game_state()
                await ctx.send("Loaded game from previously saved state")
                take_screenshot("gb.png")
                await ctx.send(file=discord.File("gb.png"))
            else:
                await ctx.send("Game is not running. ")
        elif arg == "savestate":
            if self.game_mode:
                await self.save_game_state()
                await ctx.send("Game saved!")
                take_screenshot("gb.png")
                await ctx.send(file=discord.File("gb.png"))
            else:
                await ctx.send("Game is not running. ")
        else:
            await ctx.send("```Invalid entry```")
            await ctx.send(USAGE)

    async def _start_game(self, ctx: commands.Context) -> None:
        if self.game_mode:
            await ctx.send("Game is already running")
            return
        async with ctx.typing():
            await ctx.send("Starting game. Please wait. This might take upto a minute")
            self.game_mode = True
            await self.keyboard.send_keyboard_input("emulationstation", True)
            await asyncio.sleep(30)
            await asyncio.sleep(1)
            await self.keyboard.send_keyboard_input(GAMEBOY_A)
            await asyncio.sleep(1)
            await self.keyboard.send_keyboard_input(GAMEBOY_A)
            await asyncio.sleep(25)
            await self.load_game_state()
            await asyncio.sleep(1)
            take_screenshot("gb.png")
            await ctx.send("Game ready to play")
            await asyncio.sleep(1)
            await ctx.send("```GAME MODE ACTIVATED!```")
            await ctx.send(
                "```Available Keys:\n"
                "   up <number>: to move up\n"
                "   down <number>: to move down\n"
                "   left <number>: to move left\n"
                "   right <number>: to move right\n"
                "   a : to press A\n"
                "   b : to press B\n"
                "   select: to press Select\n"
                "   start: to press Start\n```"
            )
            await ctx.send(file=discord.File("gb.png"))

    async def _stop_game(self, ctx: commands.Context) -> None:
        if not self.game_mode:
            await ctx.send("Game is not running.")
            return
        async with ctx.typing():
            await ctx.send("Stopping game safely. Please wait.")
            await self.save_game_state()
            await self.keyboard.send_keyboard_shortcut([GAMEBOY_HOTKEY, GAMEBOY_START])
            await asyncio.sleep(10)
            os.system("sudo kill $(pidof retroarch)")
            await asyncio.sleep(10)
            os.system("sudo kill $(pidof emulationstation)")
            await asyncio.sleep(10)
            self.game_mode = False
            await ctx.send("```GAME MODE DEACTIVATED, BYE!```")

    async def save_game_state(self):
        await self.keyboard.send_keyboard_shortcut([GAMEBOY_HOTKEY, "F2"])

    async def load_game_state(self):
        await self.keyboard.send_keyboard_shortcut([GAMEBOY_HOTKEY, "F4"])

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return
        if not self.game_mode or self.keyboard is None:
            return

        directions = {
            "up": GAMEBOY_UP,
            "down": GAMEBOY_DOWN,
            "left": GAMEBOY_LEFT,
            "right": GAMEBOY_RIGHT,
        }
        buttons = {
            "a": GAMEBOY_A,
            "b": GAMEBOY_B,
            "l": GAMEBOY_L,
            "r": GAMEBOY_R,
            "select": GAMEBOY_SELECT,
            "start": GAMEBOY_START,
        }
        content = message.content.lower()
        invalid_input_flag = False
        try:
            matched = next((d for d in directions if content.startswith(d)), None)
            if matched and int(message.content[-1]) <= 5:
                for _ in range(int(message.content[-1])):
                    await self.keyboard.send_keyboard_input(directions[matched])
            elif content in buttons:
                await self.keyboard.send_keyboard_input(buttons[content])
            else:
                logger.debug("Invalid game input!")
                invalid_input_flag = True
            await asyncio.sleep(0.4)

            if not invalid_input_flag:
                take_screenshot("gb.png")
                await message.channel.send(file=discord.File("gb.png"))
        except ValueError as vale:
            logger.exception(vale)
            await message.channel.send("```Empty/Invalid entry```")
        except Exception as err:
            logger.exception(err)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Gameboy(bot))
