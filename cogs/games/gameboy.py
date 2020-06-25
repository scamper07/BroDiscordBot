from discord.ext import commands
from config import GAME_MODE, COMMAND_PREFIX


class Gameboy(commands.Cog):
    @commands.command(brief='Allows you to play a GameBoy game with friends')
    async def game(self, ctx, arg=None):
        if not arg:
            await ctx.send('```Usage:\n'
                           '{}game on : to activate game mode\n'
                           '{}game off : to deactivate game mode\n```'.format(COMMAND_PREFIX, COMMAND_PREFIX))
            return

        if arg.lower() == "on":
            GAME_MODE = True
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
        elif arg.lower() == "off":
            GAME_MODE = False
            await ctx.send('```GAME MODE DEACTIVATED, BYE!```')
        else:
            await ctx.send('```Invalid entry```')
            await ctx.send('```Usage:\n'
                           '{}game on : to activate game mode\n'
                           '{}game off : to deactivate game mode\n```'.format(COMMAND_PREFIX, COMMAND_PREFIX))
