import random, requests, json
import time
from bs4 import BeautifulSoup

def gag(text):
    vowels = "aeiou"
    new_text = (
        text.lower()
        .replace("tt", "t")
        .replace("t", "th")
        .replace("ss", "s")
        .replace("s", "sh")
        .replace("gg", "g")
        .replace("g", "gh")
        .replace("k", "gh")
        .replace("l", "n")
        .replace("v", "f")
        )

    if new_text[-1] != "~" and random.randint(0,1) == 1:
        new_text = new_text + "~"

    for x in new_text: 
        if x in vowels:
            new_text = new_text.replace(x, "m")

    return new_text

def uwuify(text):
    uwu_text = (
        text.lower()
        .replace("l", "w")
        .replace("r", "w")
        .replace("v", "f")
    )

    return uwu_text + random.choice([" >~<", "~"])

def gelbooru(tags):
    url = f'https://gelbooru.com/index.php?page=dapi&s=post&q=index&json=1&limit=100&tags={tags}'
    response = requests.get(url)
    data = response.json()
    posts = data.get('post')
    if posts:
        images = []
        for post in posts:
            img = post.get('file_url')
            images.append(img)
        return images
    else:
        return None