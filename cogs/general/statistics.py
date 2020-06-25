import discord
from discord.ext import commands
from config import stats_brief, COMMAND_PREFIX
from base_logger import logger
from collections import Counter


class Statistics(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(brief=stats_brief, description='Shows stats for server or members')
    async def stats(self, ctx, user: discord.Member = None):
        wait_message = await ctx.send("Processing... Please wait. This might take sometime")
        async with ctx.typing():
            if not user:
                embed = discord.Embed(
                    title="Stats",
                    description="Showing random stats for this server",
                    colour=discord.Color.blue()
                )
                embed.set_footer(text="Hope that was helpful, bye!")
                embed.set_author(name="Bro Bot", icon_url=self.bot.user.avatar_url)
                embed.set_thumbnail(url=ctx.guild.icon_url)

                server = ctx.message.author.guild
                server_name = server.name
                server_owner = server.owner.mention
                server_create_date = server.created_at.__format__('%d/%B/%Y')
                server_member_count = server.member_count
                logger.debug("*****************************")
                logger.debug(
                    "Server name: {}\nserver owner: {}\nserver created at: {}\nTotal number of members: {}".format(
                        server_name,
                        server_owner,
                        server_create_date,
                        server_member_count)
                )
                embed.add_field(name="Server Name", value=server_name, inline=False)
                embed.add_field(name="Server Owner", value=server_owner, inline=True)
                embed.add_field(name="Server Create Date", value=server_create_date, inline=True)
                embed.add_field(name="Total Members", value=server_member_count, inline=True)

                # channel = bot.get_channel(GENERAL_CHANNEL_ID)
                # messages = await channel.history(limit=None).flatten()
                messages = await ctx.channel.history(limit=None).flatten()
                logger.debug("Total messages: {}".format(len(messages)))
                embed.add_field(name="Total messages", value=str(len(messages)), inline=False)
                authors_count = Counter()
                word_count = Counter()
                message_list = list()
                bro_in_message_count = 0
                for message in messages:
                    if "bro" in str(message.content).lower():
                        bro_in_message_count += 1
                    authors_count.update({message.author.name: 1})
                    message_list += str(message.content).split()
                word_count.update(message_list)

                top = authors_count.most_common(1)
                logger.debug("Most talkative bro: {} talked {} times".format(top[0][0], top[0][1]))
                value = str(top[0][0] if ctx.guild.get_member_named(top[0][0]) is None else ctx.guild.get_member_named(
                    top[0][0]).mention) + " (" + str(top[0][1]) + " messages)"
                logger.debug(value)
                embed.add_field(name="Most Talkative Bro", value=value, inline=False)

                low = min(authors_count, key=authors_count.get)
                logger.debug("Least talkative bro: {} talked {} time(s)".format(low, authors_count[low]))
                value = str(low if ctx.guild.get_member_named(low) is None else ctx.guild.get_member_named(
                    low).mention) + " (" + str(authors_count[low]) + " messages)"
                embed.add_field(name="Least Talkative Bro", value=value, inline=True)

                top_authors = ""
                if len(authors_count) >= 5:
                    logger.debug("Top 5 talkative Bros")
                    for author, message_count in authors_count.most_common(5):
                        logger.debug("{}: {} times".format(author, message_count))
                        top_authors += str(
                            author if ctx.guild.get_member_named(author) is None else ctx.guild.get_member_named(
                                author).mention) + " (" + str(message_count) + " messages) \n"

                embed.add_field(name="Top 5 Talkative Bros", value=top_authors, inline=False)

                top_string = ""
                if len(word_count) >= 5:
                    logger.debug("Top five words used here are:")
                    for word, count in word_count.most_common(5):
                        logger.debug("{}: {} times".format(word, count))
                        top_string += str(word) + " (" + str(count) + " times) \n"

                embed.add_field(name="Top 5 words used here", value=top_string, inline=False)

                logger.debug("Bro was mentioned {} times!".format(bro_in_message_count))
                embed.add_field(name="Bro Count", value=str(bro_in_message_count), inline=False)

                logger.debug("*****************************")
            else:
                embed = discord.Embed(
                    title="Stats",
                    description="Showing random stats for user",
                    colour=discord.Color.purple()
                )
                embed.set_footer(text="Hope that was helpful, bye!")
                embed.set_author(name="Bro Bot", icon_url=self.bot.user.avatar_url)
                embed.set_thumbnail(url=user.avatar_url)

                logger.debug("*****************************")
                logger.debug("user name: {}".format(user.mention))
                logger.debug("user join date: {}".format(user.joined_at.__format__('%d/%B/%Y @%H:%M:%S')))
                embed.add_field(name="User Name", value=user.mention, inline=False)
                embed.add_field(name="User Join Date", value=user.joined_at.__format__('%d/%B/%Y'), inline=False)

                messages = await ctx.channel.history(limit=None).flatten()
                message_list = list()
                word_count = Counter()
                for message in messages:
                    if user == message.author:
                        message_list += str(message.content).split()

                word_count.update(message_list)
                top_string = ""
                if len(word_count) >= 5:
                    logger.debug("Top five words used by {}:".format(user.display_name))
                    top_name = "Top 5 words used by {} in this server:".format(user.display_name)
                    for word, count in word_count.most_common(5):
                        logger.debug("{}: {} times".format(word, count))
                        top_string += str(word) + " (" + str(count) + " times) \n"

                    embed.add_field(name=top_name, value=top_string, inline=False)
                logger.debug("*****************************")

        await wait_message.delete()
        await ctx.send(embed=embed)

    @stats.error
    async def info_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send('```Member not found...```')
            await ctx.send(
                '```Command usage:\n {}stats  : for server stats\n {}stats <username> : for user stats```'.format(
                    COMMAND_PREFIX, COMMAND_PREFIX))


def setup(bot):
    bot.add_cog(Statistics(bot))
