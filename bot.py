import discord
from discord.ext import commands
import os
import re

# ---- ENV VARIABLES ----
TOKEN = os.environ.get("DISCORD_TOKEN")
# -----------------------

SOURCE_CHANNEL_ID = 1399251260183543868
TARGET_CHANNEL_ID = 1460461467601080352

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

LINK_REGEX = re.compile(r"https?://")

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
