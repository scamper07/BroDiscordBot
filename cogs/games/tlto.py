import asyncio
import collections
import discord

from discord.ext import commands
from base_logger import logger
from table2ascii import table2ascii, Alignment, PresetStyle
from utils import embed_send

EMOJI_RIGHT_ANSWER = "✅"
EMOJI_WRONG_ANSWER = "❌"


class Tlto(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.organizer = None
        self.is_game_running = False
        self.is_pounce_enabled = False
        self.is_round_robin_enabled = False
        self.emojis = [EMOJI_RIGHT_ANSWER, EMOJI_WRONG_ANSWER]
        self.organizer_dm = ""
        self.pounce_answers_counter = 0
        self.current_scores = collections.defaultdict(int)
        self.players = set()
        self.quiz_guild_id = ""
        self.quiz_score_channel_id = ""
        self.who_pounced = set()
        self.score_message = None

    @commands.command(brief="Start quiz")
    @commands.has_role("Organizer")
    async def tlto(self, ctx):
        # Make caller the organizer
        self.organizer = ctx.author.id
        self.is_game_running = True
        self.quiz_guild_id = ctx.guild.id
        self.quiz_score_channel_id = ctx.channel.id
        embed = discord.Embed(title="Welcome to Tell Like That Only Quiz!",
                              description="Instructions:\n"
                                          "1. When QM enables Pounce, DM the answer to Bro Bot\n"
                                          "2. Pounces after QM closes will be discarded\n"
                                          "3. Answers in Direct Round should be to told to QM on your turn ")
        await embed_send(ctx, embed)

    @commands.command(aliases=["p"], brief="Toggle pounce")
    async def pounce(self, ctx):
        if ctx.author.id == self.organizer:
            if self.is_game_running:
                message_channel = self.bot.get_channel(self.quiz_score_channel_id)
                if self.is_pounce_enabled:
                    self.is_pounce_enabled = False
                    # await message_channel.send("Pounce Disabled!")
                    embed = discord.Embed(title="Pounce Disabled!\nDirect Round begins!")
                    await embed_send(message_channel, embed)
                    # pounce was turned off
                    messages = await ctx.channel.history(limit=(self.pounce_answers_counter + 1)).flatten()
                    scores = self.score_round(messages)
                    # Normal round scoring ? wait ?
                    self.score(scores)
                    await self.print_score_table()
                    await self.round_robin()
                else:
                    self.is_pounce_enabled = True
                    print("Pounce enabled")
                    self.who_pounced = set()
                    self.pounce_answers_counter = 0
                    embed = discord.Embed(title="Pounce Enabled!")
                    await embed_send(message_channel, embed)

    @commands.command(aliases=["sup"], brief="Signup participants for TLTO Quiz")
    @commands.has_role("Organizer")
    async def signup(self, ctx, *args):
        self.players = set(args[1:])
        # init scores with zero
        for name in self.players:
            self.current_scores[name] = 0
        embed = discord.Embed(title="Done!")
        await embed_send(ctx, embed)
        await self.print_score_table()

    @commands.command(aliases=["us"], brief="update score for a participant(ADMIN USE ONLY)")
    @commands.has_role("Organizer")
    async def updatescore(self, ctx, *args):
        if self.is_game_running:
            if args:
                self.current_scores[args[0]] += int(args[1])
                embed = discord.Embed(title="Done!")
                await embed_send(ctx, embed)
                await self.print_score_table()
            else:
                embed = discord.Embed(title="Usage:",
                                      description="updatescore name score\n"
                                                  "Ex: updatescore john 10")
                await embed_send(ctx, embed)

    @commands.Cog.listener()
    async def on_message(self, message):
        # logger.debug(message.content)

        if message.author == self.bot.user:
            return
        if message.guild:
            # Ignore messages from server
            return
        if message.content == ".pounce" or message.content == ".p" and message.author.id == self.organizer:
            return
        if self.is_game_running:
            if self.is_pounce_enabled:
                self.pounce_answers_counter += 1
                u_organizer = self.bot.get_user(self.organizer)
                user_m = await u_organizer.send(message.author.name + " : " + message.content)
                self.who_pounced.add(message.author.name)
                await asyncio.sleep(.75)
                for emoji in self.emojis:
                    await user_m.add_reaction(emoji)
                    # TODO :: check if we can get hold of click events on emoji to notify if the sender of this
                    #  message was right or wrong
                    await asyncio.sleep(.75)

    async def round_robin(self):
        # List all the players who did not pounce
        players = self.players - self.who_pounced
        u_organizer = self.bot.get_user(self.organizer)
        embed = discord.Embed(title="Participants who haven't pounced :point_down: !")
        await embed_send(u_organizer, embed)

        for player in players:
            user_m = await u_organizer.send(player)
            # React with just a tick
            await user_m.add_reaction(self.emojis[0])

        await u_organizer.send("=================================")
        self.is_round_robin_enabled = True

        # On click of a tick score for that particular person
        # (Optional)
        # If the QM made a mistake checking the wrong person, he is allowed to tick another person
        # The latest tick before the next pounce will be considered for the score.
        # (/ Optional)
        # Update and print scores

    def score(self, scores):
        # TODO :: add to final score
        # Calculate total score
        # Update score table

        for name in scores:
            self.current_scores[name] += scores[name]

    def score_round(self, messages):
        scores = collections.defaultdict(int)
        messages.reverse()
        for message in messages:
            if message == ".pounce" or message == ".p":
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

    async def print_score_table(self):
        players_list = []
        scores_list = []

        for name, score in self.current_scores.items():
            players_list.append(name.strip())
            scores_list.append(str(score))

        if players_list:
            output = table2ascii(
                header=players_list,
                body=[scores_list],
                style=PresetStyle.double_box
            )

            message_channel = self.bot.get_channel(self.quiz_score_channel_id)

            '''
            if not self.score_message:
                self.score_message = await message_channel.send("```{}```".format(output))
            else:
                await self.score_message.edit(content="```{}```".format(output))
            '''
            # embed = discord.Embed(title="Score Table:",
            #                       description="```{}```".format(output))
            # await embed_send(message_channel, embed)
            await message_channel.send("```Score Table:\n{}```".format(output))

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if self.is_game_running:
            if self.is_round_robin_enabled:
                if user.id == self.organizer:
                    if reaction.emoji == EMOJI_RIGHT_ANSWER:
                        if reaction.count == 2:
                            name = reaction.message.content
                            self.current_scores[name] += 10
                            self.is_round_robin_enabled = False
                            await self.print_score_table()

            elif self.is_pounce_enabled:
                if user.id == self.organizer:
                    contestant_score = reaction.message.content.split(":")
                    guild = self.bot.get_guild(self.quiz_guild_id)
                    logger.debug(guild)
                    user = discord.utils.find(lambda m: m.name == contestant_score[0].strip(), guild.members)
                    logger.debug(user)
                    if reaction.emoji == EMOJI_RIGHT_ANSWER:
                        if reaction.count == 2:
                            # send message saying correct answer
                            embed = discord.Embed(title="Correct answer!")
                            await embed_send(user, embed)
                            # await user.send("Correct answer!")

                    elif reaction.emoji == EMOJI_WRONG_ANSWER:
                        if reaction.count == 2:
                            # await user.send("Wrong answer!")
                            embed = discord.Embed(title="Wrong answer!")
                            await embed_send(user, embed)


def setup(bot):
    bot.add_cog(Tlto(bot))
