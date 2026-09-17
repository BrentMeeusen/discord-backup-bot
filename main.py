import discord
import os
import json
from dotenv import load_dotenv


# Set up environment variables and client
if not load_dotenv():
    raise Exception("Couldn't load `.env` file.")


# Create client
class BackupClient(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)

        self.tree = discord.app_commands.CommandTree(self)

    async def setup_hook(self) -> None:
        if "TEST_SERVER_ID" not in os.environ:
            print("No test server ID provided. Continuing without force-refresh.")
            return

        guild_id = discord.Object(id=os.environ["TEST_SERVER_ID"])

        self.tree.copy_global_to(guild=guild_id)
        await self.tree.sync(guild=guild_id)

        print(f"Synchronised tree with {len(self.tree.get_commands(guild=guild_id))} commands")

    async def on_ready(self):
        print("Backup Bot ready.")


# Instantiate client
client = BackupClient(intents=discord.Intents.all())


# Define app commands
@client.tree.command()
async def backup(interaction: discord.Interaction):
    """
    Download all messages sent in this channel as a JSON file.
    """

    # Converts a `discord.Message` to a dictionary so that it can be serialized by `json`.
    def get_message_fields(message: discord.Message):
        return {
            "author": message.author.name,
            "message": message.clean_content,
            "reactions": list(map(lambda r: {"emoji": r.emoji, "count": r.count}, message.reactions)),
            "created_at": message.created_at.isoformat(sep=" ", timespec="seconds"),
        }

    # Get the messages
    messages = [get_message_fields(message) async for message in interaction.channel.history(limit=None, oldest_first=True)]

    # Store in JSON file
    os.makedirs("tmp")
    with open("./tmp/messages.json", "w") as f:
        json.dump(messages, f, indent=4)

    # Send the JSON file
    await interaction.response.send_message(file=discord.File("./tmp/messages.json"))

    # Delete the JSON file
    os.remove("./tmp/messages.json")
    os.removedirs("./tmp")


# Start bot
client.run(os.environ["BOT_TOKEN"])
