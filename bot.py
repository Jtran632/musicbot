# bot.py
import datetime
import os
import csv
from time import sleep
import youtube_dl
import random
import discord
from discord import FFmpegAudio
from discord.ext import commands
import botCommands as com
from dotenv import load_dotenv
import urllib.request as req
import pytube 
import re

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

#global variables 
searchList = []
songQueue = []
intents = discord.Intents.default()
FFMPEG_OPTS = {'before_options': 
                '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 
                'options': '-vn'}
ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
}

# client = discord.Client()
#lets use a prefix to call functions instead of using the on_message function
client = commands.Bot(command_prefix='?', description="Music Bot", intents=intents, case_insensitive=True)

@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == GUILD:
            break
    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )
    
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
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if ("hi" in message.content.lower() or
        "hello" in message.content.lower() or
        "wassup" in message.content.lower() or
        "yo" in message.content.lower() or
        "hola" in message.content.lower()):
        await message.channel.send("Hello! {}".format(message.author.mention))
    if "random" in message.content.lower():
        await com.randomQuote(message)
    elif "bd" in message.content.lower() or "birthday" in message.content.lower():
        await message.channel.send("Happy Birthday! ! !")
    elif "lol" in message.content.lower() or "urf" in message.content.lower() or "league" in message.content.lower():
        await com.randomQuote(message)
    elif "devour" in message.content.lower():
        await com.devourQuote(message)
    await client.process_commands(message)

# error logic  
@client.event
async def on_error(event, *args, **kwargs):
    with open('err.log', 'a') as f:
        if event == 'on_message':
            f.write(f'Unhandled message: {args[0]} \n')
        else:
            raise
        
# Should be in another file but need to implement cog cause it doesn't work on seperate file right now
# for both join and leave
# Doesn't move to other voice channels if the person who summoned the bot tries again in another channel while still active
# connect to voice channel [core feature]
@client.command(description= "makes bot join current channel or moves bot to current channel if already in another channel")
async def join(ctx):
    #these two lines are the basis of all the bot voice activity
    #gets the server voice channels and where the user is located if they are in a voice channel
    voice_channel = discord.utils.get(ctx.guild.voice_channels, name=ctx.message.author.voice.channel.name)
    #gets the voice client aka the bot and the current server 
    voice_client = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice_client is None:
        voice_client = await voice_channel.connect()
    else:
        await voice_client.move_to(voice_channel)
    
# Leave voice channel [core feature]
@client.command(description= "makes bot leave current voice channel")
async def leave(ctx):
    voice_client = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if not voice_client is None:
        if voice_client.is_connected():
            await voice_client.disconnect()     

# Youtube search function [core feature]
# Sends an embed button for search results found on youtube
# * grabs the context message and turns it into a string, args grabs all words into one string instead of only first word
@client.command(aliases=['s'], description= "searches for 5 songs relevent to search query and joins voice channel if not already in a channel")
async def search(ctx, *args):
    global searchList
    query = ("+".join(args[:]))
    # search = url + query 
    s = "https://www.youtube.com/results?search_query=" + query
    #request url on youtube using urllib.request
    page = req.urlopen(s)
    #decode html content into english using urllib
    pageDecode = page.read().decode('utf8')
    #use regex to filter out video ids to concatenate into a watch url
    videoID = re.findall( r"watch\?v=(\S{11})", pageDecode)
    #pytube allows me to grab title from watch link and I add the top five into choices
    topFiveResults = []
    i = 0
    j = 1
    s = ""

    await ctx.channel.send(">>> Retreiving results please wait" + ctx.author.mention)
    while True:
        if j > 5:
            break
        vidLink = "https://www.youtube.com/watch?v=" + videoID[i]
        vidTitle = pytube.YouTube(vidLink).title
        vidThumb = pytube.YouTube(vidLink).thumbnail_url
        vidLength = str(datetime.timedelta(seconds=pytube.YouTube(vidLink).length))
        if (vidLink, vidTitle, vidLength, vidThumb) not in topFiveResults:
            topFiveResults.append((vidLink, vidTitle, vidLength, vidThumb))
            s += str(j) + ": " + vidTitle + "\n"
            j+=1
        i +=1 
    await ctx.channel.send("```\nSelect video with ?play and a number within 1-5 ex: ?play 1" + f'\n{s}``` ')
        
    searchList = topFiveResults
    # print(searchList)

