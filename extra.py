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
       
    #json data from https://nookipedia.com/
    @commands.command(aliases=["ac"], description="Pick out a animal crossing villager of your choice or pick a random villager ex: ?ac ace or ?ac random or ?ac r")
    async def animalcrossing(self, ctx, *, arg):
        """Input name to pull out villager info or pick a random one | ?ac"""
        
        with open("./animal-crossing-villagers.json", 'r', encoding='utf-8') as f:
            villagers = json.load(f)
        URL = ""
        s= ""
        query = str(arg).lower()
        if query == "random" or query == "r":
            rand = random.randint(0, 489)
            URL += (villagers[rand]["title"]["image_url"])
            s+= "\n".join(
                        ("Name: " + villagers[rand]["title"]["name"], 
                        "Species: " + villagers[rand]["title"]["species"],
                        "Personality: " + villagers[rand]["title"]["personality"],
                        "Gender: " + villagers[rand]["title"]["gender"],
                        "Birthday Month: " + villagers[rand]["title"]["birthday_month"],
                        "Birthday Day: " + villagers[rand]["title"]["birthday_day"],
                        "Sign: " + villagers[rand]["title"]["sign"],
                        "Favorite Saying: " + villagers[rand]["title"]["quote"],
                        "Catch Phrase: " + villagers[rand]["title"]["phrase"],
                        "Clothing: " + villagers[rand]["title"]["clothing"])
                        )
            await ctx.channel.send(URL)
            await ctx.channel.send(">>> \n" + "```" + s + "```")
        else:
            for i in villagers:
                if i["title"]["name"].lower() == query:
                    if len(URL) == 0:
                        URL += i["title"]["image_url"]
                    s+= "\n".join(
                                ("Name: " +i["title"]["name"], 
                                "Species: " + i["title"]["species"],
                                "Personality: " + i["title"]["personality"],
                                "Gender: " + i["title"]["gender"],
                                "Birthday Month: " + i["title"]["birthday_month"],
                                "Birthday Day: " + i["title"]["birthday_day"],
                                "Sign: " + i["title"]["sign"],
                                "Favorite Saying: " + i["title"]["quote"],
                                "Catch Phrase: " + i["title"]["phrase"],
                                "Clothing: " + i["title"]["clothing"])
                                )
            if len(s) > 0:
                await ctx.channel.send(URL)
                await ctx.channel.send(">>> \n" + "```" + s + "```")
            else:
                print(len(s))
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

    #all soup select and findalls where done painfully by looking at website html to get the correct queries 
    @commands.command(aliases=["c"])
    async def champ(self, ctx, *, arg):
        """Input champ and role to get champ data ex:?c velkoz mid| ?c"""
        """Ex: ?c velkoz mid"""
        l = str(arg).lower().split(" ")
        imageURL = ""
        name = l[0]
        role = l[1]
        #special cases on opgg and other league related stat trackers
        if name == "wukong":
            name = "monkeyking"
        if name == "mundo":
            name = "drmundo"
        if name == "jarvan":
            name = "jarvaniv"
            
        if role == "jgl" or role == "jg" or role == "j":
            role = "jungle"
        if role == "ad" or role == "marksman" or role == "a":
            role = "adc"
        if role == "t":
            role = "top"
        if "su" in role or role == "s":
            role = "support"
        if role == "m":
            role = "mid"
            
        URL = f"https://na.op.gg/champions/{name}/{role}/build?region=na&tier=platinum_plus"
        #user agent so that we don't have our GET requests blocked
        headers = {'User-Agent': 'Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11'}
        page = requests.get(URL, headers=headers)
        soup = BeautifulSoup(page.content, "html.parser")

        #could not get build data from scraping op.gg and u.gg so I used metasrc
        URL2 = f"https://www.metasrc.com/5v5/champion/{name}/{role}"
        itempage = requests.get(URL2, headers=headers).text
        soup2 = BeautifulSoup(itempage, "html.parser")
        
        #get champion image to use
        for i in soup.select('img[src*="/images/lol/champion/"]'):
            if name in i["src"].lower():
                imageURL = (i["src"])
                
        #get most common starting items and full build for champion and role
        items = ""
        temp = "" 
        count = 0
        fullBuildCount = 0
        for i in soup2.select('img[style="width: 42px;height: 42px;"]'):
            if count > 2:
                fullBuildCount += 1
            if count == 2:
                temp+= "~ ~ ~ Full Build ~ ~ ~ \n"
                count+=1
            if fullBuildCount >= 7:
                if "elixir" in i["alt"].lower():
                    temp+= "\n*" + i["alt"] + "\n - - - - - - - - -\n"
                    break
                else:
                    temp+= "\n - - - - - - - - -\n"
                    break
            if "/img/item/" in i["data-src"]:
                if "ward" in i["alt"].lower() or "lens" in i["alt"].lower():
                    temp+= "*" + i["alt"] 
                    if count < 2:
                        temp += "\n - - - - - - - - -\n"
                    count+=1
                else:
                    temp+= "*" + i["alt"] + "\n"
        if len(temp) != 0:
            items += "~ ~ ~ Starting Items ~ ~ ~\n" + temp
        else:
            items+=f"Not enough data for {name} {role} for items"
            
        #get tier ranking from OP,1,2,3,4,5 (highest to lowest) for champion and role
        tier = ""
        temp = ""
        for i in soup.select('img[src*="assets/images/tiers/"]'):
            temp += i["alt"].capitalize() + "\n"
        if len(temp) != 0:
            tier+= "Tier: " + temp
        else:
            tier += f"Tier: Unknown"    
            
        #get summoner spell data for champion and role
        spells = ""
        temp = ""
        count = 0
        for i in soup.select('img[src*="/images/lol/spell/Summoner"]'):
            if count == 2:
                temp+= "\n"
            if i["alt"]:
                temp+= (i["alt"]) + " "
                count+=1
        if len(temp) != 0:
            spells+= "\n~ ~ ~ Summoner Spells ~ ~ ~\n" + temp
            
        #get mosted used skill order 
        skillOrder = ""
        for i in soup.select('div[class*="e1mrkevn3"]'):
            skillOrder += i.get_text()
        skillOrder = list(skillOrder)
        skillOrder[2], skillOrder[3] = skillOrder[3], skillOrder[2]
        skillOrder = ' > '.join(skillOrder)
        if len(skillOrder) == 0:
            skillOrder+=f"Not enough data for {name} {role} for skillOrder"
            
        #get most common used runes for champion and role
        runes=""
        temp = ""
        j = soup.find_all("img")
        for i in j:
            if ("/images/lol/perk" in i["src"] 
                and "grayscale" not in i["src"] 
                and "perkShard" not in i["src"] 
                and "48&v" not in i["src"] 
                and "56&v" not in i["src"]):
                
                if i["src"] not in runes:
                    if "perkStyle" not in i["src"]:
                        runes+= "* " + i["alt"] + "\n"
                    else:
                        runes+= "- " + i["alt"] + " -"+ "\n"
        if len(temp) != 0:
            runes+= "~ ~ ~ Runes ~ ~ ~\n" + temp     
        else:
            if len(runes) == 0:
                runes += f"Not enough data for {name} {role} for runes"
                
        #get 5 weakest matchups and 5 strongest matchups for champion and role
        matchups = ""
        j = soup.find_all("a")
        count = 0
        for i in j:
            if count == 5:
                matchups+= "\n- Strong Against -\n"
            if "plus&target_champion=" in i["href"]:
                if count == 0:
                    matchups += "~ ~ ~ Match Ups ~ ~ ~\n"
                    matchups += "- Weak Against -\n"
                temp= ((i["href"]).split("="))
                temp[-1] = temp[-1].capitalize()
                if temp[-1] == "Monkeyking":
                    temp[-1] == "Wukong"
                matchups += "* " +temp[-1]
            if i.select('div[class*="win-rate"]'):
                matchups += " " + (i.text.strip().split("%"))[0] + "%\n"
                count+=1
        if len(matchups) == 0:
            matchups += f"Not enough data for {name} {role} for matchups"

        #concat all data together besides image url
        champData = (f"Champ: {name.capitalize()}" + "\n" 
                    + f"Role: {role.capitalize()}\n" 
                    + tier + "\n"
                    + spells + "\n\n"
                    + "Skill Order: " + skillOrder + "\n\n"
                    + items + "\n"
                    + runes + "\n" 
                    + matchups)
        await ctx.channel.send(imageURL)
        await ctx.channel.send("```" + champData + "```")
       
def setup(client):
    client.add_cog(Extra(client))