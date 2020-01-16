import requests as req
from bs4 import BeautifulSoup
import discord

def getUrban(arg1):
    resp = req.get(arg1)
    if resp.status_code == 200:
        soup = BeautifulSoup(resp.text, "lxml")
    else:
        return False
    title = soup.findAll("a", {"class": "word"})[0].text
    meaning = soup.find("div", {"class": "meaning"}).text
    example = soup.find("div", {"class": "example"}).text
    return createEmbed(title, meaning, example)

def createEmbed(arg1, arg2, arg3):
    embed = discord.Embed(title=arg1, color=0x00ff00)
    embed.add_field(name="Meaning", value=arg2)
    embed.add_field(name="Example", value=arg3)
    return embed