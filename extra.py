import discord
from discord.ext import commands
import os
import csv
import random
import json
import requests
import re
from bs4 import BeautifulSoup

# extra commands just for fun and learning
class Extra(commands.Cog):
    """Extra Commands"""

    def __init__(self, client):
        self.client = client
            
    #using a kaggle joke dataset brings out a random joke
    @commands.command(aliases=['j'])
    async def joke(self, ctx):
        """Pulls out a random joke from a pool of 200,000 jokes | ?j"""
        
        filename = open('shortjokes.csv', 'r')
        file = csv.DictReader(filename)
        jokes = []
        for i in file:
            jokes.append(i['Joke'])
        await ctx.channel.send(random.choice(jokes))

    #brings out a random pokemon picture from fileset
    @commands.command(aliases=['p', 'poke'])
    async def pokemon(self, ctx):
        """Pulls out a random pokemon image from gens 1-8 | ?p"""
        
        p = "./pokemon/"
        files=os.listdir(p)
        rand = random.choice(files)
        d= p + rand
        name = rand.rsplit(".",1)[0]
        await ctx.channel.send(name, file=discord.File(d))
        
    @commands.command(aliases=["ac"], description="Pick out a animal crossing villager of your choice or pick a random villager ex: ?ac ace or ?ac random or ?ac r")
    async def animalcrossing(self, ctx, *, arg):
        """Input name to pull out villager info or pick a random one | ?ac"""
        
        with open("./animal-crossing-villagers.json", 'r', encoding='utf-8') as f:
            villagers = json.load(f)
        URL = ""
        s= ""
        query = str(arg).lower()
        if query == "random" or query == "r":
            rand = random.randint(0, 480)
            URL += (villagers[rand]["image_url"])
            s+= "\n".join(
                        ("Name: " + villagers[rand]["name"], 
                        "Species: " + villagers[rand]["species"],
                        "Personality: " + villagers[rand]["personality"],
                        "Gender: " + villagers[rand]["gender"],
                        "Birthday Month: " + villagers[rand]["birthday_month"],
                        "Birthday Day: " + villagers[rand]["birthday_day"],
                        "Sign: " + villagers[rand]["sign"],
                        "Favorite Saying: " + villagers[rand]["quote"],
                        "Catch Phrase: " + villagers[rand]["phrase"],
                        "Clothing: " + villagers[rand]["clothing"])
                        )
            await ctx.channel.send(URL)
            await ctx.channel.send(">>> \n" + "```" + s + "```")
        else:
            for i in villagers:
                if i["name"].lower() == query:
                    if len(URL) == 0:
                        URL += i["image_url"]
                    s+= "\n".join(
                                ("Name: " + i["name"], 
                                "Species: " + i["species"],
                                "Personality: " + i["personality"],
                                "Gender: " + i["gender"],
                                "Birthday Month: " + i["birthday_month"],
                                "Birthday Day: " + i["birthday_day"],
                                "Sign: " + i["sign"],
                                "Favorite Saying: " + i["quote"],
                                "Catch Phrase: " + i["phrase"],
                                "Clothing: " + i["clothing"])
                                )
            if len(s) != 0:
                await ctx.channel.send(URL)
                await ctx.channel.send(">>> \n" + "```" + s + "```")
            else:
                await ctx.channel.send(">>> Sorry the villager name you're looking for isn't correct please try again with ?ac _ or ?ac r or ?ac random")
                
    @commands.command(aliases=["v"], description="Shows a valorant players stats for the current act ex: ?valo test#NA1")
    async def valo(self, ctx, *, arg):
        """Input valorant name#tag for current act stats | ?v"""
        s = str(arg)
        s = s.replace(" ", "%20")
        s = str(arg).split("#")
        arg1, arg2, player = s[0], s[1], ""
        URL = "https://tracker.gg/valorant/profile/riot/"+ arg1 + "%23" + arg2 + "/overview"
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, "html.parser")
        
        #get current rank
        j = soup.findAll(class_="stat")
        for i in j:
            if i.find("span", class_="stat__value"):
                player += (i.text.strip() + "\n")    
                
        #get all match stats without top/bottom percentile scores because it looks too cluttered in a discored message
        j = soup.findAll(class_="numbers")
        for i in j:
            words = i.text.strip()
            if "Bottom" in words:
                player += (words[:words.find("Bottom")] + "\n")
            elif "Top" in words:   
                a = re.search(r'\b(top)\b', i.text.strip())
                player += (words[:words.find("Top")] + "\n")
            else:
                player += (words + "\n")
                
        if len(player) == 0:
            await ctx.channel.send(">>> Either the player name is wrong or the tag, try again") 
        else:
            await ctx.channel.send(">>> Stats for: " + str(arg) + "```" + player + "```") 
            
def setup(client):
    client.add_cog(Extra(client))