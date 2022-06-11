#file used for independently testing pure python without starting the bot
import urllib.request as req
from matplotlib import style
import pytube 
import re
from soupsieve import match, select
import youtube_dl
import requests
from bs4 import BeautifulSoup
# page = req.urlopen("https://www.youtube.com/results?search_query=apex")
# pageDecode = page.read().decode('utf8')
# videoID = re.findall( r"watch\?v=(\S{11})", pageDecode)
# topFive = []
# for item in range(0, 5):
#     vidLink = "https://www.youtube.com/watch?v=" + videoID[item]
#     vidTitle = pytube.YouTube(vidLink).title
#     topFive.append((vidLink, vidTitle))
# for i in topFive:
#     print(i)
# print(topFive[0][0])

# ydl_opts = {
#         'format': 'bestaudio/best',
#         'postprocessors': [{
#             'key': 'FFmpegExtractAudio',
#             'preferredcodec': 'mp3',
#             'preferredquality': '192',
#         }],
#     }
# with youtube_dl.YoutubeDL(ydl_opts) as ydl:
#     song_info = ydl.extract_info("https://www.youtube.com/watch?v=yRljn8NaDDE", download=False)
# song_url = song_info["formats"][0]["url"]
# print(song_info)


# URL = "https://tracker.gg/valorant/profile/riot/glizzynguyen%23BACK/overview"
# page = requests.get(URL)
# p = ""
# soup = BeautifulSoup(page.content, "html.parser")
# # print(soup)
# j = soup.find_all("span", class_="stat__value")
# j = soup.findAll(class_='numbers', attrs={'class':'numbers'})
# for i in j:
#     if i.find("span", class_="rank"):
#         continue
#     else:
#         p+=(i.text.strip())
# print(p)
# import random
# import json
# with open("./animal-crossing-villagers.json", 'r', encoding='utf-8') as f:
#     villagers = json.load(f)
#     rand = random.randint(0, 480)
#     s = ""
#     s+= "\n".join(
#                 ("Name: " + villagers[rand]["name"], 
#                 "Species: " + villagers[rand]["species"],
#                 "Personality: " + villagers[rand]["personality"],
#                 "Gender: " + villagers[rand]["gender"],
#                 "Birthday Month: " + villagers[rand]["birthday_month"],
#                 "Birthday Day: " + villagers[rand]["birthday_day"],
#                 "Sign: " + villagers[rand]["sign"],
#                 "Favorite Saying: " + villagers[rand]["quote"],
#                 "Catch Phrase: " + villagers[rand]["phrase"],
#                 "Clothing: " + villagers[rand]["clothing"])
#                 )
#     c = "ankha"
#     for i in villagers:
#         print(i["name"].lower() )
#         if i["name"].lower() == c:
#             s+= "\n".join(
#                         ("Name: " + i["name"], 
#                         "Species: " + i["species"],
#                         "Personality: " + i["personality"],
#                         "Gender: " + i["gender"],
#                         "Birthday Month: " + i["birthday_month"],
#                         "Birthday Day: " + i["birthday_day"],
#                         "Sign: " + i["sign"],
#                         "Favorite Saying: " + i["quote"],
#                         "Catch Phrase: " + i["phrase"],
#                         "Clothing: " + i["clothing"])
#                         )
#     print(s)
# imageURL = ""
# name = "alistar"
# role = "top"
# #special cases on opgg and other league related stat trackers
# if name.lower() == "wukong":
#     name = "monkeyking"
# if name.lower() == "mundo":
#     name = "drmundo"
# if name.lower() == "jarvan":
#     name = "jarvaniv"
# URL = f"https://na.op.gg/champions/{name}/{role}/build?region=na&tier=platinum_plus"
# #user agent so that we don't have our GET requests blocked
# headers = {'User-Agent': 'Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11'}
# page = requests.get(URL, headers=headers)
# soup = BeautifulSoup(page.content, "html.parser")

# #could not get build data from scraping opgg and ugg so I used metasrc
# URL2 = f"https://www.metasrc.com/5v5/champion/{name}/{role}"
# itempage = requests.get(URL2, headers=headers).text
# soup2 = BeautifulSoup(itempage, "html.parser")

