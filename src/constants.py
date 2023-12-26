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
    "cogs.background.botstatsapi",
    "cogs.background.events",
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
