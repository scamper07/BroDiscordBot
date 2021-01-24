import asyncio
import os

import aiohttp
import discord
from discord.ext import commands
from base_logger import logger

url = "https://tictactoe.loca.lt/api/v1/board"
DOT = ":white_small_square:"
X = ":x:"
O = ":o:"

games = {}


class Tictactoe(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.game_mode = False
        self.board = [[".", ".", "."],
                      [".", ".", "."],
                      [".", ".", "."]
                      ]
        self.computer = "O"
        self.player = "X"

    @commands.command(brief='Play a tic tac toe game with GrandMaster Bro', aliases=['ttt'])
    async def tictactoe(self, ctx):
        '''
        if ctx.guild.id in games:
            await ctx.send("Game already in progress")
        else:
            games[ctx.guild.id] = Tictactoe(self.bot)
        '''
        async with ctx.typing():
            await ctx.send(
                "Starting game. Player plays 'X'. Enter input as x,y coordinate (valid range 0,0 to 2,2)\nExample: 1,2")
            logger.debug("Starting game")
            await ctx.send(self.beautify_board())
            self.game_mode = True
            logger.debug("Done")

    def beautify_board(self):
        s = "| "
        for row in self.board:
            for elem in row:
                if elem == "X":
                    elem = X
                elif elem == "O":
                    elem = O
                else:
                    elem = DOT
                elem += " | "
                s += elem
            s += "\n| "

        s = s[:-2]
        return s

    def hasWon(self, board):
        dot_count = 0

        def check_winner_condition(s):
            if s == "XXX":
                return True, "X"
            elif s == "OOO":
                return True, "O"
            else:
                return False, "_"

        for row in range(len(board)):
            r = ""
            c = ""
            for col in range(len(board[0])):
                r += board[row][col]
                c += board[col][row]
                if board[row][col] == ".":
                    dot_count += 1

            game_over, winner = check_winner_condition(r)
            if (game_over):
                return True, winner
            game_over, winner = check_winner_condition(c)
            if (game_over):
                return True, winner

        # left to bottom right
        s = board[0][0] + board[1][1] + board[2][2]
        game_over, winner = check_winner_condition(s)
        if (game_over):
            return True, winner

        # right to bottom left diagonal
        s = board[0][2] + board[1][1] + board[2][0]
        game_over, winner = check_winner_condition(s)
        if (game_over):
            return True, winner

        if dot_count == 0:
            return

        return False

    def reset_game(self):
        self.board = [[".", ".", "."],
                      [".", ".", "."],
                      [".", ".", "."]
                      ]
        self.game_mode = False

    @commands.Cog.listener()
    async def on_message(self, message):
        # logger.debug(message.content)
        if message.author == self.bot.user:
            return

        try:
            if not self.game_mode:  # to process messages only if game has started
                return

            user_input = message.content.split(',')
            # validations
            if len(user_input) > 2:
                return

            if int(user_input[0]) < 0 or int(user_input[0]) > 2 or int(user_input[1]) < 0 or int(user_input[1]) > 2:
                return

            if self.board[int(user_input[0])][int(user_input[1])] == ".":
                self.board[int(user_input[0])][int(user_input[1])] = self.player
                await message.channel.send(self.beautify_board())
                if self.hasWon(self.board):
                    await message.channel.send("Congratulations! Player has won :trophy: :first_place:")
                    self.reset_game()
                    return
                elif self.hasWon(self.board) is None:
                    await message.channel.send("Match drawn :handshake:")
                    self.reset_game()
                    return

                await message.channel.send("Thinking...")
                await asyncio.sleep(0.5)

                # await message.channel.send("https://tenor.com/view/smart-hangover-alan-genius-zach-galifianakis-gif-5568438")

                post_data = {
                    "positions": self.board,
                    "isX": False
                }
                async with aiohttp.ClientSession() as session:
                    async with session.post(url, json=post_data) as resp:
                        user_input = await resp.json()
                        if user_input["move"]:
                            self.board[int(user_input["move"][0])][int(user_input["move"][1])] = self.computer
                            await message.channel.send(self.beautify_board())
                            if self.hasWon(self.board):
                                await message.channel.send("GrandMaster Bro wins! :robot:")
                                self.reset_game()
                            elif self.hasWon(self.board) is None:
                                await message.channel.send("Match drawn :handshake:")
                                self.reset_game()
            else:
                await message.channel.send("Position already filled. Try some other coordinate...")

        except ValueError as vale:
            logger.exception(vale)
        except Exception as e:
            logger.exception(e)


def setup(bot):
    bot.add_cog(Tictactoe(bot))
