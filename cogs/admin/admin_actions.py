import discord
import os
import subprocess
from discord_slash.utils.manage_commands import create_choice
from base_logger import logger
from discord.ext import commands
from config import TEST2_CHANNEL_ID, GENERAL_CHANNEL_ID, ROOT_DIR, COMMAND_PREFIX, ADMIN_ID, TEST_CHANNEL_ID
from utils import get_public_url, embed_send
from discord_slash import cog_ext, SlashContext, manage_commands
from constants import DESCRIPTION_PC_CONTROL


class Admin(commands.Cog):
    """
    A cog for admin commands
    """
    def __init__(self, bot):
        self.bot = bot

    @commands.command(brief=DESCRIPTION_PC_CONTROL)
    @commands.is_owner()
    async def power(self, ctx, arg=None):
        await self._power(ctx, arg)

    @cog_ext.cog_slash(name="power",
                       description=DESCRIPTION_PC_CONTROL,
                       options=[manage_commands.create_option(
                            name="arg",
                            description="\"on\" to switch on, \"off\" to switch off",
                            option_type=3,
                            required=True,
                            choices=[
                                   create_choice(
                                       name="On",
                                       value="on"
                                   ),
                                   create_choice(
                                       name="Off",
                                       value="off"
                                   )
                               ]
                            ),
                       ],
                       )
    async def powers(self, ctx: SlashContext, arg: str):
        await self._power(ctx, arg)

    async def _power(self, ctx, arg: str):
        logger.debug("PRE: {}".format(ctx))
        try:
            if not arg:
                if isinstance(ctx, discord.ext.commands.context.Context):
                    await ctx.send('```Usage:(ADMIN ONLY)\n'
                                   '{}power on : to switch on PC\n'
                                   '{}power off : to shutdown PC\n```'.format(COMMAND_PREFIX,
                                                                              COMMAND_PREFIX))

            elif arg.lower() == "on":
                if ctx.author.id == int(ADMIN_ID):
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

                    if os.environ.get('RUNNING_DOCKER_COMPOSE'):
                        key_file_path = os.environ.get("MASTER_MAC")
                        with open(key_file_path, 'r') as key_file:
                            master_mac = key_file.read().strip()
                    else:
                        master_mac = os.environ.get("MASTER_MAC")
                    logger.debug("Powering on PC")
                    os.system("wakeonlan {}".format(master_mac))
                    await ctx.send("```Powering on PC```")
                else:
                    await ctx.send("```Only my master can use this command```")

            elif arg.lower() == "off":
                if os.environ.get('RUNNING_DOCKER_COMPOSE'):
                    key_file_path = os.environ.get("ADMIN_ID")
                    with open(key_file_path, 'r') as key_file:
                        admin_id = key_file.read().strip()
                else:
                    admin_id = os.environ.get("ADMIN_ID")

                if ctx.author.id == int(admin_id):
                    if os.environ.get('RUNNING_DOCKER_COMPOSE'):
                        key_file_path = os.environ.get("MASTER_IP")
                        with open(key_file_path, 'r') as key_file:
                            master_ip = key_file.read().strip()
                    else:
                        master_ip = os.environ.get("MASTER_IP")
                    logger.debug("Shutting down PC")
                    os.system("ssh preetham@{} shutdown /s".format(master_ip))
                    await ctx.send('```Shutting down PC```')
                else:
                    await ctx.send('```Only my master can use this command.```')
            else:
                await ctx.send('```Invalid entry```')
                if isinstance(ctx, discord.ext.commands.context.Context):
                    await ctx.send('```Usage:(ADMIN ONLY)\n'
                                   '{}power on : to switch on PC\n'
                                   '{}power off : to shutdown PC\n```'.format(COMMAND_PREFIX,
                                                                              COMMAND_PREFIX))
        except Exception as e:
            logger.exception(e)
            await send_error_message(ctx)

    @commands.command(hidden=True)
    async def post(self, ctx, *args):
        if args[0] == 'gb':
            channel = self.bot.get_channel(TEST2_CHANNEL_ID)
            message = ' '.join(args[1:])
        elif args[0] == 'test':
            channel = self.bot.get_channel(TEST_CHANNEL_ID)
            message = ' '.join(args[1:])
        else:
            channel = self.bot.get_channel(GENERAL_CHANNEL_ID)
            message = ' '.join(args)
        logger.debug("{} {}".format(len(args), message))
        await channel.send(message)

    @commands.command(brief='Shows my host hardware-software info')
    async def sysinfo(self, ctx):
        await self._sysinfo(ctx)

    @cog_ext.cog_slash(name="sysinfo",
                       description='Shows my host hardware-software info',
                       )
    async def sysinfos(self, ctx: SlashContext):
        await self._sysinfo(ctx)

    async def _sysinfo(self, ctx):
        try:
            embed = discord.Embed(
                title="System Info",
                description="Showing my host hardware/software information",
                colour=discord.Color.gold()
            )
            embed.set_footer(text="Hope that was helpful, bye!")
            embed.set_author(name="Bro Bot", icon_url=self.bot.user.avatar_url)
            embed.set_thumbnail(url=ctx.guild.icon_url)
            result = subprocess.Popen(['neofetch', '--stdout'], stdout=subprocess.PIPE)
            for line in result.stdout:
                line = line.decode('utf-8').strip('\n').split(':')
                if len(line) == 2:
                    if line[0] == "OS" or line[0] == "Host":
                        embed.add_field(name=line[0], value=line[1], inline=False)
                    else:
                        embed.add_field(name=line[0], value=line[1], inline=True)

            # Raspberry Pi Only!!!
            if os.uname()[1] == "anton":
                temp = subprocess.Popen(['/opt/vc/bin/vcgencmd', 'measure_temp'], stdout=subprocess.PIPE)
                for line in temp.stdout:
                    line = line.decode('utf-8').strip('\n').split('=')
                    if len(line) == 2:
                        embed.add_field(name="CPU Temp", value=line[1], inline=True)

                url = await get_public_url()
                embed.add_field(name="Public URL", value=url, inline=False)

                # await wait_message.edit(content='', embed=embed)
                await embed_send(ctx, embed)
        except Exception as e:
            logger.exception(e)
            await send_error_message(ctx)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def runcmd(self, ctx, *args):
        logger.debug(args)
        try:
            result = subprocess.Popen(args, stdout=subprocess.PIPE)
            logger.debug(result.stdout)
            out = ""
            for line in result.stdout:
                out += line.decode('utf-8')
            logger.debug(out)
            embed = discord.Embed(title=out)
            await embed_send(ctx, embed)
        except Exception as e:
            logger.exception(e)
            await send_error_message(ctx)


def setup(bot):
    bot.add_cog(Admin(bot))
