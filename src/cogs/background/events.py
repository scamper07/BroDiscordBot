import discord
from discord.ext import commands
from base_logger import logger


class Events(commands.Cog):
    """
    Cog to handle global events (messages)
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        await self.bot.change_presence(
            status=discord.Status.online,
            activity=discord.Activity(
                type=discord.ActivityType.listening,
                name=".help",
            ),
        )
        logger.info("Bot is online!")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        full_message = message.content.lower().split()

        if "bro" in full_message:
            logger.debug("Sending Bro")
            await message.channel.send("# Bro")

        if "hello" in full_message or "hi" in full_message:
            logger.debug("Sending hello")
            await message.channel.send(f"Hello {message.author.mention} bro")

        if "bye" in full_message:
            logger.debug("Sending bye")
            await message.channel.send(f"Bye Bye {message.author.mention} bro")
            await message.author.send("👋")


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Events(bot))
