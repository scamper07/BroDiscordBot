from collections import Counter

import discord
import nltk
from discord.ext import commands
from nltk.corpus import stopwords

from base_logger import logger
from constants import ADDITIONAL_STOPWORDS, BOT_NAME
from utility import send_embed

# download the stopwords corpus once, only if it isn't already available
try:
    stopwords.words("english")
except LookupError:
    nltk.download("stopwords", quiet=True)


class Statistics(commands.Cog):
    """
    Cog to handle server and user statistics
    """

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.hybrid_command(description="Shows stats for the server or a member")
    async def stats(self, ctx: commands.Context, user: discord.Member = None) -> None:
        """Shows random stats about the server, or a user when one is given"""
        async with ctx.typing():
            await self._stats(ctx, user)

    async def _stats(self, ctx: commands.Context, user: discord.Member) -> None:
        try:
            wait_message = await ctx.send(
                "Processing... Please wait. This might take sometime"
            )
            if not user:
                embed = await self._server_stats(ctx)
            else:
                embed = await self._user_stats(ctx, user)

            await wait_message.delete()
            await send_embed(ctx=ctx, embed=embed)
        except Exception as err:
            logger.exception(err)

    async def _server_stats(self, ctx: commands.Context) -> discord.Embed:
        embed = discord.Embed(
            title="Stats",
            description="Showing random stats for this server",
            colour=discord.Color.blue(),
        )
        embed.set_footer(text="Hope that was helpful, bye!")
        embed.set_author(name=BOT_NAME, icon_url=self.bot.user.display_avatar.url)
        if ctx.guild.icon:
            embed.set_thumbnail(url=ctx.guild.icon.url)

        server = ctx.guild
        embed.add_field(name="Server Name", value=server.name, inline=False)
        embed.add_field(name="Server Owner", value=server.owner.mention, inline=True)
        embed.add_field(
            name="Server Create Date",
            value=server.created_at.__format__("%d/%B/%Y"),
            inline=True,
        )
        embed.add_field(name="Total Members", value=server.member_count, inline=True)

        messages = [message async for message in ctx.channel.history(limit=None)]
        embed.add_field(
            name="Total messages in this channel",
            value=str(len(messages)),
            inline=False,
        )

        authors_count = Counter()
        word_count = Counter()
        message_list = []
        bro_in_message_count = 0

        full_stopwords = stopwords.words("english")
        full_stopwords.extend(ADDITIONAL_STOPWORDS)
        for message in messages:
            if "bro" in str(message.content).lower():
                bro_in_message_count += 1
            authors_count.update({message.author.name: 1})
            filtered_words = [
                word for word in message.content.split() if word not in full_stopwords
            ]
            message_list += filtered_words
        word_count.update(message_list)

        if authors_count:
            top = authors_count.most_common(1)
            embed.add_field(
                name="Most Talkative Bro",
                value=self._member_value(ctx, top[0][0], top[0][1]),
                inline=False,
            )

            low = min(authors_count, key=authors_count.get)
            embed.add_field(
                name="Least Talkative Bro",
                value=self._member_value(ctx, low, authors_count[low]),
                inline=True,
            )

        if len(authors_count) >= 5:
            top_authors = ""
            for author, message_count in authors_count.most_common(5):
                top_authors += self._member_value(ctx, author, message_count) + "\n"
            embed.add_field(
                name="Top 5 Talkative Bros", value=top_authors, inline=False
            )

        if len(word_count) >= 5:
            top_string = ""
            for word, count in word_count.most_common(5):
                top_string += f"{word} ({count} times) \n"
            embed.add_field(
                name="Top 5 words used here", value=top_string, inline=False
            )

        embed.add_field(name="Bro Count", value=str(bro_in_message_count), inline=False)
        return embed

    async def _user_stats(
        self, ctx: commands.Context, user: discord.Member
    ) -> discord.Embed:
        embed = discord.Embed(
            title="Stats",
            description="Showing random stats for user",
            colour=discord.Color.purple(),
        )
        embed.set_footer(text="Hope that was helpful, bye!")
        embed.set_author(name=BOT_NAME, icon_url=self.bot.user.display_avatar.url)
        embed.set_thumbnail(url=user.display_avatar.url)

        embed.add_field(name="User Name", value=user.mention, inline=False)
        embed.add_field(
            name="User Join Date",
            value=user.joined_at.__format__("%d/%B/%Y"),
            inline=False,
        )

        messages = [message async for message in ctx.channel.history(limit=None)]
        message_list = []
        for message in messages:
            if user == message.author:
                message_list += str(message.content).split()

        word_count = Counter()
        word_count.update(message_list)
        if len(word_count) >= 5:
            top_string = ""
            for word, count in word_count.most_common(5):
                top_string += f"{word} ({count} times) \n"
            embed.add_field(
                name=f"Top 5 words used by {user.display_name} in this server:",
                value=top_string,
                inline=False,
            )
        return embed

    @staticmethod
    def _member_value(ctx: commands.Context, name: str, count: int) -> str:
        """Render a member mention (or raw name) with their message count"""
        member = ctx.guild.get_member_named(name)
        display = member.mention if member else name
        return f"{display} ({count} messages)"


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Statistics(bot))
