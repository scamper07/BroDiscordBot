import asyncio
import datetime
import html
import json
import random

import aiohttp
from discord.ext import commands

from base_logger import logger
from constants import MAX_NO_OF_QUIZ_QUESTIONS, QUIZ_API_URL


class Quiz(commands.Cog):
    """
    Cog to handle a multiplayer trivia quiz game
    """

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.QUIZ_MODE = False
        self.QUIZ_DIFFICULTY = "easy"
        self.QUIZ_MAX_QUESTIONS = 5
        self.QUIZ_QUESTION_WAIT_TIME = 15  # seconds

    async def generate_quiz_question(self):
        """Fetches a single trivia question and shuffled answer options"""
        category = question = correct_answer = ""
        options = []
        try:
            session = aiohttp.ClientSession()
            async with session.get(QUIZ_API_URL.format(self.QUIZ_DIFFICULTY)) as resp:
                json_response = json.loads(await resp.read())
            await session.close()

            result = json_response["results"][0]
            category = result["category"]
            question = result["question"]
            correct_answer = result["correct_answer"]
            options = result["incorrect_answers"].copy()
            options.append(correct_answer)
            random.shuffle(options)
        except Exception as err:
            logger.exception(err)

        return category, question, options, correct_answer

    @commands.hybrid_command(description="Starts a game of quiz")
    async def quiz(self, ctx: commands.Context, arg: str = None) -> None:
        """Starts a game of quiz, or configures it (easy/medium/hard/stop/number)"""
        await self._quiz(ctx, arg)

    async def _quiz(self, ctx: commands.Context, arg: str = None) -> None:
        if not arg or arg == "noinstructions":
            await self._run_quiz(ctx, arg)
        elif arg.lower() == "stop":
            self.QUIZ_MODE = False
            await ctx.send("```Quiz mode stopped```")
        elif arg.lower() in ("easy", "medium", "hard"):
            self.QUIZ_DIFFICULTY = arg.lower()
            await ctx.send(f"```Quiz difficulty set to {arg.lower()}```")
        elif arg.isdigit():
            if int(arg) > MAX_NO_OF_QUIZ_QUESTIONS:
                await ctx.send(
                    "```Quiz: max number of questions cannot be greater than "
                    f"{MAX_NO_OF_QUIZ_QUESTIONS}```"
                )
            else:
                self.QUIZ_MAX_QUESTIONS = int(arg)
                await ctx.send(
                    "```Quiz: max number of questions set to "
                    f"{self.QUIZ_MAX_QUESTIONS}```"
                )

    async def _run_quiz(self, ctx: commands.Context, arg: str) -> None:
        self.QUIZ_MODE = True
        if arg != "noinstructions":
            await ctx.send(
                "```Instructions:\n"
                f"a. There will be a total of {self.QUIZ_MAX_QUESTIONS} questions\n"
                "b. Each question will have 4 options with 100 pts for correct "
                "answer\n"
                "c. To answer, participants have to click on the appropriate "
                "reaction\n"
                "d. Participants have "
                f"{self.QUIZ_QUESTION_WAIT_TIME} seconds to answer each question\n"
                "e. Selecting more than one choice will result in "
                "DISQUALIFICATION\n"
                "f. Participant with the most points is the WINNER!\n```"
            )
            await asyncio.sleep(2)
            await ctx.send("```Game begins in 25 seconds...```")
            await asyncio.sleep(25)

        question_number = 1
        participant_score = {}
        # keycap emojis require the U+FE0F variation selector for Discord reactions
        emojis = [
            f"{num}\N{VARIATION SELECTOR-16}\N{COMBINING ENCLOSING KEYCAP}"
            for num in range(1, 5)
        ]

        while question_number <= self.QUIZ_MAX_QUESTIONS:
            if not self.QUIZ_MODE:
                return

            async with ctx.typing():
                _, question, options, answer = await self.generate_quiz_question()
                if len(options) < 4:
                    await ctx.send("```Could not fetch a question, try again later```")
                    self.QUIZ_MODE = False
                    return
                message = await ctx.send(
                    html.unescape(
                        f"\n**Question {question_number}**\n"
                        f"**{question}**\n"
                        f":one: {options[0]}\n"
                        f":two: {options[1]}\n"
                        f":three: {options[2]}\n"
                        f":four: {options[3]}\n"
                    )
                )
            for emoji in emojis:
                try:
                    await message.add_reaction(emoji)
                except Exception as err:
                    logger.exception(err)
                await asyncio.sleep(0.75)

            participant_response = {}
            target_time = (
                datetime.datetime.today().timestamp() + self.QUIZ_QUESTION_WAIT_TIME
            )
            while datetime.datetime.today().timestamp() < target_time:
                try:
                    reaction, user = await self.bot.wait_for(
                        "reaction_add",
                        timeout=5,
                        check=lambda r, u: str(r.emoji) in emojis,
                    )
                    participant_response[user.display_name] = emojis.index(
                        reaction.emoji
                    )
                except asyncio.TimeoutError:
                    logger.debug("Timeout in Quiz")
                except Exception as err:
                    logger.exception(err)

            await ctx.send(f"Correct answer was **{html.unescape(answer)}**")

            for participant in participant_response:
                if participant == "Bro":
                    continue
                participant_score.setdefault(participant, 0)
                if participant_response[participant] == options.index(answer):
                    participant_score[participant] += 100

            round_score = "".join(
                f"{name}: {score}\n" for name, score in participant_score.items()
            )
            await ctx.send(f"```Score after Round {question_number}\n{round_score}```")
            question_number += 1
            await asyncio.sleep(3)

        logger.debug("quiz complete")
        if participant_score:
            winner = max(participant_score, key=participant_score.get)
            if participant_score[winner] != 0:
                await ctx.send(
                    f"{winner} is the WINNER. Congrats! :trophy: :first_place:"
                )
                return
        await ctx.send("No one scored any points. LOSERS!")


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Quiz(bot))
