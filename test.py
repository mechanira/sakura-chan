import requests, random, webbrowser

apikey = "AIzaSyD2xu7C33nuVDG3dlxn4sr_A6Aycruksxc"
ckey = "Tenor"
lmt = 10

search_term = "anime-pat"

response = requests.get(
    "https://tenor.googleapis.com/v2/search?q=%s&key=AIzaSyD2xu7C33nuVDG3dlxn4sr_A6Aycruksxc&client_key=Tenor&limit=20" % (search_term))
data = response.json()
gif = random.choice(data["results"])
    
print(gif["media_formats"]["mediumgif"]["url"])