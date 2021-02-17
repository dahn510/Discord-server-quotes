import os

import discord
from dotenv import load_dotenv

import mysql.connector


#Get token from .env
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()

#Connects to SQL server specified in .env file and returns connector
def connect_SQL_DB(cnx):

    this_user=os.getenv('SQL_USER')
    this_password=os.getenv('SQL_PASSWORD')
    this_host=os.getenv('SQL_HOST')
    this_database=os.getenv('SQL_DATABASE')

    try:
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
        

#Logs discord message to the server
def log_message(message, cnx):
    

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




#(main)===================================
connect_SQL_DB();

client.run(TOKEN)
