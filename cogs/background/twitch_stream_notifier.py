import aiohttp
import asyncio
import json
import os
from discord.ext import tasks, commands
from base_logger import logger
from config import ROOT_DIR, TWITCH_NOT_STREAMING, TWITCH_STARTED_STREAMING, TWITCH_STILL_STREAMING, GENERAL_CHANNEL_ID


class TwitchNotifier(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.live_status_dict = {}
        self.streamers = ["swatplayskreede",
                          "code_name_47_",
                          "bamboozle_heck",
                          "kbharathi",
                          "supersonic_mk",
                          "scamper07"
                          ]  # Twitch user names
        for player in self.streamers:
            self.live_status_dict.update({player: TWITCH_NOT_STREAMING})
        logger.debug("starting self.twitch_notifier.start()")
        self.twitch_notifier.start()

    def cog_unload(self):
        self.twitch_notifier.cancel()

    @tasks.loop(minutes=5)
    async def twitch_notifier(self):
        await self.bot.wait_until_ready()

        client_id_path = os.path.join(ROOT_DIR, "keys/twitch_client_id")
        app_access_path = os.path.join(ROOT_DIR, "keys/twitch_app_access")

        with open(client_id_path) as f:
            client_id = f.read().strip()

        with open(app_access_path) as f:
            app_access_token = f.read().strip()

        url = "https://api.twitch.tv/helix/streams?user_login="  # Twitch get streams api
        games_url = "https://api.twitch.tv/helix/games?id="  # Twitch get game api
        headers = {'Client-ID': client_id,
                   'Authorization': 'Bearer ' + app_access_token,
                   }

        # Total 550-600 bytes of data fetched
        logger.debug(self.live_status_dict)

        channel = self.bot.get_channel(GENERAL_CHANNEL_ID)  # channel to which notification should be sent
        session = aiohttp.ClientSession()
        try:
            for streamer in self.streamers:
                twitch_url = url + streamer

                async with session.get(twitch_url, headers=headers) as resp:
                    data = await resp.read()
                    json_response = json.loads(data)
                    logger.debug(json_response)

                    # if data not empty, user is streaming
                    if json_response['data']:
                        # TODO: if oAuth token gets expired, json wont have data field, need to regen token.
                        if self.live_status_dict[streamer] == TWITCH_NOT_STREAMING:
                            game_id = json_response['data'][0]['game_id']

                            # get info on game the user is playing
                            async with session.get(games_url + game_id, headers=headers) as resp:
                                game_data = await resp.read()
                                game_response = json.loads(game_data)
                                logger.debug(game_response)  # size: 140 bytes
                                logger.debug("https://www.twitch.tv/{}".format(json_response['data'][0]['user_name']))

                                await channel.send(
                                    "**{} is live on Twitch playing {}!**\nhttps://www.twitch.tv/{}".format(json_response['data'][0]['user_name'],
                                                                                  game_response['data'][0]['name'], json_response['data'][0]['user_name']))
                            self.live_status_dict[streamer] = TWITCH_STARTED_STREAMING
                        else:
                            logger.debug("{} is still live. not sending".format(streamer))
                            self.live_status_dict[streamer] = TWITCH_STILL_STREAMING
                    else:
                        logger.debug("{} is not live".format(streamer))
                        if self.live_status_dict[streamer] == TWITCH_STARTED_STREAMING or self.live_status_dict[
                            streamer] == TWITCH_STILL_STREAMING:
                            await channel.send("{}\'s stream has ended.".format(streamer))
                            self.live_status_dict[streamer] = TWITCH_NOT_STREAMING
                await asyncio.sleep(2)
        except Exception as e:
            logger.exception(e)
        finally:
            await session.close()

    @twitch_notifier.before_loop
    async def before(self):
        await self.bot.wait_until_ready()


def setup(bot):
    bot.add_cog(TwitchNotifier(bot))
