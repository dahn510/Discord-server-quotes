import os
import discord
from dotenv import load_dotenv

#Get Discord token stored in .env file
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.client()


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')




client.run(TOKEN)
