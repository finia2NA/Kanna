import json
from builtins import FileNotFoundError
from functools import reduce
from typing import Callable, List

import discord
from langdetect import detect
from pygoogletranslation import Translator


class Command:
  keyword: str
  description: str
  method: Callable[[discord.Message, str], None]

  def __init__(self, keyword, description, method):
    self.keyword = keyword
    self.description = description
    self.method = method


commands: List[Command] = [
    Command("help", "Displays help section", lambda msg,clean: help(msg)),
    Command("kanji", "Given a kanji, displays information about it",
            lambda msg,clean: kanji(msg,clean)),  # TODO: expand to multiple kanji
    Command("tojp", "Translated from English to Japanese",
            lambda msg,clean: translate(msg, clean, reverse=True)),
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


def pad(s: str, i: int):
  if len(s) < i:
    BadValueError: "Given padding value was lower than string length"

  padding = " "*(i-len(s))

  return s + padding


async def translate(msg, clean=None, reverse=False):
  if clean == None:
    clean = msg.content

  trans = None
  romaji = None

  if not reverse:
    # get an english translation
    # FIXME: remove 。 substitution workaround when fixed in pygoogletranslate library
    trans = translator.translate(clean.replace("。", ".")).text

    # get romaji
    romaji = translator.translate(clean, dest='ja').pronunciation

  else:
    response = translator.translate(
        clean.replace("。", "."), dest='ja')
    trans = response.text
    romaji = response.pronunciation

  await msg.channel.send("Romaji: ```" + romaji + " ```\n Translation: ```" + trans + " ```")


async def help(msg):

  l = max(map(lambda x: len(x.keyword), commands))

  descriptionString: str = reduce(lambda x, y: x + "\n`" + getConfig(
  )["prefix"] + pad(y.keyword, l) + "` \t" + y.description, commands, "")

  await msg.channel.send(
      "🎶 `かんな〜ちゃん v0.2` 🎶\n" + descriptionString
  )


async def kanji(msg, clean=None):
  if clean == None:
    clean = msg.content

  replystring = None

  if len(msg.content) != 8:
    replystring = "please enter a single kanji as an argument."
  else:
    replystring = "https://hochanh.github.io/rtk/" + \
        msg.content[7:] + "/index.html"

  await msg.reply(replystring)


@client.event
async def on_message(message):
  # if the user is the client user itself, ignore the message
  if message.author == client.user:
    return

  # if the message is not in a designated channel or server, ignore the message
  if not (message.channel.id in getConfig()["bound_channels"] or message.guild.id in getConfig()["bound_servers"]):
    return

  # now this looks like a job for me!
  if(message.content.startswith(getConfig()["prefix"])):
    prefixless = message.content[len(getConfig()["prefix"]):]
    for command in commands:
      if prefixless.startswith(command.keyword):
        await command.method(message, prefixless[len(command.keyword) + 1:])

  # finally, if the message is in japanese, do your thing!
  lang = detect(message.content)
  print(lang)
  if lang == 'ja':
    await translate(message)


TOKEN = getConfig()["token"]
print("かんな〜ちゃん: スタート!")
client.run(TOKEN)
