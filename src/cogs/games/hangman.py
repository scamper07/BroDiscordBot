from discord.ext import commands

from constants import (
    EMOJI_COAT,
    EMOJI_DIZZY_FACE,
    EMOJI_HANGMAN_ROPE,
    EMOJI_JEANS,
    EMOJI_POINT_FINGER_UP,
    EMOJI_QUESTION_MARK,
    STR_ABORT_SUCCESS,
    STR_ALREADY_PLAYING,
    STR_GAME_OVER,
    STR_GET_WORD,
    STR_GUESSED_SO_FAR,
    STR_NO_GAME,
    STR_TRY_HANGMAN,
    STR_WORD_EMPTY,
    STR_YOU_LOST,
    STR_YOU_WON,
)


class HM:
    """Manages one instance of a Hangman game at a given time"""

    def __init__(self, server_id, channel_id, challenger):
        self.server_id = server_id
        self.channel_id = channel_id
        self.challenger = challenger
        self.accepting_letters = False
        self.is_game_over = False
        self.has_player_won = False
        self.truth = None
        self.guessed_letters = []
        self.wrong_answers = 0
        self.blanks = []
        self.hangman_status = ""
        self.print_list = [
            EMOJI_HANGMAN_ROPE,
            ".     " + EMOJI_DIZZY_FACE,
            "." + EMOJI_POINT_FINGER_UP,
            EMOJI_COAT,
            EMOJI_POINT_FINGER_UP,
            " .     " + EMOJI_JEANS,
        ]

    def process_input(self, letter):
        if self.is_game_over:
            return
        if letter.upper() in self.truth:
            self.update_blanks(letter)
        else:
            self.wrong_answers += 1
            self.update_hangman_status(self.wrong_answers)
        if letter.upper() not in self.guessed_letters and letter != "":
            self.guessed_letters.append(letter.upper())

    def update_blanks(self, letter):
        if letter == "":
            for _ in self.truth:
                self.blanks.append(EMOJI_QUESTION_MARK)
        else:
            for i, l in enumerate(self.truth):
                if l.upper() == letter.upper():
                    self.blanks[i] = letter.upper()
        if self.blanks == list(self.truth):
            self.is_game_over = True
            self.has_player_won = True

    def update_hangman_status(self, wrong_answers):
        # arms and body need to be on a straight line, hence no newline for 3 and 4
        if wrong_answers == 3 or wrong_answers == 4:
            self.hangman_status += self.print_list[wrong_answers - 1]
        else:
            self.hangman_status += self.print_list[wrong_answers - 1] + "\n"
        if self.wrong_answers == len(self.print_list):
            self.is_game_over = True
            self.has_player_won = False

    def get_game_status(self):
        result_string = ""
        if self.is_game_over:
            result_string += STR_GAME_OVER
            if self.has_player_won:
                result_string += STR_YOU_WON
            else:
                result_string += STR_YOU_LOST + "\n" + "The word was " + self.truth
        else:
            result_string = STR_GUESSED_SO_FAR
            for guess in self.guessed_letters:
                result_string += guess.upper() + " , "

        blanks = ""
        for b in self.blanks:
            blanks += b + "\t"
        return "\n" + blanks + " \n" + self.hangman_status + "\n" + result_string


class Hangman(commands.Cog):
    """
    Cog to handle a game of Hangman
    """

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.game_instances = {}
        self.challenger_to_server_dict = {}
        self.server_id_to_challenger = {}

    @commands.hybrid_command(description="Starts a game of Hangman")
    async def hangman(self, ctx: commands.Context) -> None:
        """Starts a game of Hangman, the challenger is DMed for the secret word"""
        server_id = ctx.guild.id
        channel_id = ctx.channel
        challenger = ctx.author.id
        if server_id in self.game_instances:
            await ctx.channel.send(STR_ALREADY_PLAYING)
            return
        self.game_instances[server_id] = HM(server_id, channel_id, challenger)
        user = self.bot.get_user(challenger)
        self.challenger_to_server_dict[challenger] = server_id
        self.server_id_to_challenger[server_id] = challenger
        await user.send(STR_GET_WORD)

    @commands.hybrid_command(description="Sets the secret word for Hangman")
    async def word(self, ctx: commands.Context, word: str = "") -> None:
        """Sets the secret word for the ongoing Hangman game (sent via DM)"""
        challenger = ctx.author.id
        if challenger not in self.challenger_to_server_dict:
            await ctx.channel.send(STR_TRY_HANGMAN)
            return
        server_id = self.challenger_to_server_dict[challenger]
        hm_instance = self.game_instances[server_id]
        if word == "":
            await ctx.channel.send(STR_WORD_EMPTY)
            return
        hm_instance.accepting_letters = True
        hm_instance.truth = word.upper()
        hm_instance.process_input("")
        await hm_instance.channel_id.send(hm_instance.get_game_status())

    @commands.hybrid_command(description="Stops the ongoing Hangman game")
    async def abort(self, ctx: commands.Context) -> None:
        """Stops the ongoing Hangman game for this server"""
        if not ctx.guild:
            return
        server_id = ctx.guild.id
        if server_id in self.game_instances:
            del self.game_instances[server_id]
            challenger = self.server_id_to_challenger[server_id]
            del self.challenger_to_server_dict[challenger]
            del self.server_id_to_challenger[server_id]
            await ctx.send(STR_ABORT_SUCCESS)
        else:
            await ctx.send(STR_NO_GAME)

    @commands.Cog.listener()
    async def on_message(self, message):
        if not message.guild:
            # Ignore DMs - they also trigger on_message and have no guild
            return
        channel_id = message.channel
        server_id = message.guild.id
        if message.author == self.bot.user:
            return
        if server_id not in self.game_instances:
            return
        hm_instance = self.game_instances[server_id]
        if channel_id != hm_instance.channel_id:
            return
        if not hm_instance.accepting_letters:
            return
        if len(message.content) != 1:
            return
        hm_instance.accepting_letters = False
        hm_instance.process_input(message.content)
        await hm_instance.channel_id.send(hm_instance.get_game_status())
        hm_instance.accepting_letters = True
        if hm_instance.is_game_over:
            del self.challenger_to_server_dict[hm_instance.challenger]
            del self.server_id_to_challenger[server_id]
            del self.game_instances[server_id]


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Hangman(bot))
