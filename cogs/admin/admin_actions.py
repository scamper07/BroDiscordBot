import json
import aiohttp
import os
from base_logger import logger
from discord.ext import commands
from config import TEST2_CHANNEL_ID, GENERAL_CHANNEL_ID, ROOT_DIR, COMMAND_PREFIX


class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(brief='Turns on/off my Master\'s PC')
    async def power(self, ctx, arg=None):
        if not arg:
            await ctx.send('```Usage:(ADMIN ONLY)\n'
                           '{}power on : to switch on PC\n'
                           '{}power off : to shutdown PC\n```'.format(COMMAND_PREFIX,
                                                                      COMMAND_PREFIX))
            return

        elif arg.lower() == "on":
            admin_id_path = os.path.join(ROOT_DIR, "keys/admin_id")
            with open(admin_id_path) as f:
                admin_id = f.read().strip()
            if ctx.message.author.id == int(admin_id):
                ''' api way '''
                '''
                session = aiohttp.ClientSession()
                data = {"action": "on"}
                api_path = os.path.join(ROOT_DIR, "keys/api")
                try:
                    
                    # read API endpoint from file
                    # with open(api_path) as f:
                    #    pc_api = f.read().strip()
                    # res = await session.post(pc_api, data=json.dumps(data), headers={'content-type': 'application/json'})
                    # await session.close()
    
                    await ctx.send('```Done```')
                except Exception as e:
                    logger.exception(e)
                '''

                ''' direct call '''
                master_mac_path = os.path.join(ROOT_DIR, "keys/master_mac")
                with open(master_mac_path) as f:
                    master_mac = f.read().strip()
                logger.debug("Powering on PC")
                os.system("wakeonlan {}".format(master_mac))

                await ctx.send('```Done```')
            else:
                await ctx.send('```Only my master can use this command.```')

        elif arg.lower() == "off":
            admin_id_path = os.path.join(ROOT_DIR, "keys/admin_id")
            with open(admin_id_path) as f:
                admin_id = f.read().strip()
            if ctx.message.author.id == int(admin_id):
                master_ip_path = os.path.join(ROOT_DIR, "keys/master_ip")
                with open(master_ip_path) as f:
                    master_ip = f.read().strip()
                logger.debug("Shutting down PC")
                os.system("ssh preetham@{} shutdown /s".format(master_ip))
                await ctx.send('```Done```')
            else:
                await ctx.send('```Only my master can use this command.```')
        else:
            await ctx.send('```Invalid entry```')
            await ctx.send('```Usage:(ADMIN ONLY)\n'
                           '{}power on : to switch on PC\n'
                           '{}power off : to shutdown PC\n```'.format(COMMAND_PREFIX,
                                                                      COMMAND_PREFIX))

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
