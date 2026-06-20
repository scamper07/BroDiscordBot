import os

# Bot name
BOT_NAME = "Bro Bot"

# Bot prefix
COMMAND_PREFIX = "."

# Bot creator name
BOT_CREATOR_NAME = "scamper"

# Bot github project url
BOT_GITHUB_URL = "https://github.com/scamper07/BroDiscordBot"

# Bot version number
BOT_VERSION_INFO = "0.2"

# List of activated cogs
COGS = [
    "cogs.misc.help",
    "cogs.misc.general",
    "cogs.misc.statistics",
    "cogs.misc.music",
    "cogs.background.botstatsapi",
    "cogs.background.events",
    "cogs.background.status_changer",
    "cogs.background.sleep_remainder",
    # "cogs.background.daily_advice",
    # "cogs.background.daily_news",
    # "cogs.background.twitch_notifier",
    "cogs.background.f1_calendar",
    "cogs.admin.admin",
    "cogs.games.hangman",
    "cogs.games.quiz",
    "cogs.games.tictactoe",
    "cogs.games.tlto",
    "cogs.games.gameboy",
    "cogs.games.terraria",
]

# List of cogs not to be displayed in help command
HELP_HIDDEN_COGS = [
    "Help",
    "AdminOnly",
    "Admin",
    "Events",
    "BotStatsAPI",
    "StatusChanger",
    "SleepRemainder",
    "DailyAdvice",
    "DailyNews",
    "WebHookListener",
]

# Root direction location
ROOT_DIR = os.path.abspath(os.curdir)

# Log location
LOG_FILE_LOCATION = os.path.join(ROOT_DIR, "logs/discord.log")

# Bot Intro Message
BOT_INTRO_MESSAGE = "Say Bro and I'll bro you back"
BOT_INTRO_GIF = "https://media.giphy.com/media/l0K45p4XQTVmyClMs/giphy.gif"

# Error message
BOT_ERROR_GIF = "https://media1.giphy.com/media/5xaOcLyjXRo4hX5UhSU/giphy.gif"

# Channel IDs
ALPHA_MALES_GOODIE_BAG_CHANNEL = 573003537609654283
GENERAL_CHANNEL_ID = 698571675754692752
TEST_CHANNEL_ID = 207481917975560192
TEST2_CHANNEL_ID = 573003537609654283
GAMEBOY_TEST_CHANNEL_ID = 725730342945947701
F1_DISCUSSION_CHANNEL_ID = 729404385901281341
TERRARIA_BACKUP_CHANNEL_ID = 888711934705291294
GOODIE_BAG_OFFICIAL_GENERAL_CHANNEL = 399577277903536138

# Daily task trigger times (24-hr HH:MM, host local time)
DAILY_ADVICE_TIME = "7:30"
DAILY_NEWS_TIME = "9:00"
DAILY_SLEEP_TIME = "0:15"
DAILY_TERRARIA_BACKUP_TIME = "21:20"

# Terraria server (host specific paths/scripts)
OUTPUT_WORLD_FILE = "/home/pi/tshock/Worlds.zip"
TERRARIA_WORLDS_DIR = "/home/pi/tshock/Worlds/"
TERRARIA_WORLDS_BACKUP_DIR = "/home/pi/tshock/Worlds/backup/"

# Twitch stream states
TWITCH_NOT_STREAMING = 0
TWITCH_STARTED_STREAMING = 1
TWITCH_STILL_STREAMING = 2

# External API endpoints
ADVICE_API_URL = "https://api.adviceslip.com/advice"
FACT_API_URL = "https://catfact.ninja/fact"
INSULT_API_URL = "https://insult.mattbas.org/api/insult.json"
XKCD_LATEST_URL = "https://xkcd.com/info.0.json"
XKCD_COMIC_URL = "https://xkcd.com/{}/info.0.json"
NEWS_API_URL = (
    "https://newsapi.org/v2/top-headlines?sources=bbc-news&language=en&apiKey={}"
)
QUIZ_API_URL = (
    "https://opentdb.com/api.php?amount=1&category=9&difficulty={}&type=multiple"
)
TICTACTOE_API_URL = "http://localhost:8080/api/v1/board"
NGROK_TUNNELS_URL = "http://localhost:4040/api/tunnels/"
TWITCH_USERS_API = "https://api.twitch.tv/helix/users?login={}"
TWITCH_STREAMS_API = "https://api.twitch.tv/helix/streams?user_login="
TWITCH_GAMES_API = "https://api.twitch.tv/helix/games?id="

# Web server ports used by background cogs
F1_WEBHOOK_PORT = 4200
BOTSTATS_API_PORT = 8999

