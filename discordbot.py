import os

import sys
import discord
from dotenv import load_dotenv

import mysql.connector


# Get token from .env
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()

# get admin id
admin = os.getenv('DISCORD_ADMIN')


# Connects to SQL server specified in .env file and returns connector/connection
def get_connector():

    # get login info
    this_user = os.getenv('SQL_USER')
    this_password = os.getenv('SQL_PASSWORD')
    this_host = os.getenv('SQL_HOST')
    this_database = os.getenv('SQL_DATABASE')

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
        print("### Connection established to SQL server")
        return cnx


# Replaces @ mentions in the message with fakeName and returns the string
def replace_mentions(message, fakeName):

    # first get list of mentions in the message
    mentions = message.mentions

    # different mentions will be replaced with index numbers
    # e.g. "@Lorian threw a ball to @Lothric" will be replaced with
    #      "@fakeName0 threw a ball to @fakeName2"
    fakeNameIndex = 0

    new_msg = message.clean_content


    for member in mentions:
        replacement = fakeName + str(fakeNameIndex)
        fakeNameIndex += 1
        new_msg = new_msg.replace(member.display_name, replacement)

    return new_msg


# Takes message and stores it in database 
def store_message(message):
    global cnx

    # SQL insert statment
    add_message = ("INSERT INTO messages (message) VALUES (%s)")

    # replace @ mentions with 'Human'
    data_message = replace_mentions(message, 'Human')
    # limit string length since the database only accepts messages up to 2000 characters
    data_message = (data_message[0:2000],)

    # check if connector is connected
    if cnx.is_connected() is False:
        cnx = get_connector()

    cursor = cnx.cursor()
    
    # insert new message
    cursor.execute(add_message, data_message)
    # just to make sure data is committed to the database
    cnx.commit()

    cursor.close()


@client.event
async def on_message(message):
    # ignore message sent by this bot
    if message.author == client.user:
        return

    # process !shutdown command to safely disconnect and close
    if message.content.startswith("!shutdown"):
        if message.author.id == int(admin):
            await client.close()
            cnx.close()
            sys.exit()

        else:
            print(type(message.author.id))
            print(f'Warning: non-admin(id:{message.author.id} tried to invoke !shutdown command')


    print(f'{message.author}:', message.clean_content);
    store_message(message)

@client.event
async def on_message_delete(message):
    # Ignore message sent by this bot
    if message.author == client.user:
        return
    print(f'(Deleted) {message.author}:', message.clean_content);


@client.event
async def on_ready():
    print(f'{client.user} is connected to:')

    # Print all the connected guilds
    for guild in client.guilds:
        print(f'{guild.name} (id: {guild.id})')    




cnx = get_connector()
client.run(TOKEN)
