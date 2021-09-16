import datetime
import aiohttp
import json
import discord_slash
import os
import asyncio
import random
import discord
import uinput
from base_logger import logger


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
