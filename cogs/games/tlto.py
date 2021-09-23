import asyncio
from discord.ext import commands


class Tlto(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.organizer = None
        self.is_game_running = False
        self.is_pounce_enabled = False
        self.emojis = ["{}\N{COMBINING ENCLOSING KEYCAP}".format(num) for num in
                          range(1, 5)]
        self.organizer_dm = ""
        self.pounce_answers_counter = 0
        pass

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
                    messages = await ctx.channel.history(limit=(self.pounce_answers_counter+1)).flatten()
                    for message in messages:
                        if message == ".pounce":
                            continue

                        print(message.content)
                        emoji = ""
                        for reaction in message.reactions:
                            if reaction.count == 2:
                                emoji = reaction.emoji

                        print(emoji)
                        # Check if emoji is tick or cross
                        # Calculate scores for people who answered
                        # Get people who did not answer and print names one by one with the same reaction emojis
                        # Organizer now turn by turn will look for the answer
                        # When a person gives the right answer
                        # Organizer has to react to that person's emoji
                        # Question is now closed

                    # read messages and reactions from the organizer - bot dm
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

def setup(bot):
    bot.add_cog(Tlto(bot))