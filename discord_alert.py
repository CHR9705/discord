import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
raw_id = os.getenv("auth_id", "")

RECIPIENT_IDS = [int(x.strip()) for x in raw_id.split(",")] if raw_id else []


intents = discord.Intents.default()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"Logged in as {client.user}")
    for user_id in RECIPIENT_IDS:
        try:
            user = await client.fetch_user(user_id)
            await user.send("디스코드 봇 테스팅")
        except discord.Forbidden:
            print(f"Can't DM {user_id} — they may have DMs disabled or don't share a server with the bot.")
    await client.close()

client.run(TOKEN)