# Gameboy key mapping (host virtual keyboard)
GAMEBOY_A = "z"
GAMEBOY_B = "x"
GAMEBOY_L = "a"
GAMEBOY_R = "s"
GAMEBOY_UP = "UP"
GAMEBOY_DOWN = "DOWN"
GAMEBOY_LEFT = "LEFT"
GAMEBOY_RIGHT = "RIGHT"
GAMEBOY_START = "c"
GAMEBOY_SELECT = "v"
GAMEBOY_HOTKEY = "M"

# Quiz limits
MAX_NO_OF_QUIZ_QUESTIONS = 30

# Hangman strings
STR_GAME_OVER = (
    "\n:regional_indicator_g: :regional_indicator_a: :regional_indicator_m: "
    ":regional_indicator_e:      :regional_indicator_o: :regional_indicator_v: "
    ":regional_indicator_e: :regional_indicator_r:\n "
)
STR_YOU_WON = (
    "\n:regional_indicator_y: :regional_indicator_o: :regional_indicator_u:     "
    ":regional_indicator_w: :regional_indicator_o: :regional_indicator_n:\n"
)
STR_YOU_LOST = (
    "\n:regional_indicator_y: :regional_indicator_o: :regional_indicator_u:     "
    ":regional_indicator_l: :regional_indicator_o: :regional_indicator_s: "
    ":regional_indicator_t:\n"
)
STR_GET_WORD = 'Tell me the secret word, type ".word [your word]" '
STR_ALREADY_PLAYING = "I am already playing a game"
STR_ABORT_SUCCESS = "Game stopped"
STR_NO_GAME = "No game running"
STR_GUESSED_SO_FAR = "Guessed so far : "
STR_TRY_HANGMAN = "Please use .hangman before using the 'word' command"
STR_WORD_EMPTY = "Please type your word with the command Eg: .word [your word]"

# Hangman emojis
EMOJI_HANGMAN_ROPE = ".       |"
EMOJI_QUESTION_MARK = ":question:"
EMOJI_POINT_FINGER_UP = ":point_up:"
EMOJI_COAT = ":coat:"
EMOJI_JEANS = ":jeans:"
EMOJI_DIZZY_FACE = ":dizzy_face:"

