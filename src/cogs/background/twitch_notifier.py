import asyncio
import json
import os

import aiohttp
from discord.ext import tasks, commands

from base_logger import logger
from constants import (
    GENERAL_CHANNEL_ID,
    ROOT_DIR,
    TWITCH_GAMES_API,
    TWITCH_NOT_STREAMING,
    TWITCH_STARTED_STREAMING,
    TWITCH_STILL_STREAMING,
    TWITCH_STREAMS_API,
    TWITCH_USERS_API,
)
from utility import get_secret

STREAMERS_FILE = os.path.join(ROOT_DIR, "data/streamers.txt")


class Twitch(commands.Cog):
    """
    Cog to notify a channel when registered Twitch streamers go live
    """

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.live_status_dict = {}
        self.streamers = []
        self.twitch_notifier.start()

    def cog_unload(self) -> None:
        self.twitch_notifier.cancel()

    @staticmethod
    def _twitch_headers():
        """Return the Twitch API headers, or None when credentials aren't set"""
        client_id = get_secret("TWITCH_CLIENT_ID")
        app_access_token = get_secret("TWITCH_APP_ACCESS")
        if not client_id or not app_access_token:
            return None
        return {
            "Client-ID": client_id,
            "Authorization": "Bearer " + app_access_token,
        }

    @commands.hybrid_command(
        aliases=["tn"],
        description="Registers a streamer whose streams will be notified",
    )
    async def twitchnotify(self, ctx: commands.Context, username: str = None) -> None:
        """Registers a streamer whose streams will be notified"""
        async with ctx.typing():
            if not username:
                await ctx.send(
                    "Provide a streamer name whose streams you want to be notified"
                )
                return

            headers = self._twitch_headers()
            if not headers:
                await ctx.send("Twitch notifications are not configured")
                return

            session = aiohttp.ClientSession()
            try:
                async with session.get(
                    TWITCH_USERS_API.format(username), headers=headers
                ) as resp:
                    json_response = json.loads(await resp.read())
                    logger.debug(json_response)

                if json_response["data"]:
                    os.makedirs(os.path.dirname(STREAMERS_FILE), exist_ok=True)
                    with open(STREAMERS_FILE, "a+") as f:
                        f.write(username + "\n")
                    await ctx.send(
                        f"Streamer added. Will notify you when **{username}** "
                        "goes live!"
                    )
                else:
                    await ctx.send(
                        f"{username} does not exists. Check streamer name and "
                        "add again"
                    )
            except Exception as err:
                logger.exception(err)
                await ctx.send("Sorry, could not add streamer. Try again later")
            finally:
                await session.close()

    @commands.hybrid_command(
        aliases=["ts"],
        description="Get list of streamers whose streams will be notified",
    )
    async def twitchsubs(self, ctx: commands.Context) -> None:
        """Gets the list of streamers whose streams will be notified"""
        async with ctx.typing():
            if self.streamers:
                streamer_list = "\n".join(str(elem) for elem in self.streamers)
                await ctx.send(
                    "```Notifying streams from \n=======================\n"
                    f"{streamer_list}```"
                )
            else:
                await ctx.send(
                    "```No streamers to notify. Add streamers using " ".twitchnotify```"
                )

    @tasks.loop(minutes=5)
    async def twitch_notifier(self) -> None:
        await self.bot.wait_until_ready()
        headers = self._twitch_headers()
        if not headers:
            logger.debug("Twitch credentials not configured, skipping notifier")
            return

        self.streamers = []
        if os.path.exists(STREAMERS_FILE):
            with open(STREAMERS_FILE, "r") as f:
                for line in f:
                    self.streamers.append(line.strip())

        for player in self.streamers:
            self.live_status_dict.setdefault(player, TWITCH_NOT_STREAMING)

        logger.debug(self.live_status_dict)
        channel = self.bot.get_channel(GENERAL_CHANNEL_ID)
        session = aiohttp.ClientSession()
        try:
            for streamer in self.streamers:
                async with session.get(
                    TWITCH_STREAMS_API + streamer, headers=headers
                ) as resp:
                    json_response = json.loads(await resp.read())
                    logger.debug(json_response)

                if json_response["data"]:
                    await self._handle_live(
                        session, headers, channel, streamer, json_response
                    )
                else:
                    await self._handle_offline(channel, streamer)
                await asyncio.sleep(2)
        except Exception as err:
            logger.exception(err)
        finally:
            await session.close()

    async def _handle_live(self, session, headers, channel, streamer, json_response):
        if self.live_status_dict[streamer] != TWITCH_NOT_STREAMING:
            logger.debug(f"{streamer} is still live. not sending")
            self.live_status_dict[streamer] = TWITCH_STILL_STREAMING
            return

        try:
            user_name = json_response["data"][0]["user_name"]
            game_id = json_response["data"][0]["game_id"]
            twitch_url = f"https://www.twitch.tv/{user_name}"
            if game_id:
                async with session.get(
                    TWITCH_GAMES_API + game_id, headers=headers
                ) as resp:
                    game_response = json.loads(await resp.read())
                game_name = game_response["data"][0]["name"]
                await channel.send(
                    f"**{user_name} is live on Twitch playing {game_name}!**\n"
                    f"{twitch_url}"
                )
            else:
                await channel.send(f"**{user_name} is live on Twitch!**\n{twitch_url}")
            self.live_status_dict[streamer] = TWITCH_STARTED_STREAMING
        except Exception as err:
            logger.exception(err)

    async def _handle_offline(self, channel, streamer):
        logger.debug(f"{streamer} is not live")
        if self.live_status_dict[streamer] in (
            TWITCH_STARTED_STREAMING,
            TWITCH_STILL_STREAMING,
        ):
            await channel.send(f"{streamer}'s stream has ended.")
            self.live_status_dict[streamer] = TWITCH_NOT_STREAMING

    @twitch_notifier.before_loop
    async def before(self) -> None:
        await self.bot.wait_until_ready()


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Twitch(bot))
