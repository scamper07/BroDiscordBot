import asyncio

import discord
from aiohttp import web
from discord.ext import commands
from base_logger import logger
from config import TEST_CHANNEL_ID, ALPHA_MALES_GOODIE_BAG_CHANNEL, GENERAL_CHANNEL_ID, F1_DISCUSSION_CHANNEL_ID


class WebHookListener(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # self.channel_list = [TEST_CHANNEL_ID]
        self.channel_list = [F1_DISCUSSION_CHANNEL_ID]

    async def webserver(self):
        async def handler(request):
            logger.debug(request)
            # res = request.get_json()
            try:
                res = await request.json()
                logger.info(res)
                if "austria" in res['title'].lower():
                    gp_place = "Austria"
                elif "styria" in res['title'].lower():
                    gp_place = "Styria"
                elif "hungar" in res['title'].lower():
                    gp_place = "Hungar"
                elif "britain" in res['title'].lower():
                    gp_place = "Great%20Britain"
                elif "anniversary" in res['title'].lower():
                    gp_place = "70th%20Anniversary"
                elif "spanish" in res['title'].lower() or "spain" in res['title'].lower():
                    gp_place = "Spain"
                elif "belg" in res['title'].lower():
                    gp_place = "Belgium"
                elif "ital" in res['title'].lower():
                    gp_place = "Italy"
                else:
                    gp_place = ""

                embed = discord.Embed(
                    title=res['title'],
                    description="Event in 15 minutes",
                    colour=discord.Color.red()
                )
                embed.set_author(name="Bro Bot", icon_url=self.bot.user.avatar_url)
                embed.set_image(url="https://www.formula1.com/content/dam/fom-website/2018-redesign-assets/Track%20icons%204x3/{}%20carbon.png.transform/8col/image.png".format(gp_place))
                embed.set_thumbnail(
                    url="https://www.google.com/url?sa=i&url=http%3A%2F%2Ft0.gstatic.com%2Fimages%3Fq%3Dtbn%3AANd9GcTxRmfGmozn5szS7lnaBIceJ9sweiO45WBJmnsRzTdcjFAlLFQ4&psig=AOvVaw0Mp-oe1kLL3yOoi6vPptQV&ust=1594016113076000&source=images&cd=vfe&ved=0CA0QjhxqFwoTCKCj1_O6teoCFQAAAAAdAAAAABAD")
                embed.add_field(name="Date", value=res['starts']+" IST", inline=False)
                embed.add_field(name="Track", value=res['location'], inline=True)
                embed.set_footer(text="Hope that was helpful, bye!")
                for channel in self.channel_list:
                    message_channel = self.bot.get_channel(channel)
                    await message_channel.send(embed=embed)
            except Exception as e:
                logger.exception(e)
            return web.Response(text="Success")

        app = web.Application()
        app.router.add_get('/', handler)
        runner = web.AppRunner(app)
        await runner.setup()
        self.site = web.TCPSite(runner, '0.0.0.0', 4200)
        await self.bot.wait_until_ready()
        await self.site.start()

    def __unload(self):
        asyncio.ensure_future(self.site.stop())


def setup(bot):
    wl = WebHookListener(bot)
    bot.add_cog(wl)
    bot.loop.create_task(wl.webserver())
