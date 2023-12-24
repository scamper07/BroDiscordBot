from discord.ext import commands
import constants


class HM:
    # Manages one instance of Hangman game at a given time
    def __init__(self, server_id, channel_id, challenger):
        # state variables
        self.server_id = server_id
        self.channel_id = channel_id
        self.challenger = challenger
        self.accepting_letters = False
        self.is_game_over = False
        self.has_player_won = False
        # used by game logic
        self.truth = None
        self.guessed_letters = []
        self.wrong_answers = 0
        self.blanks = []
        self.hangman_status = ""
        self.print_list = [constants.EMOJI_HANGMAN_ROPE, ".     " + constants.EMOJI_DIZZY_FACE,
                           "." + constants.EMOJI_POINT_FINGER_UP, constants.EMOJI_COAT, constants.EMOJI_POINT_FINGER_UP,
                           " .     " + constants.EMOJI_JEANS]

    def process_input(self, letter):
        if self.is_game_over:
            return
        if letter.upper() in self.truth:
            # If letter is in the word - update the blanks
            self.update_blanks(letter)
        else:
            # If letter is not in the word count it as a wrong answer and update the hangman
            self.wrong_answers += 1
            self.update_hangman_status(self.wrong_answers)
        if letter.upper() not in self.guessed_letters and letter != "":
            self.guessed_letters.append(letter.upper())

    def update_blanks(self, letter):
        if letter == "":
            # draw exactly len(truth) number of dashes - game initialization
            for _ in self.truth:
                self.blanks.append(constants.EMOJI_QUESTION_MARK)
        else:
            # update relevant index of the blanks list
            for i, l in enumerate(self.truth):
                if l.upper() == letter.upper():
                    self.blanks[i] = letter.upper()
        if self.blanks == list(self.truth):
            # the player won
            self.is_game_over = True
            self.has_player_won = True

    def update_hangman_status(self, wrong_answers):
        # The arms and body needs to be in a straight line and therefore no new line character
        if wrong_answers == 3 or wrong_answers == 4:
            self.hangman_status += self.print_list[wrong_answers - 1]
        else:
            self.hangman_status += self.print_list[wrong_answers - 1] + "\n"
        if self.wrong_answers == len(self.print_list):
            # the player is out of chances
            self.is_game_over = True
            self.has_player_won = False

    def get_game_status(self):
        # Check if the player won, lost or is still ongoing and return relevant status
        # The output of this method is a string and can be printed/used/shown to the user as is.
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
        # maintain dictionaries 1. server to HM object and 2. challenger to server_id. 3. server_id to challenger
        self.game_instances = {}
        self.challenger_to_server_dict = {}
        self.server_id_to_challenger = {}

    @commands.command(brief="Hangman game")
    async def hangman(self, ctx):
        server_id = ctx.guild.id
        channel_id = ctx.channel
        challenger = ctx.author.id
        if server_id in self.game_instances:
            await ctx.channel.send(constants.STR_ALREADY_PLAYING)
            return
        else:
            # Create new HM instance per server
            self.game_instances[server_id] = HM(server_id, channel_id, challenger)
        user = self.bot.get_user(challenger)
        self.challenger_to_server_dict[challenger] = server_id
        self.server_id_to_challenger[server_id] = challenger
        # DM user
        await user.send(constants.STR_GET_WORD)

    @commands.command()
    async def word(self, ctx, word=""):
        challenger = ctx.author.id
        if challenger not in self.challenger_to_server_dict:
            # Word command used before .hangman send retry message
            await ctx.channel.send(constants.STR_TRY_HANGMAN)
            return
        # We have the challenger (because we DMd him)
        # Use the challenger to get server_id and in turn the relevant HM game instance
        server_id = self.challenger_to_server_dict[challenger]
        hm_instance = self.game_instances[server_id]
        if word == "":
            # Word was empty ? Retry
            await ctx.channel.send(constants.STR_WORD_EMPTY)
            return
        # The below variable sets a flag which starts accepting letters in the onMessage fn.
        hm_instance.accepting_letters = True
        hm_instance.truth = word.upper()
        hm_instance.process_input("")
        # Send blanks and start the game
        await hm_instance.channel_id.send(hm_instance.get_game_status())

    @commands.command()
    async def abort(self, ctx):
        # Consider only messages from a server so the game associated with the server can be stopped
        if not ctx.guild:
            return
        # Get server that is requesting the game to be stopped
        server_id = ctx.guild.id
        if server_id in self.game_instances:
            # clear dictionaries
            del self.game_instances[server_id]
            challenger = self.server_id_to_challenger[server_id]
            del self.challenger_to_server_dict[challenger]
            del self.server_id_to_challenger[server_id]
            await ctx.send(constants.STR_ABORT_SUCCESS)
        else:
            await ctx.send(constants.STR_NO_GAME)

    @commands.Cog.listener()
    async def on_message(self, message):
        if not message.guild:
            # Ignore DMs, DMs to the bot also triggers on_message and for DMs guild don't exist and it crashes
            return
        channel_id = message.channel
        server_id = message.guild.id
        if message.author == self.bot.user:
            return
        if server_id not in self.game_instances:
            return
        hm_instance = self.game_instances[server_id]
        if channel_id != hm_instance.channel_id:
            # Ignore messages from other channels
            return
        if not hm_instance.accepting_letters:
            # Return if not accepting letters.
            return
        if len(message.content) != 1:
            # Only accept single char
            return
        hm_instance.accepting_letters = False
        hm_instance.process_input(message.content)
        # send out the game progress
        await hm_instance.channel_id.send(hm_instance.get_game_status())
        hm_instance.accepting_letters = True
        if hm_instance.is_game_over:
            # Clean up dictionary, erase game instance and remove challenger
            del self.challenger_to_server_dict[hm_instance.challenger]
            del self.server_id_to_challenger[server_id]
            del self.game_instances[server_id]


def setup(bot):
    bot.add_cog(Hangman(bot))