# items = "~ ~ ~ Starting Items ~ ~ ~\n" 
# count = 0
# fullBuildCount = 0
# for i in soup2.select('img[style="width: 42px;height: 42px;"]'):
#     if count > 2:
#         fullBuildCount += 1
#     if count == 2:
#         items+= "~ ~ ~ Full Build ~ ~ ~ \n"
#         count+=1
#     if fullBuildCount >= 7:
#         if "elixir" in i["alt"].lower():
#             items+= "\n*" + i["alt"] + "\n - - - - - - - - -\n"
#             break
#         else:
#             items+= "\n - - - - - - - - -\n"
#             break
#     if "/img/item/" in i["data-src"]:
#         if "ward" in i["alt"].lower() or "lens" in i["alt"].lower():
#             items+= "*" + i["alt"] 
#             if count < 2 :
#                 items += "\n - - - - - - - - -\n"
#             count+=1
#         else:
#             items+= "*" + i["alt"] + "\n"
            
# print(fullBuildCount)
# #get summoner spell data for champion and role
# spells = ""
# count = 0
# for i in soup.select('img[src*="/images/lol/spell/Summoner"]'):
#     if count == 2:
#         spells+= "\n"
#     if i["alt"]:
#         if count == 0:
#             spells+= "~ ~ ~ Summoner Spells ~ ~ ~\n"
#         spells+= (i["alt"]) + " "
#         count+=1
# #get champion image to use
# for i in soup.select('img[src*="/images/lol/champion/"]'):
#     if name in i["src"].lower():
#         imageURL = (i["src"])
        
# #get tier ranking from OP,1,2,3,4,5 (highest to lowest) for champion and role
# tier = "Tier: "
# for i in soup.select('img[src*="assets/images/tiers/"]'):
#     tier += i["alt"].capitalize() + "\n"
    
# #get mosted used skill order 
# skillOrder = ""
# for i in soup.select('div[class*="e1mrkevn3"]'):
#     skillOrder += i.get_text()
# skillOrder = list(skillOrder)
# skillOrder[2], skillOrder[3] = skillOrder[3], skillOrder[2]
# skillOrder = ' > '.join(skillOrder)

# #get most common used runes for champion and role
# runes="~ ~ ~ Runes ~ ~ ~\n"
# j = soup.find_all("img")
# for i in j:
#     if ("/images/lol/perk" in i["src"] 
#         and "grayscale" not in i["src"] 
#         and "perkShard" not in i["src"] 
#         and "48&v" not in i["src"] 
#         and "56&v" not in i["src"]):
        
#         if i["src"] not in runes:
#             if "perkStyle" not in i["src"]:
#                 runes+= "* " + i["alt"] + "\n"
#             else:
#                  runes+= "- " + i["alt"] + " -"+ "\n"
                 
# #get 5 weakest matchups and 5 strongest matchups for champion and role
# matchups = ""
# j = soup.find_all("a")
# count = 0
# for i in j:
#     if count == 5:
#         matchups+= "\n- Strong Against -\n"
#     if "plus&target_champion=" in i["href"]:
#         if count == 0:
#             matchups += "~ ~ ~ Match Ups ~ ~ ~\n"
#             matchups += "- Weak Against -\n"
#         temp= ((i["href"]).split("="))
#         temp[-1] = temp[-1].capitalize()
#         if temp[-1] == "Monkeyking":
#             temp[-1] == "Wukong"
#         matchups += "* " +temp[-1]
#     if i.select('div[class*="win-rate"]'):
#         matchups += " " + (i.text.strip().split("%"))[0] + "%\n"
#         count+=1
# if len(matchups) == 0:
#     matchups += f"Not enough data for {name} {role} for matchups"


# #concat all data together besides image url
# champData = (f"Champ: {name.capitalize()}" + "\n" 
#              + f"Role: {role.capitalize()}\n" 
#              + tier + "\n"
#              + spells + "\n\n"
#              + "Skill Order: " + skillOrder + "\n\n"
#              + items + "\n"
#              + runes + "\n" 
#              + matchups)

# print(champData)

