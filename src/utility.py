import discord

from constants import BOT_NAME


async def send_embed(
    self,
    ctx,
    embed: discord.Embed = None,
    title=None,
    description=None,
    url=None,
    color=discord.Colour.purple(),
    image_url=None,
):
    """Function to send custom embed with default properties"""

    if not embed:
        embed = discord.Embed(
            title=title, description=description, color=color, url=url
        )

    embed.set_image(url=image_url)
    embed.set_author(name=BOT_NAME, icon_url=self.bot.user.avatar.url)
    embed.set_footer(text=f"Powered by discord.py v{discord.__version__}")
    await ctx.send(embed=embed)
