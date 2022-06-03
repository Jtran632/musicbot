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
