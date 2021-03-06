import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

# The prefix added before any command to which Bro bot will respond
COMMAND_PREFIX = '.'

# Channel info
ALPHA_MALES_GOODIE_BAG_CHANNEL = 573003537609654283
GENERAL_CHANNEL_ID = 698571675754692752
TEST_CHANNEL_ID = 207481917975560192
TEST2_CHANNEL_ID = 573003537609654283
GAMEBOY_TEST_CHANNEL_ID = 725730342945947701
F1_DISCUSSION_CHANNEL_ID = 729404385901281341

# Twitch globals
TWITCH_NOT_STREAMING = 0
TWITCH_STARTED_STREAMING = 1
TWITCH_STILL_STREAMING = 2

# Quiz globals
MAX_NO_OF_QUIZ_QUESTIONS = 30

# Misc globals
MEMBER_UPDATE_COUNT = 0
stats_brief = 'Shows random stats about server, {}stats <username> for user'.format(COMMAND_PREFIX)

# Messages/Quotes
WAR_CRY_LIST = ['LET\'S GO BROS!',
                'IT\'S OUR TIME TO SHINE BROS!',
                'Leeeeroy Jenkins!',
                'IT\'S TIME TO KICK ASS BROS!',
                'Carpe diem. Seize the day, bros',
                'Requiescat in pace bros',
                'May the Force be with you bros',
                'Keep your friends close, but your enemies closer bros',
                'Hasta la vista, bros',
                'Fasten your seatbelts. It\'s going to be a bumpy ride bros',
                'To infinity and beyond bros!',
                'The Force will be with you. Always.',
                'The time to fight is now bros.'
                ]


# Gameboy key mapping
GAMEBOY_A = 'z'
GAMEBOY_B = 'x'
GAMEBOY_L = 'a'
GAMEBOY_R = 's'
GAMEBOY_UP = 'UP'
GAMEBOY_DOWN = 'DOWN'
GAMEBOY_LEFT = 'LEFT'
GAMEBOY_RIGHT = 'RIGHT'
GAMEBOY_START = 'c'
GAMEBOY_SELECT = 'v'
GAMEBOY_HOTKEY = 'M'

DEBUG_FLAG_FILE = "/home/pi/debug"

DAILY_ADVICE_TIME = "6:45"  # am
DAILY_NEWS_TIME = "9:30"  # am
DAILY_SLEEP_TIME = "0:00"

admin_id_path = os.path.join(ROOT_DIR, "keys/admin_id")
with open(admin_id_path) as f:
    ADMIN_ID = f.read().strip()
