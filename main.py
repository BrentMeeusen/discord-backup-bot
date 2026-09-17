import discord
import os
from dotenv import load_dotenv


class BackupClient(discord.Client):
    async def on_ready(self):
        print("Backup Bot ready.")


if __name__ == "__main__":
    if not load_dotenv():
        raise Exception("Couldn't load `.env` file.")

    client = BackupClient(intents=discord.Intents.all())
    client.run(os.environ["BOT_TOKEN"])
