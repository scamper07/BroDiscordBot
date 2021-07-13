from discord.ext import commands

import constants


class HM:
    # Manages one instance of Hangman game at a given time
    def __init__(self, server_id, channel_id, challenger):
        self.server_id = server_id
        self.channel_id = channel_id
        self.challenger = challenger
        self.accepting_letters = False
        self.truth = None
        self.guessed_letters = []
        self.wrong_answers = 0
        self.blanks = []
        self.hangman_status = ""
        self.is_game_over = False
        self.has_player_won = False
        self.print_list = [constants.EMOJI_HANGMAN_ROPE, ".     " + constants.EMOJI_DIZZY_FACE, "." + constants.EMOJI_POINT_FINGER_UP, constants.EMOJI_COAT, constants.EMOJI_POINT_FINGER_UP,
                           " .     " + constants.EMOJI_JEANS ]

    def process_input(self, letter):
        if self.is_game_over:
            return
        if letter.upper() in self.truth:
            self.update_blanks(letter)
        else:
            self.wrong_answers += 1
            self.update_hangman_status(self.wrong_answers)
        if letter not in self.guessed_letters and letter != "":
            self.guessed_letters.append(letter)

    def update_blanks(self, letter):
        if letter == "":
            for _ in self.truth:
                self.blanks.append(constants.EMOJI_QUESTION_MARK)
        else:
            for i, l in enumerate(self.truth):
                if l.upper() == letter.upper():
                    self.blanks[i] = letter.upper()
        if self.blanks == list(self.truth):
            self.is_game_over = True
            self.has_player_won = True

    def update_hangman_status(self, wrong_answers):
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
            result_string += constants.STR_GAME_OVER
            if self.has_player_won:
                result_string += constants.STR_YOU_WON
            else:
                result_string += constants.STR_YOU_LOST + "\n" + "The word was " + self.truth
        else:
            result_string = constants.STR_GUESSED_SO_FAR
            guesses = self.guessed_letters
            for i in range(len(guesses)):
                result_string += guesses[i].upper() + " , "

        blanks = ""
        for b in self.blanks:
            blanks += b + "\t"
        return "\n" + blanks + " \n" + self.hangman_status + "\n" + result_string


class Hangman(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.game_instances = {}
        self.challenger_to_server_dict = {}

    @commands.command(brief="Hangman game")
    async def hangman(self, ctx):
        # dm challenger
        # Create a hangman instance
        # print on channel
        server_id = ctx.guild.id
        channel_id = ctx.channel
        challenger = ctx.author.id
        if server_id in self.game_instances:
            await ctx.channel.send(constants.STR_ALREADY_PLAYING)
            return
        else:
            self.game_instances[server_id] = HM(server_id, channel_id, challenger)
        user = self.bot.get_user(challenger)
        self.challenger_to_server_dict[challenger] = server_id
        await user.send(constants.STR_GET_WORD)

    @commands.command()
    async def word(self, ctx, word=""):
        challenger = ctx.author.id
        if challenger not in self.challenger_to_server_dict:
            await ctx.channel.send(constants.STR_TRY_HANGMAN)
            return
        server_id = self.challenger_to_server_dict[challenger]
        hm_instance = self.game_instances[server_id]
        if word == "":
            await ctx.channel.send(constants.STR_WORD_EMPTY)
            return
        hm_instance.accepting_letters = True
        hm_instance.truth = word.upper()
        hm_instance.process_input("")
        await hm_instance.channel_id.send(hm_instance.get_game_status())

    @commands.Cog.listener()
    async def on_message(self, message):
        if not message.guild:
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
            del self.game_instances[server_id]


def setup(bot):
    bot.add_cog(Hangman(bot))
