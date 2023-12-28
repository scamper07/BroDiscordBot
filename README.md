# BroDiscordBot
A simple discord bot created to learn Python

<!-- ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/discord.py) -->
![Python 3.9](https://img.shields.io/badge/python-3.9+-blue.svg)
![GitHub contributors](https://img.shields.io/github/contributors/scamper07/BroDiscordBot)
![GitHub Workflow Status (with event)](https://img.shields.io/github/actions/workflow/status/scamper07/BroDiscordBot/main.yml)
![GitHub License](https://img.shields.io/github/license/scamper07/BroDiscordBot)
![GitHub repo size](https://img.shields.io/github/repo-size/scamper07/BroDiscordBot)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit)
[![code style: black](https://img.shields.io/badge/code_style-black-000000.svg)](https://github.com/psf/black)

## Getting Started
### Pre requisites
1. Create a Bot application at 	[Discord Developer Portal](https://discord.com/developers/docs/getting-started) and copy client secret
2. Software
    - `Python 3.9 or higher`
    - `Make`
    - `Docker` (optional)

### Manual setup
1. Clone the repo:
    ```
    git clone https://github.com/scamper07/BroDiscordBot.git
    cd BroDiscordBot
    ```
2. Setup virtual environment
    ```
    make setup-venv
    ```
3. Activate the environment

    a. On Linux
    ```
    source bot-env/bin/activate
    ```
    b. On Windows
    ```
    bot-env\Scripts\activate
    ```
4. Install package requirements
    ```
    make setup
    ```
5. Save client secret in `DISCORD_BOT_TOKEN` environment variable

6. Start the bot
    ```
    make run
    ```

Or<br>
### Automated setup using Docker
1. Run the following command
    ```
    docker-compose up -d --build --force-recreate bro
    ```

Done! 