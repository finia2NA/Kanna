from functools import reduce

import json
from typing import List
import discord
from pygoogletranslation import Translator
from langdetect import detect

class Command:
  def __init__(self, keyword, description, method):
    self.keyword = keyword
    self.description = description
    self.method = method

commands:List[Command] = [
  Command("help", "Displays help section", help),
  Command("kanji", "Given a kanji, displays information about it", lambda x: kanji(x)), #TODO: expand to multiple kanji
  Command("reverse", "Translated from English to Japanese", lambda x: translate(x,reversed=True)),
  ]

translator = Translator()
client = discord.Client()

def getConfig():
  try:
    with open("config.json", 'r') as j:
      return json.load(j)
  except FileNotFoundError:
    FileNotFoundError: "Please provide a config.json"

"""pads a string to the given length"""
def pad(s:str,i:int):
  if len(s) < i:
    BadValueError: "Given padding value was lower than string length"

  padding = " "*(i-len(s))

  return s + padding


async def translate(message, reverse = False):

  trans = None;
  romaji = None

  if not reverse:
      # if the message is in a normie language, ignore the message
    # get an english translation
    # FIXME: remove 。 substitution workaround when fixed in pygoogletranslate library
    trans = translator.translate(message.content.replace("。", ".")).text

    # get romaji
    romaji = translator.translate(message.content, dest='ja').pronunciation

  else:
    response = translator.translate(message.content.replace("。", "."), dest='ja')
    trans = response.text
    romaji=response.pronounciation


  await message.channel.send("Romaji: ```" + romaji + " ```\n Translation: ```" + trans + " ```")


async def help(message):
    l = max(map(lambda x:len(x.keyword), commands))

    descriptionString:str = reduce(lambda x, y: x + "\n`" + getConfig()["prefix"] + pad(y.keyword,l) + "` \t" + y.description, commands,"")

    await message.channel.send(
    "🎶 `かんな〜ちゃん v0.2` 🎶\n" + descriptionString
  )

async def kanji(message):
  replystring = None

  if len(message.content) != 8:
    replystring = "please enter a single kanji as an argument."
  else:
    replystring = "https://hochanh.github.io/rtk/"+ message.content[7:] +"/index.html"


  await message.reply(replystring)

@client.event
async def on_message(message):
  # if the user is the client user itself, ignore the message
  if message.author == client.user:
    return

  # if the message is not in a designated channel or server, ignore the message
  if not (message.channel.id in getConfig()["bound_channels"] or message.guild.id in getConfig()["bound_servers"]):
    return

  if(message.content.startswith("?kanji")):
    await kanji(message)
    return

  if message.content.startswith("?help"):
    await help(message)
    return
  
  if message.content.startswith("?tojp"):
    pass #TODO:

  # catch all for things that are def. commands, but I do not recognize
  if message.content.startswith("?"):
    await message.channel.send("Unknown Command :thinking:")

  # finally, if the message is in japanese, do your thing!
  lang = detect(message.content)
  print(lang)
  if lang == 'ja':
    await translate(message)
  

TOKEN = getConfig()["token"]
print("かんな〜ちゃん: スタート!")
client.run(TOKEN)