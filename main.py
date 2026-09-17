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

    # Util function that converts a `discord.Message` to a dictionary so that it can be serialized by `json`
    def get_message_fields(message: discord.Message):
        return {
            "author": message.author.name,
            "message": message.clean_content,
            "reactions": list(map(lambda r: {"emoji": "custom_" + r.emoji.name if r.is_custom_emoji() else r.emoji, "count": r.count}, message.reactions)),
            "created_at": message.created_at.isoformat(sep=" ", timespec="seconds"),
        }

    # Send reply
    print("Sending initial response...")
    await interaction.response.send_message("Working on it...")

    # Get the messages
    print("Getting messages...")
    messages = [get_message_fields(message) async for message in interaction.channel.history(limit=None, oldest_first=True)]

    # Store in JSON file
    print("Saving to JSON file...")
    os.makedirs("tmp")
    with open("messages.json", "w") as f:
        json.dump(messages, f, indent=4)

    # Send the JSON file
    print("Updating response...")
    await interaction.edit_original_response(content="Done! Download them quick, before they're gone :P", attachments=[discord.File(
        "messages.json")])

    # Delete the JSON file
    print("Deleting JSON file...")
    os.remove("messages.json")
    os.removedirs("./tmp")


# Start bot
client.run(os.environ["BOT_TOKEN"])