# helper function get formatted webpage audio url
async def getAudioURL(url):
    global ydl_opts
    #youtube_dl allows us to stream audio as extract_info us to get the entire webpage including the audio source only and use best options for audio
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        webpage = ydl.extract_info(url, download=False)
    return webpage["formats"][0]["url"]

import asyncio  
# Play youtube video [Core Feature]
@client.command(description= "plays song from song search")
async def play(ctx, *, arg):
    if searchList == []:
        await ctx.channel.send(">>> Must use ?s _ or ?search _ to search for a video first")
    choice = int(arg)
    if choice > 5 or choice < 1:
        await ctx.channel.send(">>> Needs to be a number within 1 and 5")
    else:
        await join(ctx)
        voice_client = discord.utils.get(client.voice_clients, guild=ctx.guild) 
        
        #extract from the webpage the audio source is located in the formats dictionary and the "url" tag
        song_url = await getAudioURL(searchList[choice-1][0])
        
        #play with ffmpeg using song url we extracted and apply ffmepg options we want for best audio and set after param to do something 
        #if song is already playing we our selected song to queue
        try:
            voice_client.play(discord.FFmpegPCMAudio(song_url, **FFMPEG_OPTS), after= None)
            # await ctx.channel.send("https://cdn.discordapp.com/emojis/651471037787013126.gif?size=32")
            await ctx.channel.send(searchList[choice-1][3])
            await ctx.channel.send(">>> Now playing\n" + searchList[choice-1][1] + "| Audio Length: " + searchList[choice-1][2])
        except:
            songQueue.append(searchList[choice-1])
            await ctx.channel.send(">>> Added to queue\n" + searchList[choice-1][1] )
            print(songQueue)
            
@client.command(description= "stops song and removes it from play")
async def stop(ctx):
    voice_client = discord.utils.get(client.voice_clients, guild=ctx.guild)
    voice_client.stop()
    await ctx.channel.send("Song Stopped")

@client.command(description= "pauses song")
async def pause(ctx):
    voice_client = discord.utils.get(client.voice_clients, guild=ctx.guild) 
    voice_client.pause()
    await ctx.channel.send("Song Paused")
    
@client.command(description= "resumes song")
async def resume(ctx):
    voice_client = discord.utils.get(client.voice_clients, guild=ctx.guild) 
    voice_client.resume()
    await ctx.channel.send("Song Resumed")

#skips current song and plays the top of queue popped out
#almost same as play function just use the queued items popped out as our url to play music from
@client.command(aliases=['next'], description= "skips current song and plays next in queue")
async def skip(ctx):
    voice_client = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if len(songQueue) > 0:
        voice_client.stop()
        song = songQueue.pop()
        song_url = await getAudioURL(song[0])
        voice_client.play(discord.FFmpegPCMAudio(song_url, **FFMPEG_OPTS), after= None)
        # await ctx.channel.send("https://cdn.discordapp.com/emojis/651471037787013126.gif?size=32")
        await ctx.channel.send(song[3])
        await ctx.channel.send("Now playing\n" + song[1] + "| Audio Length: " + song[2])
    else:
        await ctx.channel.send("Song queue is currently empty nothing else to play stopping song")
        await voice_client.stop()   

@client.command(aliases=['q'], description= "Shows next song queue")
async def upcoming(ctx):
    if len(songQueue) > 0:
        await ctx.channel.send("Current Queue Items:\n")
        s, j = "", 1
        for i in songQueue[:-1]:
            s+= (str(j) + ": " + i[1] + "\n")
            j+=1
        await ctx.channel.send(s)
    else:
        await ctx.channel.send("Song queue is currently empty")
    
# @client.event
# async def on_command_error(ctx, error):
#     if isinstance(error, commands.CommandNotFound): 
#         await ctx.channel.send("?help for valid bot commands")
    
# --------------------------------------------------------------------------------------------------------------------------------------------------------#
# extra functions for fun

#using a kaggle joke dataset brings out a random joke
@client.command(aliases=['j'])
async def joke(ctx):
    filename = open('shortjokes.csv', 'r')
    file = csv.DictReader(filename)
    jokes = []
    for i in file:
        jokes.append(i['Joke'])
    await ctx.channel.send(random.choice(jokes))

#brings out a random pokemon picture from fileset
@client.command(aliases=['p', 'poke'])
async def pokemon(ctx):
    p = "./pokemon/"
    files=os.listdir(p)
    rand = random.choice(files)
    d= p + rand
    name = rand.rsplit(".",1)[0]
    await ctx.channel.send(name, file=discord.File(d))
    
client.run(TOKEN)