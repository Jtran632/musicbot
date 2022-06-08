# bot.py
import os
import discord
from discord.ext import commands
import onMessageCommands as com
from dotenv import load_dotenv
import csv
import random
import json
import requests
import re
import bs4
from bs4 import BeautifulSoup
import datetime
import youtube_dl
import urllib.request as req
import pytube

# Outcomes:
# - Can't find song
# - Reply to let user know their song is queued

# Core Features 
# - Function Search for Song / Artist (Gives Top 5 results) 
# - Function Play Song 
# - Stop Bot (Remove from VC) 
# - Pause and Skip songs in queue 
# - Look @ Queue list 
# - Choose from queue (Similiar to Search for Song / Artist)

# Grabs message from chat in does one of the functions below 

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
intents = discord.Intents.default()

#lets use a prefix to call functions instead of using the on_message function
client = commands.Bot(command_prefix='?', description="Music Bot", intents=intents, case_insensitive=True)
COGS = ['music', 'extra']

@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == GUILD:
            break
    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )
    
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if ("hi" == message.content.lower() or
        "hello" == message.content.lower() or
        "wassup" == message.content.lower() or
        "yo" == message.content.lower() or
        "hola" == message.content.lower()):
        await message.channel.send("Hello! {}".format(message.author.mention))
    elif "bd" in message.content.lower() or "birthday" in message.content.lower():
        await message.channel.send("Happy Birthday! ! !")
    elif ("lol" in message.content.lower() 
            or "urf" in message.content.lower() 
            or "league" in message.content.lower()):
        await com.league(message)
    elif "devour" in message.content.lower():
        await com.devourQuote(message)
    await client.process_commands(message)

# error logic for on message
@client.event
async def on_error(event, *args, **kwargs):
    with open('err.log', 'a') as f:
        if event == 'on_message':
            f.write(f'Unhandled message: {args[0]} \n')
        else:
            raise
            
if __name__ == '__main__':
    for cog in COGS:
        client.load_extension(cog)
    client.run(TOKEN)