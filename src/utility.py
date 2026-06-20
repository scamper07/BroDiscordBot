import asyncio
import datetime
import json
import os

import aiohttp
import discord

from base_logger import logger


async def fetch_json(url):
    """Fetch and decode a JSON payload from a url, returning None on failure"""
    json_response = None
    session = aiohttp.ClientSession()
    try:
        async with session.get(url) as resp:
            data = await resp.read()
            json_response = json.loads(data)
    except Exception as err:
        logger.exception(err)
    finally:
        await session.close()
    return json_response


def get_secret(name: str) -> str:
    """Read a secret either from a mounted file (docker compose) or the environment.

    When running under docker compose the env var holds a path to a secret file,
    otherwise the env var holds the value directly.
    """
    if os.environ.get("RUNNING_DOCKER_COMPOSE"):
        with open(os.environ[name], "r") as key_file:
            return key_file.read().strip()
    return os.environ.get(name)


async def sleep_until_time(trigger_time: str) -> None:
    """Sleep until the next occurrence of trigger_time (24-hr HH:MM, host local time)"""
    hour, minute = (int(part) for part in trigger_time.split(":"))
    now = datetime.datetime.today()
    future = datetime.datetime(now.year, now.month, now.day, hour, minute)
    if now.hour >= hour:
        future += datetime.timedelta(days=1)
    await asyncio.sleep((future - now).seconds)


async def send_embed(
    ctx,
    embed: discord.Embed = None,
    title=None,
    description=None,
    url=None,
    color=discord.Colour.purple(),
    image_url=None,
    dm=False,
):
    """Send a custom embed with sensible defaults.

    When ``embed`` is not supplied one is built from the remaining arguments.
    A caller-provided image or footer is preserved rather than overwritten.
    """
    if not embed:
        embed = discord.Embed(
            title=title, description=description, color=color, url=url
        )

    if image_url:
        embed.set_image(url=image_url)
    # if not embed.footer.text:
    #    embed.set_footer(text=f"Powered by discord.py v{discord.__version__}")

    target = ctx.author if dm else ctx
    await target.send(embed=embed)
