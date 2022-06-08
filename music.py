import discord
from discord.ext import commands
import datetime
import youtube_dl
import urllib.request as req
import pytube 
import re

#global variables 
searchList = []
songQueue = []
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

class MusicPlayer(commands.Cog):
    """Music Player"""

    def __init__(self, client):
        self.client = client

    # for both join and leave
    # Doesn't move to other voice channels if the person who summoned the bot tries again in another channel while still active
    # connect to voice channel [core feature]
    @commands.command(description= "Connect bot to users current voice channel or moves bot to users current voice channel if already in another channel")
    async def join(self, ctx):
        """Connect bot to current voice channel or moves bot to user"""
        #these two lines are the basis of all the bot voice activity
        #gets the server voice channels and where the user is located if they are in a voice channel
        voice_channel = discord.utils.get(ctx.guild.voice_channels, name=ctx.message.author.voice.channel.name)
        #gets the voice client aka the bot and the current server 
        voice_client = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
        if voice_client is None:
            voice_client = await voice_channel.connect()
        else:
            await voice_client.move_to(voice_channel)
        
    # Leave voice channel [core feature]
    @commands.command(description= "makes bot leave current voice channel")
    async def leave(self, ctx):
        """Makes bot leave current voice channel"""
        voice_client = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
        if not voice_client is None:
            if voice_client.is_connected():
                await voice_client.disconnect()     

    # Youtube search function [core feature]
    # Sends an embed button for search results found on youtube
    # * grabs the context message and turns it into a string, args grabs all words into one string instead of only first word
    @commands.command(aliases=['s'], description= "Searches for 5 videos relevent to search query")
    async def search(self, ctx, *args):
        """Searches for 5 relevent videos | ?s"""
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
        topFiveResults, i, j, s = [], 0, 1, ""

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

    # helper function get formatted webpage audio url
    async def getAudioURL(self, url):
        global ydl_opts
        #youtube_dl allows us to stream audio as extract_info us to get the entire webpage including the audio source only and use best options for audio
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            webpage = ydl.extract_info(url, download=False)
        return webpage["formats"][0]["url"]

    # Play youtube video [Core Feature]
    @commands.command(description= "Plays song from song search if song already in play will add to queue")
    async def play(self, ctx, *, arg):
        """Plays selection from search adds to queue if already playing"""
        if searchList == []:
            await ctx.channel.send(">>> Must use ?s _ or ?search _ to search for a video first")
        choice = int(arg)
        if choice > 5 or choice < 1:
            await ctx.channel.send(">>> Needs to be a number within 1 and 5")
        else:
            await self.join(ctx)
            voice_client = discord.utils.get(self.client.voice_clients, guild=ctx.guild) 
            
            #extract from the webpage the audio source is located in the formats dictionary and the "url" tag
            song_url = await self.getAudioURL(searchList[choice-1][0])
            
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
                
    @commands.command(description= "Stops song and removes it from play")
    async def stop(self, ctx):
        """Stops song and removes it from play"""
        voice_client = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
        voice_client.stop()
        await ctx.channel.send(">>> Song Stopped and removed")

    @commands.command(description= "Pauses song")
    async def pause(self, ctx):
        """Pauses song"""
        voice_client = discord.utils.get(self.client.voice_clients, guild=ctx.guild) 
        voice_client.pause()
        await ctx.channel.send(">>> Song Paused")
        
    @commands.command(description= "Resumes song")
    async def resume(self, ctx):
        """Resumes song"""
        voice_client = discord.utils.get(self.client.voice_clients, guild=ctx.guild) 
        voice_client.resume()
        await ctx.channel.send(">>> Song Resumed")

    #skips current song and plays the top of queue popped out
    #almost same as play function just use the queued items popped out as our url to play music from
    @commands.command(aliases=['next'], description= "Skips current song and plays next in queue if there is one")
    async def skip(self, ctx):
        """Skips current song and plays next in queue | ?next"""
        voice_client = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
        if len(songQueue) > 0:
            voice_client.stop()
            song = songQueue.pop(0)
            song_url = await self.getAudioURL(song[0])
            voice_client.play(discord.FFmpegPCMAudio(song_url, **FFMPEG_OPTS), after= None)
            # await ctx.channel.send("https://cdn.discordapp.com/emojis/651471037787013126.gif?size=32")
            await ctx.channel.send(song[3])
            await ctx.channel.send(">>> Now playing\n" + song[1] + "| Audio Length: " + song[2])
        else:
            await ctx.channel.send(">>> Song queue is currently empty nothing else to play stopping song")
            await voice_client.stop()   

    @commands.command(aliases=['q'], description= "Shows next song queue")
    async def upcoming(self, ctx):
        """Shows next song queue | ?q"""
        if len(songQueue) > 0:
            await ctx.channel.send(">>> Current Queue Items:\n")
            s, j = "", 1
            for i in songQueue:
                s+= (str(j) + ": " + i[1] + "\n")
                j+=1
            await ctx.channel.send("```" + s + "\nTo play the next song in queue use ?skip or ?next, to play a specific song in queue use ?qp _ or ?queueplay _ ```")
        else:
            await ctx.channel.send("Song queue is currently empty")

    @commands.command(aliases=['qp'], description= "Plays a specific song from queue list")
    async def queueplay(self, ctx, *, arg):
        """Plays a specific song from queue list | ?qp"""
        voice_client = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
        if len(songQueue) > 0:
            choice = int(arg)
            if choice >  len(songQueue) or choice < 0:
                if len(songQueue) == 1:
                    await ctx.channel.send(">>> Queue length is 1 use ?skip or ?next")
                else:
                    await ctx.channel.send(">>> Choice needs a number within 1 and " + str(len(songQueue)))
            else:
                voice_client.stop()
                song = songQueue.pop(choice-1)
                song_url = await self.getAudioURL(song[0])
                voice_client.play(discord.FFmpegPCMAudio(song_url, **FFMPEG_OPTS), after= None)
                await ctx.channel.send(song[3])
                await ctx.channel.send(">>> Now playing\n" + song[1] + "| Audio Length: " + song[2])
        else:
            await ctx.channel.send(">> Song queue is currently empty nothing else to play stopping song")
            
def setup(client):
    client.add_cog(MusicPlayer(client))