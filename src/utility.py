import discord


async def send_embed(
    self,
    ctx,
    embed: discord.Embed = None,
    title=None,
    description=None,
    url=None,
    color=discord.Colour.purple(),
    image_url=None,
    dm=False,
):
    """Function to send custom embed with default properties"""

    if not embed:
        embed = discord.Embed(
            title=title, description=description, color=color, url=url
        )

    embed.set_image(url=image_url)
    embed.set_footer(text=f"Powered by discord.py v{discord.__version__}")
    if not dm:
        await ctx.send(embed=embed)
    else:
        await ctx.author.send(embed=embed)
