import os

import discord
from dotenv import load_dotenv

import mysql.connector


# Get token from .env
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()

# Connects to SQL server specified in .env file and returns connector
def get_connector(cnx):

    # check if connector is already connected
    if cnx.is_connected() is True:
        return cnx

    # get login info
    this_user=os.getenv('SQL_USER')
    this_password=os.getenv('SQL_PASSWORD')
    this_host=os.getenv('SQL_HOST')
    this_database=os.getenv('SQL_DATABASE')

    try:
        # login to database and get connector
        cnx=mysql.connector.connect(user=this_user, password=this_password,
                                    host=this_host, database=this_database)

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Invalid username or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)

    else:
        return cnx


# Replaces @mentions in the message with fakeName and returns the string
def replace_mentions(message, fakeName)

    # first get list of mentions in the message
    mentions = message.mentions.name

    # different mentions will be replaced with index numbers
    # e.g. "@Lorian threw a ball to @Lothric" will be replaced with
    #      "@fakeName0 threw a ball to @fakeName2"
    fakeNameIndex = 0

    new_msg = ''

    for names in mentions:
        replacement = fakename + fakeNameIndex
        new_msg = message.content.replace(names, replacement)
        fakeNameIndex += 1

    return new_msg


# Takes message and stores it in database 
def store_message(message)
    

@client.event
async def on_message(message):
    #Ignore message sent by this bot
    if message.author==client.user:
        return

    print(f'{message.author}:', message.clean_content);

@client.event
async def on_message_delete(message):
    # Ignore message sent by this bot
    if message.author==client.user:
        return
    print(f'(Deleted) {message.author}:', message.clean_content);

@client.event
async def on_ready():
    print(f'{client.user} is connected to:')

    # Print all the connected guilds
    for guild in client.guilds:
        print(f'{guild.name} (id: {guild.id})')    




#(main)===================================

# connect to SQL server first
connect_SQL_DB()

client.run(TOKEN)
