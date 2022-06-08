#file used for independently testing pure python without starting the bot
# import urllib.request as req
# import pytube 
# import re
# import youtube_dl
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

# import requests
# from bs4 import BeautifulSoup

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