# Discord Backup Bot
A simple Python project to back up text channels in servers using a slash command.
The bot is not developed to be run 24/7; instead, it is meant to be started up if you want to make a backup.
It is probably possible to have it running on some server, but that is up to you to figure out if that's what you're after.

## Getting started
The project is built with Python 3.14.0 and uses `.venv`.

### Setting up a development environment

[//]: # (TODO: make sure that this is correct)

1. Clone the repository.
2. Install the packages from `requirements.txt` using `pip install -r requirements.txt`.
3. Set up your Discord bot in the Discord Developer Portal.
4. Copy `.env.example` to `.env` and enter your environment variables.
5. Run `main.py` to start the bot.

### Updating requirements
If you need more requirements or want to upgrade existing ones, remember to run `pip freeze > requirements.txt` afterwards so that the latest package versions are in there.