# Additional stopwords used by the statistics cog word frequency counter
# fmt: off
ADDITIONAL_STOPWORDS = ["|", "-", "0o", "0s", "3a", "3b", "3d", "6b", "6o", "a", "a1", "a2", "a3", "a4", "ab", "able", "about", "above", "abst", "ac", "accordance", "according", "accordingly", "across", "act", "actually", "ad", "added", "adj", "ae", "af", "affected", "affecting", "affects", "after", "afterwards", "ag", "again", "against", "ah", "ain", "ain't", "aj", "al", "all", "allow", "allows", "almost", "alone", "along", "already", "also", "although", "always", "am", "among", "amongst", "amoungst", "amount", "an", "and", "announce", "another", "any", "anybody", "anyhow", "anymore", "anyone", "anything", "anyway", "anyways", "anywhere", "ao", "ap", "apart", "apparently", "appear", "appreciate", "appropriate", "approximately", "ar", "are", "aren", "arent", "aren't", "arise", "around", "as", "a's", "aside", "ask", "asking", "associated", "at", "au", "auth", "av", "available", "aw", "away", "awfully", "ax", "ay", "az", "b", "b1", "b2", "b3", "ba", "back", "bc", "bd", "be", "became", "because", "become", "becomes", "becoming", "been", "before", "beforehand", "begin", "beginning", "beginnings", "begins", "behind", "being", "believe", "below", "beside", "besides", "best", "better", "between", "beyond", "bi", "bill", "biol", "bj", "bk", "bl", "bn", "both", "bottom", "bp", "br", "brief", "briefly", "bs", "bt", "bu", "but", "bx", "by", "c", "c1", "c2", "c3", "ca", "call", "came", "can", "cannot", "cant", "can't", "cause", "causes", "cc", "cd", "ce", "certain", "certainly", "cf", "cg", "ch", "changes", "ci", "cit", "cj", "cl", "clearly", "cm", "c'mon", "cn", "co", "com", "come", "comes", "con", "concerning", "consequently", "consider", "considering", "contain", "containing", "contains", "corresponding", "could", "couldn", "couldnt", "couldn't", "course", "cp", "cq", "cr", "cry", "cs", "c's", "ct", "cu", "currently", "cv", "cx", "cy", "cz", "d", "d2", "da", "date", "dc", "dd", "de", "definitely", "describe", "described", "despite", "detail", "df", "di", "did", "didn", "didn't", "different", "dj", "dk", "dl", "do", "does", "doesn", "doesn't", "doing", "don", "done", "don't", "down", "downwards", "dp", "dr", "ds", "dt", "du", "due", "during", "dx", "dy", "e", "e2", "e3", "ea", "each", "ec", "ed", "edu", "ee", "ef", "effect", "eg", "ei", "eight", "eighty", "either", "ej", "el", "eleven", "else", "elsewhere", "em", "empty", "en", "end", "ending", "enough", "entirely", "eo", "ep", "eq", "er", "es", "especially", "est", "et", "et-al", "etc", "eu", "ev", "even", "ever", "every", "everybody", "everyone", "everything", "everywhere", "ex", "exactly", "example", "except", "ey", "f", "f2", "fa", "far", "fc", "few", "ff", "fi", "fifteen", "fifth", "fify", "fill", "find", "fire", "first", "five", "fix", "fj", "fl", "fn", "fo", "followed", "following", "follows", "for", "former", "formerly", "forth", "forty", "found", "four", "fr", "from", "front", "fs", "ft", "fu", "full", "further", "furthermore", "fy", "g", "ga", "gave", "ge", "get", "gets", "getting", "gi", "give", "given", "gives", "giving", "gj", "gl", "go", "goes", "going", "gone", "got", "gotten", "gr", "greetings", "gs", "gy", "h", "h2", "h3", "had", "hadn", "hadn't", "happens", "hardly", "has", "hasn", "hasnt", "hasn't", "have", "haven", "haven't", "having", "he", "hed", "he'd", "he'll", "hello", "help", "hence", "her", "here", "hereafter", "hereby", "herein", "heres", "here's", "hereupon", "hers", "herself", "hes", "he's", "hh", "hi", "hid", "him", "himself", "his", "hither", "hj", "ho", "home", "hopefully", "how", "howbeit", "however", "how's", "hr", "hs", "http", "hu", "hundred", "hy", "i", "i2", "i3", "i4", "i6", "i7", "i8", "ia", "ib", "ibid", "ic", "id", "i'd", "ie", "if", "ig", "ignored", "ih", "ii", "ij", "il", "i'll", "im", "i'm", "immediate", "immediately", "importance", "important", "in", "inasmuch", "inc", "indeed", "index", "indicate", "indicated", "indicates", "information", "inner", "insofar", "instead", "interest", "into", "invention", "inward", "io", "ip", "iq", "ir", "is", "isn", "isn't", "it", "itd", "it'd", "it'll", "its", "it's", "itself", "iv", "i've", "ix", "iy", "iz", "j", "jj", "jr", "js", "jt", "ju", "just", "k", "ke", "keep", "keeps", "kept", "kg", "kj", "km", "know", "known", "knows", "ko", "l", "l2", "la", "largely", "last", "lately", "later", "latter", "latterly", "lb", "lc", "le", "least", "les", "less", "lest", "let", "lets", "let's", "lf", "like", "liked", "likely", "line", "little", "lj", "ll", "ln", "lo", "look", "looking", "looks", "los", "lr", "ls", "lt", "ltd", "m", "m2", "ma", "made", "mainly", "make", "makes", "many", "may", "maybe", "me", "mean", "means", "meantime", "meanwhile", "merely", "mg", "might", "mightn", "mightn't", "mill", "million", "mine", "miss", "ml", "mn", "mo", "more", "moreover", "most", "mostly", "move", "mr", "mrs", "ms", "mt", "mu", "much", "mug", "must", "mustn", "mustn't", "my", "myself", "n", "n2", "na", "name", "namely", "nay", "nc", "nd", "ne", "near", "nearly", "necessarily", "necessary", "need", "needn", "needn't", "needs", "neither", "never", "nevertheless", "new", "next", "ng", "ni", "nine", "ninety", "nj", "nl", "nn", "no", "nobody", "non", "none", "nonetheless", "noone", "nor", "normally", "nos", "not", "noted", "nothing", "novel", "now", "nowhere", "nr", "ns", "nt", "ny", "o", "oa", "ob", "obtain", "obtained", "obviously", "oc", "od", "of", "off", "often", "og", "oh", "oi", "oj", "ok", "okay", "ol", "old", "om", "omitted", "on", "once", "one", "ones", "only", "onto", "oo", "op", "oq", "or", "ord", "os", "ot", "other", "others", "otherwise", "ou", "ought", "our", "ours", "ourselves", "out", "outside", "over", "overall", "ow", "owing", "own", "ox", "oz", "p", "p1", "p2", "p3", "page", "pagecount", "pages", "par", "part", "particular", "particularly", "pas", "past", "pc", "pd", "pe", "per", "perhaps", "pf", "ph", "pi", "pj", "pk", "pl", "placed", "please", "plus", "pm", "pn", "po", "poorly", "possible", "possibly", "potentially", "pp", "pq", "pr", "predominantly", "present", "presumably", "previously", "primarily", "probably", "promptly", "proud", "provides", "ps", "pt", "pu", "put", "py", "q", "qj", "qu", "que", "quickly", "quite", "qv", "r", "r2", "ra", "ran", "rather", "rc", "rd", "re", "readily", "really", "reasonably", "recent", "recently", "ref", "refs", "regarding", "regardless", "regards", "related", "relatively", "research", "research-articl", "respectively", "resulted", "resulting", "results", "rf", "rh", "ri", "right", "rj", "rl", "rm", "rn", "ro", "rq", "rr", "rs", "rt", "ru", "run", "rv", "ry", "s", "s2", "sa", "said", "same", "saw", "say", "saying", "says", "sc", "sd", "se", "sec", "second", "secondly", "section", "see", "seeing", "seem", "seemed", "seeming", "seems", "seen", "self", "selves", "sensible", "sent", "serious", "seriously", "seven", "several", "sf", "shall", "shan", "shan't", "she", "shed", "she'd", "she'll", "shes", "she's", "should", "shouldn", "shouldn't", "should've", "show", "showed", "shown", "showns", "shows", "si", "side", "significant", "significantly", "similar", "similarly", "since", "sincere", "six", "sixty", "sj", "sl", "slightly", "sm", "sn", "so", "some", "somebody", "somehow", "someone", "somethan", "something", "sometime", "sometimes", "somewhat", "somewhere", "soon", "sorry", "sp", "specifically", "specified", "specify", "specifying", "sq", "sr", "ss", "st", "still", "stop", "strongly", "sub", "substantially", "successfully", "such", "sufficiently", "suggest", "sup", "sure", "sy", "system", "sz", "t", "t1", "t2", "t3", "take", "taken", "taking", "tb", "tc", "td", "te", "tell", "ten", "tends", "tf", "th", "than", "thank", "thanks", "thanx", "that", "that'll", "thats", "that's", "that've", "the", "their", "theirs", "them", "themselves", "then", "thence", "there", "thereafter", "thereby", "thered", "therefore", "therein", "there'll", "thereof", "therere", "theres", "there's", "thereto", "thereupon", "there've", "these", "they", "theyd", "they'd", "they'll", "theyre", "they're", "they've", "thickv", "thin", "think", "third", "this", "thorough", "thoroughly", "those", "thou", "though", "thoughh", "thousand", "three", "throug", "through", "throughout", "thru", "thus", "ti", "til", "tip", "tj", "tl", "tm", "tn", "to", "together", "too", "took", "top", "toward", "towards", "tp", "tq", "tr", "tried", "tries", "truly", "try", "trying", "ts", "t's", "tt", "tv", "twelve", "twenty", "twice", "two", "tx", "u", "u201d", "ue", "ui", "uj", "uk", "um", "un", "under", "unfortunately", "unless", "unlike", "unlikely", "until", "unto", "uo", "up", "upon", "ups", "ur", "us", "use", "used", "useful", "usefully", "usefulness", "uses", "using", "usually", "ut", "v", "va", "value", "various", "vd", "ve", "very", "via", "viz", "vj", "vo", "vol", "vols", "volumtype", "vq", "vs", "vt", "vu", "w", "wa", "want", "wants", "was", "wasn", "wasnt", "wasn't", "way", "we", "wed", "we'd", "welcome", "well", "we'll", "well-b", "went", "were", "we're", "weren", "werent", "weren't", "we've", "what", "whatever", "what'll", "whats", "what's", "when", "whence", "whenever", "when's", "where", "whereafter", "whereas", "whereby", "wherein", "wheres", "where's", "whereupon", "wherever", "whether", "which", "while", "whim", "whither", "who", "whod", "whoever", "whole", "who'll", "whom", "whomever", "whos", "who's", "whose", "why", "why's", "wi", "widely", "will", "willing", "wish", "with", "within", "without", "wo", "won", "wonder", "wont", "won't", "words", "world", "would", "wouldn", "wouldnt", "wouldn't", "www", "x", "x1", "x2", "x3", "xf", "xi", "xj", "xk", "xl", "xn", "xo", "xs", "xt", "xv", "xx", "y", "y2", "yes", "yet", "yj", "yl", "you", "youd", "you'd", "you'll", "your", "youre", "you're", "yours", "yourself", "yourselves", "you've", "yr", "ys", "yt", "z", "zero", "zi", "zz"]  # noqa: E501
# fmt: on
