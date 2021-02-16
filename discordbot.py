import os

import discord
from dotenv import load_dotenv

#Get token from .env
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()

@client.event
async def on_message(message):
    #Ignore message sent by this bot
    if message.author==client.user:
        return;

    print(f'{message.author}:', message.clean_content);

@client.event
async def on_message_delete(message):
    #Ignore message sent by this bot
    if message.author==client.user:
        return;
    print(f'(Deleted) {message.author}:', message.clean_content);

@client.event
async def on_ready():
    print(f'{client.user} is connected to:')

    #Print all the connected guilds
    for guild in client.guilds:
        print(f'{guild.name} (id: {guild.id})')    



client.run(TOKEN)
