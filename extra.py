from importlib.metadata import metadata
from wsgiref import headers
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
                
    @commands.command(aliases=["va"])
    async def valagent(self, ctx, *, arg):
        """Input ?agent name or ?va name valorant agent skills| ?va"""
        page = requests.get("https://valorant-api.com/v1/agents")
        data = page.json()
        j = 0
        imageURL = ""
        abilities = ""
        skills = ""
        embed = discord.Embed()
        for i in data['data']:
            if i["isPlayableCharacter"]:
                j+=1
                if arg.lower() == i['displayName'].lower():
                    abilities = i['abilities']
                    imageURL = i['displayIcon']
                    
        embed.set_image(url=imageURL,)
        for i in abilities:
            skills+= i['slot'] + ": "
            skills+= i['displayName'] + "\n"
            skills+= i['description'] + "\n\n"
        await ctx.channel.send(embed=embed)
        await ctx.channel.send(">>> " + "```" + skills + "```" )
        
    @commands.command(aliases=["vmmr"])
    async def valmmr(self, ctx, *, arg):
        """Input ?valmmr name/tag or ?vmmr name/tag to check comp stats"""
        s = str(arg)
        s = s.replace(" ", "%20")
        s = str(arg).split("/")
        name, tag=  s[0], s[1]
        if len(s)!=2:
            print("Wrong input")
            return
        URL = f"https://api.henrikdev.xyz/valorant/v2/mmr/na/{name}/{tag}"
        headers = {'User-Agent': 'Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11'}
        page = requests.get(URL, headers=headers)
        json_ = page.json()
        
        s = ""
        if json_['data']['current_data']['currenttierpatched'] == None:
            await ctx.channel.send(">>> Hasn't placed yet or Unrated")
            return
        s+= (
             json_['data']['name'] + " #" + json_['data']['tag'] + "\n" 
             + "Current Act Rank: " + json_['data']['current_data']['currenttierpatched'] + "\n"
             + "Elo: " + str(json_['data']['current_data']['elo']) + "\n\n"
            )
        l = []
        for i in json_['data']['by_season']:
            l.append(str(i))
        for i in l:
            if len(json_['data']['by_season'][i]) > 1:
                temp = i.replace("e", "Episode ").replace("a", " Act ")
                s+= str(temp) + "\n"
                s+= (
                    "Wins: " + str(json_['data']['by_season'][i]['wins']) + "\n"
                    + "Number of Games: " + str(json_['data']['by_season'][i]['number_of_games']) + "\n"
                    + "Final Ranking: " + json_['data']['by_season'][i]['final_rank_patched'] + "\n\n"
                    )
        await ctx.channel.send(">>> ```" + s + "```")
        
    @commands.command(aliases=["vm"])
    async def valmatch(self, ctx, *, arg):
        """Input ?vm name/tag/mode or ?vm name/tag for previous matches"""
        s = str(arg)
        s = s.replace(" ", "%20")
        s = str(arg).split("/")
        nofilter = False
        if len(s) == 2 or len(s) == 3 and s[2] == '':
            name, tag, filter_, nofilter = s[0], s[1], '', True
        elif len(s) == 3 and s[2] != '':
            if "co" in s[2].lower():
                s[2] = "competitive"
            elif "un" in s[2].lower() or s[2].lower() == "ur":
                s[2] = 'unrated'
            elif "de" in s[2].lower() or s[2].lower() == "dm":
                s[2] = "deathmatch"
            elif "es" in s[2].lower():
                s[2] = "escalation"
            elif "re" in s[2].lower():
                s[2] = "replication"
            print(s[2])
            name, tag, filter_=  s[0], s[1], s[2]
        else:
            await ctx.channel.send("Please try again in this format ?vm name/tag/filter or ?vm name/tag e.x ?vm asdf/1234/comp\n"
                                   +"Mode filters[competitve/comp, unrated/ur, deathmatch/dm, replication/rep, escalation/esc]")
            return
        
        if nofilter == True:
            URL = f"https://api.henrikdev.xyz/valorant/v3/matches/na/{name}/{tag}"
        else:
            URL = f"https://api.henrikdev.xyz/valorant/v3/matches/na/{name}/{tag}?filter={filter_}"
        # print( name + " " + tag  + " " + filter_)
        headers = {'User-Agent': 'Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11'}
        page = requests.get(URL, headers=headers)
        json_ = page.json()
        s = ""
        comp = False
        if len(json_['data']) > 0:
            await ctx.channel.send(f">>> Previous matches for {name} #{tag} (Up to 5) \n")
            for i in json_['data']:
                if i["metadata"]:
                    s+= (
                        i["metadata"]['map'] + "\n"
                        + i["metadata"]['mode'] + "\n"
                        + i["metadata"]['game_start_patched'] + "\n"
                        + i["metadata"]['cluster'] + "\n"
                        )
                if i["metadata"]['mode'] == 'Competitive':
                    comp = True
                if i["teams"]['red']['has_won'] == True:
                    s+= (
                        "Winner Team A - " + "Score: " 
                        + str(i["teams"]['red']['rounds_won']) 
                        + ":" + str(i["teams"]['red']['rounds_lost']) +"\n\n"
                        )
                else:
                    s+= (
                        "Winner Team B - " 
                        + "Score: " + str(i["teams"]['blue']['rounds_won']) 
                        + ":" + str(i["teams"]['blue']['rounds_lost']) +"\n\n"
                        )
                    
                if i['players']['red']:
                    s+=("- - - - - TEAM A - - - - -\n")
                    for h in i['players']['red']:
                        s+= h['name']+" #"+h['tag']+ "\n"
                        s+= "Agent: " + h['character']+ "\n"
                        if comp == True:
                             s+= "Rank: " + h['currenttier_patched'] + "\n"
                        s+= (
                            "Score: Kills: " + str(h['stats']['kills']) 
                            + " Deaths: "  + str(h['stats']['deaths']) 
                            + " Assists: " + str(h['stats']['assists']) + "\n\n"
                            )
                        
                if i['players']['blue']:
                    s+=("- - - - - TEAM B - - - - -\n")
                    for h in i['players']['blue']:
                        s+= h['name']+" #"+h['tag']+ "\n"
                        s+= "Agent: " + h['character']+ "\n"
                        if comp == True:
                            s+= "Rank: " + h['currenttier_patched'] + "\n"
                        s+= (
                            "Score: Kills: " + str(h['stats']['kills']) 
                            + " Deaths: "  + str(h['stats']['deaths']) 
                            + " Assists: " + str(h['stats']['assists']) + "\n\n"
                            )
                        
                mapData = ">>> ```" + s + "```"
                await ctx.channel.send(mapData)
                s = ""
                comp = False
        else:
            if len(filter_) != 0:
                await ctx.channel.send(f"Not enough matches of {filter_} to be shown")
            else:
                await ctx.channel.send(f"Not enough data for match history")

    # No longer working because site has blocked webscraping, could not find a way to bypass
    # @commands.command(aliases=["v"], description="Shows a valorant players stats for the current act ex: ?valo test#NA1")
    # async def valo(self, ctx, *, arg):
    #     """Input valorant name#tag for current act stats | ?v"""
    #     s = str(arg)
    #     s = s.replace(" ", "%20")
    #     s = str(arg).split("#")
    #     arg1, arg2, player = s[0], s[1], ""
    #     URL = "https://tracker.gg/valorant/profile/riot/"+ arg1 + "%23" + arg2 + "/overview"
    #     page = requests.get(URL)
    #     soup = BeautifulSoup(page.content, "html.parser")
    #     player = ""
    #     #get current rank
    #     j = soup.findAll(class_="stat")
    #     for i in j:
    #         if i.find("span", class_="stat__value"):
    #             player += (i.text.strip() + "\n")    
                
    #     #get all match stats without top/bottom percentile scores because it looks too cluttered in a discored message
    #     j = soup.findAll(class_="numbers")
    #     for i in j:
    #         words = i.text.strip()
    #         if "Bottom" in words:
    #             player += (words[:words.find("Bottom")] + "\n")
    #         elif "Top" in words:   
    #             a = re.search(r'\b(top)\b', i.text.strip())
    #             player += (words[:words.find("Top")] + "\n")
    #         else:
    #             player += (words + "\n")
                
    #     if len(player) == 0:
    #         await ctx.channel.send(">>> Either the player name is wrong or the tag, try again") 
    #         await ctx.channel.send(">>> If message above takes more than 3 seconds website information is taken from is not cooperating with the bot") 
    #     else:
    #         await ctx.channel.send(">>> Stats for: " + str(arg) + "```" + player + "```") 
    
    #all soup select and findalls where done painfully by looking at website html to get the correct queries 
    @commands.command(aliases=["c"])
    async def champ(self, ctx, *, arg):
        """Input champ and role to get champ data ex:?c velkoz mid| ?c"""
        
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
        if role == "m" or role == "middle":
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
                temp+= "~ ~ ~ Full Build Order ~ ~ ~ \n"
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
        #Getting off a different url because it was getting out dated skill order now uses most popular
        URLSKILLS = F"https://na.op.gg/champions/{name}/{role}/skills"
        skillpage = requests.get(URLSKILLS, headers=headers).text
        soup3 = BeautifulSoup(skillpage, "html.parser")
        li = soup3.find('div', id='content-container').findAll('div', class_="skill_command_box")
        skillOrder = ""
        for i in li:
            if i.select('div[class*="hot-key"]'):
                skillOrder += i.text
                if len(skillOrder) == 3:
                    skillOrder += "R"
                    break
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
                
                if i["src"] not in temp:
                    if "perkStyle" not in i["src"]:
                        temp+= "* " + i["alt"] + "\n"
                    else:
                        temp+= "- " + i["alt"] + " -"+ "\n"
        if len(temp) != 0:
            runes += "~ ~ ~ Runes ~ ~ ~\n" + temp     
        else:
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
                    + tier 
                    + spells + "\n\n"
                    + "Skill Order: " + skillOrder + "\n\n"
                    + items + "\n"
                    + runes + "\n" 
                    + matchups)
        await ctx.channel.send(imageURL)
        await ctx.channel.send("```" + champData + "```")
       
def setup(client):
    client.add_cog(Extra(client))
