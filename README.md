# BroDiscordBot
A simple discord bot created to learn Python


## Getting Started
### Pre requisites
1. Create a Bot application at 	[Discord Developer Portal](https://discord.com/developers/docs/getting-started) and copy client secret
2. Software
    - `Python3.10`
    - `Make`

### Manual
1. Clone the repo using these steps:
```
git clone https://github.com/scamper07/BroDiscordBot.git
cd BroDiscordBot
```
2. Setup virtual environment
```
make setup-venv
```
3. Activate the environment

4. Install package requirements
```
make setup
```
5. Save client secret in `DISCORD_BOT_TOKEN` environment variable

6. Start the bot
```
python3 src/main.py
```

Or<br>
### Automated using Docker
1. Run the following command
```
docker-compose up -d --build --force-recreate bro
```

Done! 