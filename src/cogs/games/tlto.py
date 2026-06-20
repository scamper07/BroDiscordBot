import asyncio
import collections

import discord
from discord.ext import commands
from table2ascii import table2ascii, PresetStyle

from utility import send_embed

EMOJI_RIGHT_ANSWER = "✅"
EMOJI_WRONG_ANSWER = "❌"


class Tlto(commands.Cog):
    """
    Cog to run a "Tell Like That Only" pounce-style quiz
    """

    def __init__(self, bot: commands.Bot) -> None:
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
    async def tlto(self, ctx: commands.Context) -> None:
        """Starts the TLTO quiz and makes the caller the organizer"""
        self.organizer = ctx.author.id
        self.is_game_running = True
        self.quiz_guild_id = ctx.guild.id
        self.quiz_score_channel_id = ctx.channel.id
        await send_embed(
            ctx=ctx,
            title="Welcome to Tell Like That Only Quiz!",
            description=(
                "Instructions:\n"
                "1. When QM enables Pounce, DM the answer to Bro Bot\n"
                "2. Pounces after QM closes will be discarded\n"
                "3. Answers in Direct Round should be told to QM on your turn "
            ),
        )

    @commands.command(aliases=["p"], brief="Toggle pounce")
    async def pounce(self, ctx: commands.Context) -> None:
        """Toggles pounce mode on or off (organizer only)"""
        if ctx.author.id != self.organizer or not self.is_game_running:
            return
        message_channel = self.bot.get_channel(self.quiz_score_channel_id)
        if self.is_pounce_enabled:
            self.is_pounce_enabled = False
            await send_embed(
                ctx=message_channel,
                title="Pounce Disabled!\nDirect Round begins!",
            )
            messages = [
                msg
                async for msg in ctx.channel.history(
                    limit=(self.pounce_answers_counter + 1)
                )
            ]
            scores = self.score_round(messages)
            self.score(scores)
            await self.print_score_table()
            await self.round_robin()
        else:
            self.is_pounce_enabled = True
            self.who_pounced = set()
            self.pounce_answers_counter = 0
            await send_embed(ctx=message_channel, title="Pounce Enabled!")

    @commands.command(aliases=["sup"], brief="Signup participants for TLTO Quiz")
    @commands.has_role("Organizer")
    async def signup(self, ctx: commands.Context, *args) -> None:
        """Signs up participants for the quiz"""
        self.players = set(args[1:])
        for name in self.players:
            self.current_scores[name] = 0
        await send_embed(ctx=ctx, title="Done!")
        await self.print_score_table()

    @commands.command(aliases=["us"], brief="update score for a participant")
    @commands.has_role("Organizer")
    async def updatescore(self, ctx: commands.Context, *args) -> None:
        """Updates the score for a participant (organizer only)"""
        if not self.is_game_running:
            return
        if args:
            self.current_scores[args[0]] += int(args[1])
            await send_embed(ctx=ctx, title="Done!")
            await self.print_score_table()
        else:
            await send_embed(
                ctx=ctx,
                title="Usage:",
                description="updatescore name score\nEx: updatescore john 10",
            )

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return
        if message.guild:
            # only consider DMs as pounce answers
            return
        if (
            message.content == ".pounce"
            or message.content == ".p"
            and message.author.id == self.organizer
        ):
            return
        if self.is_game_running and self.is_pounce_enabled:
            self.pounce_answers_counter += 1
            u_organizer = self.bot.get_user(self.organizer)
            user_m = await u_organizer.send(
                message.author.name + " : " + message.content
            )
            self.who_pounced.add(message.author.name)
            await asyncio.sleep(0.75)
            for emoji in self.emojis:
                await user_m.add_reaction(emoji)
                await asyncio.sleep(0.75)

    async def round_robin(self):
        players = self.players - self.who_pounced
        u_organizer = self.bot.get_user(self.organizer)
        await send_embed(
            ctx=u_organizer,
            title="Participants who haven't pounced :point_down: !",
        )
        for player in players:
            user_m = await u_organizer.send(player)
            await user_m.add_reaction(self.emojis[0])
        await u_organizer.send("=================================")
        self.is_round_robin_enabled = True

    def score(self, scores):
        for name in scores:
            self.current_scores[name] += scores[name]

    def score_round(self, messages):
        scores = collections.defaultdict(int)
        messages.reverse()
        for message in messages:
            if message == ".pounce" or message == ".p":
                continue
            emoji = ""
            for reaction in message.reactions:
                if reaction.count == 2:
                    emoji = reaction.emoji
            contestant_score = message.content.split(":")
            if emoji == EMOJI_RIGHT_ANSWER:
                scores[contestant_score[0]] = 10
            elif emoji == EMOJI_WRONG_ANSWER:
                scores[contestant_score[0]] = -5
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
                style=PresetStyle.double_box,
            )
            message_channel = self.bot.get_channel(self.quiz_score_channel_id)
            await message_channel.send(f"```Score Table:\n{output}```")

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if not self.is_game_running:
            return

        if self.is_round_robin_enabled:
            if user.id == self.organizer and reaction.emoji == EMOJI_RIGHT_ANSWER:
                if reaction.count == 2:
                    name = reaction.message.content
                    self.current_scores[name] += 10
                    self.is_round_robin_enabled = False
                    await self.print_score_table()
        elif self.is_pounce_enabled and user.id == self.organizer:
            contestant_score = reaction.message.content.split(":")
            guild = self.bot.get_guild(self.quiz_guild_id)
            member = discord.utils.find(
                lambda m: m.name == contestant_score[0].strip(), guild.members
            )
            if reaction.count == 2:
                if reaction.emoji == EMOJI_RIGHT_ANSWER:
                    await send_embed(ctx=member, title="Correct answer!")
                elif reaction.emoji == EMOJI_WRONG_ANSWER:
                    await send_embed(ctx=member, title="Wrong answer!")


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Tlto(bot))
