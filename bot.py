import discord
from discord.ext import commands
import os
import re

# ==============================
# ENV VARIABLE (Render)
# ==============================
TOKEN = os.environ.get("DISCORD_TOKEN")

if not TOKEN:
    raise ValueError("DISCORD_TOKEN environment variable not found.")

# ==============================
# CHANNEL CONFIG
# ==============================
SOURCE_CHANNEL_ID = 1399251260183543868
TARGET_CHANNEL_ID = 1460461467601080352

# ==============================
# BOT SETUP
# ==============================
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Regex to detect http/https links
LINK_REGEX = re.compile(r"https?://")

# ==============================
# EVENTS
# ==============================
@bot.event
async def on_ready():
    print("===================================")
    print(f"Logged in as {bot.user}")
    print("Link Mirror Bot is now running.")
    print("===================================")

@bot.event
async def on_message(message):
    # Ignore bot messages
    if message.author.bot:
        return

    # Only listen to source channel
    if message.channel.id != SOURCE_CHANNEL_ID:
        return

    # Check if message contains a link
    has_link = LINK_REGEX.search(message.content)

    # If no link AND no attachments → ignore
    if not has_link and not message.attachments:
        return

    target_channel = bot.get_channel(TARGET_CHANNEL_ID)
    if not target_channel:
        print("Target channel not found.")
        return

    try:
        # Send message content if it exists
        if message.content:
            await target_channel.send(
                f"**{message.author.display_name}:** {message.content}"
            )

        # Send attachments (if any)
        for attachment in message.attachments:
            await target_channel.send(attachment.url)

    except Exception as e:
        print(f"Error forwarding message: {e}")

    await bot.process_commands(message)

# ==============================
# RUN BOT
# ==============================
bot.run(TOKEN)
