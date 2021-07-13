import aiohttp
from discord.ext import commands
from discord_slash import cog_ext
from discord_slash.utils import manage_commands
from discord_slash.utils.manage_commands import create_choice

from base_logger import logger


class HM:
    # Manages one instance of Hangman game at a given time
    def __init__(self):
        self.truth = None
        self.guessed_letters = []
        self.wrong_answers = 0
        self.blanks = []
        self.hangman_status = ""
        self.game_in_progress = False
        self.is_game_over = False
        self.has_player_won = False
        self.print_list = [".       |", ".     :dizzy_face:", ".:point_up:", ":coat:",":point_up:",
                           " .     :jeans:", ]

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
                self.blanks.append(":question:")
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
            result_string += "\n :regional_indicator_g: :regional_indicator_a: :regional_indicator_m: :regional_indicator_e:      :regional_indicator_o: :regional_indicator_v: :regional_indicator_e: :regional_indicator_r: \n "
            if self.has_player_won:
                result_string += ":regional_indicator_y: :regional_indicator_o: :regional_indicator_u:     :regional_indicator_w: :regional_indicator_o: :regional_indicator_n:"
            else:
                result_string += ":regional_indicator_y: :regional_indicator_o: :regional_indicator_u:     :regional_indicator_l: :regional_indicator_o: :regional_indicator_s: :regional_indicator_t:" + "\n" + "The word was " + self.truth
        else:
            result_string = "Guessed so far : "
            guesses = self.guessed_letters
            for i in range(len(guesses)):
                result_string += guesses[i].upper() + " , "

        blanks = ""
        for b in self.blanks:
            blanks += b + "\t"
        return "\n" + blanks + " \n " + self.hangman_status + "\n" + result_string


class Hangman(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.channel_id = None
        self.accepting_letter = False
        self.hangman = HM()

    @commands.command(brief="Hangman game")
    async def hangman(self, ctx):
        # dm player1
        # Create a hangman instance
        # print on channel
        if self.hangman.game_in_progress:
            ctx.channel.send("I am already playing a game")
            return
        self.hangman.game_in_progress = True
        self.channel_id = ctx.channel
        player_one = ctx.author.id
        user = self.bot.get_user(player_one)
        await user.send("Tell me the secret word, type \".word [your word]\" ")

    @commands.command()
    async def word(self, ctx, word=""):
        if not self.hangman.game_in_progress:
            ctx.channel.send("Please use .hangman before using the word command")
            return
        if word == "":
            ctx.channel.send("Please type your word with the command Eg: .word [your word]")
        self.accepting_letter = True
        self.hangman.truth = word.upper()
        self.hangman.process_input("")
        await self.channel_id.send(self.hangman.get_game_status())

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return
        if not self.hangman.game_in_progress:
            return
        if not self.accepting_letter:
            return
        if len(message.content) != 1:
            return
        self.accepting_letter = False
        self.hangman.process_input(message.content)
        await message.channel.send(self.hangman.get_game_status())
        self.accepting_letter = True
        if self.hangman.is_game_over:
            self.hangman.game_in_progress = False
            self.hangman = HM()


def setup(bot):
    bot.add_cog(Hangman(bot))
