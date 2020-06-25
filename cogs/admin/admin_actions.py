import json
import aiohttp
import os
from base_logger import logger
from discord.ext import commands
from config import TEST2_CHANNEL_ID, GENERAL_CHANNEL_ID, ROOT_DIR


class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(brief='Turns on my Master\'s PC')
    async def switchon(self, ctx):
        logger.debug("Powering on PC")
        admin_id_path = os.path.join(ROOT_DIR, "keys/admin_id")
        with open(admin_id_path) as f:
            admin_id = f.read().strip()

        logger.debug(ctx.message.author.id)
        logger.debug(admin_id)
        if ctx.message.author.id == int(admin_id):
            session = aiohttp.ClientSession()
            data = {"action": "on"}
            api_path = os.path.join(ROOT_DIR, "keys/api")
            ''' read API endpoint from file '''
            with open(api_path) as f:
                pc_api = f.read().strip()
            res = await session.post(pc_api, data=json.dumps(data), headers={'content-type': 'application/json'})
            await session.close()
            await ctx.send('```Done```')
        else:
            await ctx.send('```Only my master can use this command.```')

    @commands.command(brief='', hidden=True)
    async def post(self, ctx, *args):
        if args[0] == 'gb':
            channel = self.bot.get_channel(TEST2_CHANNEL_ID)
            message = ' '.join(args[1:])
        else:
            channel = self.bot.get_channel(GENERAL_CHANNEL_ID)
            message = ' '.join(args)
        logger.debug("{} {}".format(len(args), message))
        await channel.send(message)


def setup(bot):
    bot.add_cog(Admin(bot))
