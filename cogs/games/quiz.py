import asyncio
import aiohttp
import json
import html
import datetime
import random
from discord.ext import commands
from base_logger import logger


class Quiz(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.QUIZ_MODE = False
        self.QUIZ_DIFFICULTY = "easy"
        self.QUIZ_MAX_QUESTIONS = 5
        self.QUIZ_QUESTION_WAIT_TIME = 15  # seconds

    async def generate_quiz_question(self):
        category = ""
        question = ""
        options = ""
        correct_answer = ""
        try:
            session = aiohttp.ClientSession()
            url = 'https://opentdb.com/api.php?amount=1&category=9&difficulty={}&type=multiple'.format(self.QUIZ_DIFFICULTY)
            async with session.get(url) as resp:
                data = await resp.read()
                json_response = json.loads(data)
            await session.close()

            category = json_response['results'][0]['category']
            question = json_response['results'][0]['question']
            correct_answer = json_response['results'][0]['correct_answer']
            incorrect_answers = json_response['results'][0]['incorrect_answers']

            logger.debug("Category: {}".format(category))
            logger.debug("Question: {}".format(question))
            logger.debug("Answer: {}".format(correct_answer))

            options = incorrect_answers.copy()
            options.append(correct_answer)
            random.shuffle(options)

        except Exception as e:
            logger.exception(e)

        return category, question, options, correct_answer

    @commands.command(brief='Starts a game of quiz')
    async def quiz(self, ctx, arg=None):
        if not arg or arg == "noinstructions":
            self.QUIZ_MODE = True
            if arg != "noinstructions":
                await ctx.send(
                    '```Instructions:\n'
                    'a. There will be a total of {} questions\n'
                    'b. Each question will have 4 options with 100 pts for correct answer\n'
                    'c. To answer, participants have to click on the appropriate reaction\n'
                    'd. Participants have {} seconds to answer each question\n'
                    'e. Selecting more than one choice will result in DISQUALIFICATION\n'
                    'f. Participant with the most points is the WINNER!\n```'.format(self.QUIZ_MAX_QUESTIONS,
                                                                                     self.QUIZ_QUESTION_WAIT_TIME)
                )
                await asyncio.sleep(2)
                await ctx.send('```Game begins in 20 seconds...```')
                await asyncio.sleep(20)

            question_number = 1
            participant_score = {}  # dictionary which stores participant name and score

            while question_number <= self.QUIZ_MAX_QUESTIONS:
                if not self.QUIZ_MODE:
                    # Stop quiz mode
                    return

                async with ctx.typing():
                    category, question, options, answer = await self.generate_quiz_question()
                    message = await ctx.send(html.unescape('\n**Question {}**\n'
                                                           '**{}**\n'
                                                           ':one: {}\n'
                                                           ':two: {}\n'
                                                           ':three: {}\n'
                                                           ':four: {}\n'.format(question_number,
                                                                                question,
                                                                                options[0],
                                                                                options[1],
                                                                                options[2],
                                                                                options[3]
                                                                                )))
                emojis = ["{}\N{COMBINING ENCLOSING KEYCAP}".format(num) for num in
                          range(1, 5)]  # emoji code for 1,2,3,4
                for emoji in emojis:
                    await message.add_reaction(emoji)
                    await asyncio.sleep(.75)

                participant_response = {}  # dictionary to record user response

                # Give participants some time to react before moving on to next question
                time_at_start = datetime.datetime.today().timestamp()
                target_time = time_at_start + self.QUIZ_QUESTION_WAIT_TIME  # wait for QUIZ_QUESTION_WAIT_TIME seconds for response

                logger.debug("time_at_start {}".format(time_at_start))
                logger.debug("target_time {}".format(target_time))

                while datetime.datetime.today().timestamp() < target_time:
                    logger.debug("while now {}".format(datetime.datetime.today().timestamp()))
                    try:
                        reaction, user = await self.bot.wait_for('reaction_add', timeout=5,
                                                                 check=lambda reaction1, user1: str(
                                                                     reaction1.emoji) in emojis)
                        logger.debug("{} reacted with {}".format(user.display_name, reaction))
                        # TODO: remove older reaction if user changes option
                        # message.remove_reaction(participant_response[user], user)
                        participant_response.update({user.display_name: emojis.index(reaction.emoji)})
                    except asyncio.TimeoutError:
                        logger.debug("Timeout in Quiz")
                    except Exception as e:
                        logger.exception(e)

                await ctx.send("Correct answer was **{}**".format(html.unescape(answer)))

                for participant in participant_response:
                    if participant == "Bro":
                        continue

                    if participant not in participant_score:
                        participant_score.update({participant: 0})

                    if participant_response[participant] == options.index(answer):
                        logger.debug("Updating score for {}".format(participant))
                        participant_score.update({participant: participant_score[participant] + 100})

                # show round score
                round_score = ""
                for participant in participant_score:
                    round_score += "{}: {}\n".format(participant, participant_score[participant])
                await ctx.send("```Score after Round {}\n{}```".format(question_number, round_score))
                question_number += 1
                await asyncio.sleep(3)

            logger.debug("quiz complete")
            winner = max(participant_score, key=participant_score.get)
            if participant_score[winner] != 0:
                await ctx.send("{} is the WINNER. Congrats! :trophy: :first_place:".format(winner))
            else:
                await ctx.send("No one scored any points. LOSERS!")

        elif arg.lower() == "stop":
            self.QUIZ_MODE = False
            await ctx.send('```Quiz mode stopped```')
        elif arg.lower() == "easy":
            self.QUIZ_DIFFICULTY = "easy"
            await ctx.send('```Quiz difficulty set to easy```')
        elif arg.lower() == "medium":
            self.QUIZ_DIFFICULTY = "medium"
            await ctx.send('```Quiz difficulty set to medium```')
        elif arg.lower() == "hard":
            self.QUIZ_DIFFICULTY = "hard"
            await ctx.send('```Quiz difficulty set to hard```')
        elif arg.isdigit():
            if int(arg) > 30:
                await ctx.send('```Quiz: max number of questions cannot be greater than 30```')
            else:
                self.QUIZ_MAX_QUESTIONS = int(arg)
                await ctx.send('```Quiz: max number of questions set to {}```'.format(self.QUIZ_MAX_QUESTIONS))
        else:
            # TODO: add option to change quiz config settings
            # number of questions
            # mode : easy, medium, hard
            # delay: ?
            pass


def setup(bot):
    bot.add_cog(Quiz(bot))
