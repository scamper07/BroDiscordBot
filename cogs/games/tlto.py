import asyncio
import collections

from discord.ext import commands

EMOJI_RIGHT_ANSWER = "✅"
EMOJI_WRONG_ANSWER = "❌"


class Tlto(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.organizer = None
        self.is_game_running = False
        self.is_pounce_enabled = False
        self.emojis = [EMOJI_RIGHT_ANSWER, EMOJI_WRONG_ANSWER]
        self.organizer_dm = ""
        self.pounce_answers_counter = 0
        self.current_scores = collections.defaultdict(int)

    @commands.command(brief="Start quiz")
    @commands.has_role("Organizer")
    async def tlto(self, ctx):
        # TODO :: From PESIT server
        # Make caller the organizer
        self.organizer = ctx.author.id
        self.is_game_running = True

    @commands.command(brief="Toggle pounce")
    async def pounce(self, ctx):
        if ctx.author.id == self.organizer:
            if self.is_game_running:
                if self.is_pounce_enabled:
                    self.is_pounce_enabled = False
                    # pounce was turned off
                    messages = await ctx.channel.history(limit=(self.pounce_answers_counter + 1)).flatten()
                    scores = self.score_round(messages)
                    # Normal round scoring ? wait ?
                    res = self.score(scores)
                    await ctx.send(res)
                else:
                    self.is_pounce_enabled = True
                    print("Pounce enabled")
                    self.pounce_answers_counter = 0

    @commands.Cog.listener()
    async def on_message(self, message):
        # logger.debug(message.content)

        if message.author == self.bot.user:
            return
        if message.guild:
            # Ignore messages from server
            return
        if message.content == ".pounce" and message.author.id == self.organizer:
            return
        if self.is_game_running:
            if self.is_pounce_enabled:
                self.pounce_answers_counter += 1
                u_organizer = self.bot.get_user(self.organizer)
                user_m = await u_organizer.send(message.author.name + " : " + message.content)
                await asyncio.sleep(.75)
                for emoji in self.emojis:
                    await user_m.add_reaction(emoji)
                    await asyncio.sleep(.75)

    def score(self, scores):
        # TODO :: add to final score
        # Calculate total score
        # Update score table
        res = ""
        for name in scores:
            self.current_scores[name] += scores[name]
            res += name + " : " + str(self.current_scores[name]) + "\n"
        return res

    def score_round(self, messages):
        scores = collections.defaultdict(int)
        messages.reverse()
        for message in messages:
            if message == ".pounce":
                continue
            print(message.content)
            emoji = ""
            for reaction in message.reactions:
                if reaction.count == 2:
                    emoji = reaction.emoji
            contestant_score = message.content.split(":")
            if emoji == EMOJI_RIGHT_ANSWER:
                scores[contestant_score[0]] = 10
            elif emoji == EMOJI_WRONG_ANSWER:
                scores[contestant_score[0]] = -5
            else:
                pass
            print(emoji)
        return scores


def setup(bot):
    bot.add_cog(Tlto(bot))
