import asyncio
import aiohttp
from discord.ext import commands
from discord_slash import cog_ext
from discord_slash.utils import manage_commands
from discord_slash.utils.manage_commands import create_choice

from base_logger import logger

url = "http://localhost:8080/api/v1/board"
DOT = ":white_medium_small_square:"
X = ":x:"
O = ":o:"

# dictionary that holds game sessions across multiple servers. key - server id, value - TTT game object
games = {}


# tictactoe game class
class TTT:
    def __init__(self, board, computer, player, difficulty):
        self.board = board
        self.computer = computer
        self.player = player
        self.difficulty = difficulty

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
            if game_over:
                return True, winner
            game_over, winner = check_winner_condition(c)
            if game_over:
                return True, winner

        # left to bottom right
        s = board[0][0] + board[1][1] + board[2][2]
        game_over, winner = check_winner_condition(s)
        if game_over:
            return True, winner

        # right to bottom left diagonal
        s = board[0][2] + board[1][1] + board[2][0]
        game_over, winner = check_winner_condition(s)
        if game_over:
            return True, winner

        if dot_count == 0:
            return

        return False


# tictactoe discord cog class
class Tictactoe(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.game_mode = False
        self.bot_thinking = False

    @commands.command(brief='Play a tic tac toe game with GrandMaster Bro', aliases=['ttt'])
    async def tictactoe(self, ctx, difficulty="impossible"):
        async with ctx.typing():
            await self._tictactoe(ctx, difficulty)

    @cog_ext.cog_slash(name="tictactoe",
                       description='Play a tic tac toe game with GrandMaster Bro',
                       #guild_ids=[207481917975560192, 572648167573684234],
                       options=[manage_commands.create_option(
                           name="difficulty",
                           description="Supported: \"easy\", \"medium\", \"impossible\"",
                           option_type=3,
                           required=False,
                           choices=[
                               create_choice(
                                   name="Easy",
                                   value="easy"
                               ),
                               create_choice(
                                   name="Medium",
                                   value="medium"
                               ),
                               create_choice(
                                   name="Impossible",
                                   value="impossible"
                               )
                           ]
                       ),
                       ],
                       )
    async def tictactoes(self, ctx, difficulty="impossible"):
        await self._tictactoe(ctx, difficulty)

    async def _tictactoe(self, ctx, difficulty="impossible"):
        if ctx.guild.id in games:
            await ctx.send("Game already in progress")
        else:
            games[ctx.guild.id] = TTT(board=[[".", ".", "."],
                                             [".", ".", "."],
                                             [".", ".", "."]
                                             ],
                                      computer="O",
                                      player="X",
                                      difficulty=difficulty)

            logger.debug("Starting TTT...")
            logger.debug(games)

            await ctx.send(
                "Starting game. Player plays 'X'. Enter input as x,y coordinate (valid range 0,0 to 2,2)\nExample: 1,2")
            logger.debug("Starting game")
            await ctx.send(games[ctx.guild.id].beautify_board())
            self.game_mode = True
            logger.debug("Done")

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

            if self.bot_thinking:
                await message.channel.send("Slow down Bro. Try again...")
                return

            game = games[message.guild.id]

            # adding check to see if position is already filled
            if game.board[int(user_input[0])][int(user_input[1])] == ".":
                self.bot_thinking = True  # added flag to handle user input spam while bot is executing api
                game.board[int(user_input[0])][int(user_input[1])] = game.player
                await message.channel.send(game.beautify_board())
                if game.hasWon(game.board):
                    await message.channel.send("Congratulations! Player has won :trophy: :first_place:")
                    del games[message.guild.id]     # delete game instance
                    self.bot_thinking = False
                    logger.debug(games)
                    return
                elif game.hasWon(game.board) is None:
                    await message.channel.send("Match drawn :handshake:")
                    del games[message.guild.id]     # delete game instance
                    self.bot_thinking = False
                    logger.debug(games)
                    return

                await message.channel.send("Thinking...")
                # await asyncio.sleep(0.25)

                logger.debug("DIFFICULTY:")
                logger.debug(game.difficulty)
                post_data = {
                    "positions": game.board,
                    "player": "X",
                    "difficulty": game.difficulty
                }
                async with aiohttp.ClientSession() as session:
                    async with session.post(url, json=post_data) as resp:
                        user_input = await resp.json()
                        if user_input["move"]:
                            game.board[int(user_input["move"][0])][int(user_input["move"][1])] = game.computer
                            await message.channel.send(game.beautify_board())
                            self.bot_thinking = False
                            if game.hasWon(game.board):
                                await message.channel.send("GrandMaster Bro wins! :robot:")
                                del games[message.guild.id]      # delete game instance
                                logger.debug(games)
                            elif game.hasWon(game.board) is None:
                                await message.channel.send("Match drawn :handshake:")
                                del games[message.guild.id]      # delete game instance
                                logger.debug(games)
            else:
                await message.channel.send("Position already filled. Try some other coordinate...")

        except ValueError as vale:
            logger.exception(vale)
        except Exception as e:
            logger.exception(e)
            self.bot_thinking = False


def setup(bot):
    bot.add_cog(Tictactoe(bot))
