import asyncio
import random
from typing import Literal

from discord.ext import commands

from base_logger import logger
from utility import send_embed

DOT = ":white_medium_small_square:"
X = ":x:"
CIRCLE = ":o:"

# game sessions across servers. key - server id, value - TTT game object
games = {}


class TTT:
    """Holds the board and players for a single tic tac toe game"""

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
                    elem = CIRCLE
                else:
                    elem = DOT
                s += elem + " | "
            s += "\n| "
        return s[:-2]

    def hasWon(self, board):
        dot_count = 0

        def check_winner_condition(s):
            if s == "XXX":
                return True, "X"
            elif s == "OOO":
                return True, "O"
            return False, "_"

        for row in range(len(board)):
            r = c = ""
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

        game_over, winner = check_winner_condition(
            board[0][0] + board[1][1] + board[2][2]
        )
        if game_over:
            return True, winner

        game_over, winner = check_winner_condition(
            board[0][2] + board[1][1] + board[2][0]
        )
        if game_over:
            return True, winner

        if dot_count == 0:
            return

        return False

    def available_moves(self):
        """Return the list of empty (row, col) coordinates"""
        return [(r, c) for r in range(3) for c in range(3) if self.board[r][c] == "."]

    def _winner(self):
        """Return 'X'/'O' for a winner, 'draw' for a full board, else None"""
        result = self.hasWon(self.board)
        if result:
            return result[1]
        if result is None:
            return "draw"
        return None

    def _minimax(self, is_computer_turn):
        """Score the current board from the computer's perspective"""
        winner = self._winner()
        if winner == self.computer:
            return 1
        if winner == self.player:
            return -1
        if winner == "draw":
            return 0

        mark = self.computer if is_computer_turn else self.player
        scores = []
        for r, c in self.available_moves():
            self.board[r][c] = mark
            scores.append(self._minimax(not is_computer_turn))
            self.board[r][c] = "."
        return max(scores) if is_computer_turn else min(scores)

    def best_move(self):
        """Pick the computer's next move based on the configured difficulty"""
        moves = self.available_moves()
        if not moves:
            return None

        # easy always plays randomly; medium plays randomly half the time
        if self.difficulty == "easy" or (
            self.difficulty == "medium" and random.random() < 0.5
        ):
            return random.choice(moves)

        # otherwise play the optimal (unbeatable) move
        best_score = None
        best = moves[0]
        for r, c in moves:
            self.board[r][c] = self.computer
            score = self._minimax(False)
            self.board[r][c] = "."
            if best_score is None or score > best_score:
                best_score, best = score, (r, c)
        return best


class Tictactoe(commands.Cog):
    """
    Cog to play a game of tic tac toe against GrandMaster Bro
    """

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.bot_thinking = False

    @commands.hybrid_command(
        aliases=["ttt"], description="Play a tic tac toe game with GrandMaster Bro"
    )
    async def tictactoe(
        self,
        ctx: commands.Context,
        difficulty: Literal["easy", "medium", "impossible"] = "impossible",
    ) -> None:
        """Play a tic tac toe game with GrandMaster Bro"""
        async with ctx.typing():
            await self._tictactoe(ctx, difficulty)

    async def _tictactoe(self, ctx: commands.Context, difficulty: str) -> None:
        if ctx.guild.id in games:
            await send_embed(ctx=ctx, title="Game already in progress")
            return

        games[ctx.guild.id] = TTT(
            board=[[".", ".", "."], [".", ".", "."], [".", ".", "."]],
            computer="O",
            player="X",
            difficulty=difficulty,
        )
        logger.debug("Starting TTT...")
        await send_embed(
            ctx=ctx,
            title=(
                "Starting game.\nPlayer plays 'X'.\n"
                "Enter input as x,y coordinate (valid range 0,0 to 2,2)\n"
                "Example: 1,2"
            ),
        )
        await ctx.send(games[ctx.guild.id].beautify_board())

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        # only process moves for guilds that have an active game
        if not message.guild or message.guild.id not in games:
            return

        try:
            user_input = message.content.split(",")
            if len(user_input) > 2:
                return
            if (
                int(user_input[0]) < 0
                or int(user_input[0]) > 2
                or int(user_input[1]) < 0
                or int(user_input[1]) > 2
            ):
                return

            if self.bot_thinking:
                await send_embed(
                    ctx=message.channel, title="Slow down Bro. Try again..."
                )
                return

            game = games[message.guild.id]
            row, col = int(user_input[0]), int(user_input[1])

            if game.board[row][col] != ".":
                await send_embed(
                    ctx=message.channel,
                    title="Position already filled. Try some other coordinate...",
                )
                return

            self.bot_thinking = True
            game.board[row][col] = game.player
            await message.channel.send(game.beautify_board())
            if await self._check_end(message.channel, game, message.guild.id):
                self.bot_thinking = False
                return

            await message.channel.send("Thinking...")
            await self._computer_move(message.channel, game, message.guild.id)
        except ValueError as vale:
            logger.exception(vale)
        except Exception as err:
            logger.exception(err)
            self.bot_thinking = False

    async def _computer_move(self, channel, game, guild_id):
        # run the minimax search off the event loop so the bot stays responsive
        move = await asyncio.to_thread(game.best_move)
        if move:
            game.board[move[0]][move[1]] = game.computer
            await channel.send(game.beautify_board())
            self.bot_thinking = False
            await self._check_end(channel, game, guild_id, computer=True)

    async def _check_end(self, channel, game, guild_id, computer=False) -> bool:
        result = game.hasWon(game.board)
        if result:
            if computer:
                await send_embed(ctx=channel, title="GrandMaster Bro wins! :robot:")
            else:
                await send_embed(
                    ctx=channel,
                    title="Congratulations! Player has won :trophy: :first_place:",
                )
            del games[guild_id]
            return True
        if result is None:
            await send_embed(ctx=channel, title="Match drawn :handshake:")
            del games[guild_id]
            return True
        return False


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Tictactoe(bot))
