import json
import discord
from pygoogletranslation import Translator
from langdetect import detect

translator = Translator()
client = discord.Client()

def getConfig():
  try:
    with open("config.json", 'r') as j:
      return json.load(j)
  except FileNotFoundError:
    FileNotFoundError: "Please provide a config.json"

async def translate(message):

    # if the message is in a normie language, ignore the message
  lang = detect(message.content)
  print(lang)
  if lang != 'ja':
    return

  # get an english translation
  trans = translator.translate(message.content).text

  # get romaji
  romaji = translator.translate(message.content, dest='ja').pronunciation

  await message.channel.send("Romaji: ```" + romaji + " ```\n Translation: ```" + trans + " ```")

async def help(message):
  await message.channel.send(
    "🎶 `かんな〜ちゃん v0.2` 🎶\n\n"+
    "`?kanji []` -> enter a single kanji, get its RTK index page."
  )

async def kanji(message):
  if len(message.content) != 8:
    await message.channel.send("please enter a single kanji as an argument.")
    return
  await message.channel.send("https://hochanh.github.io/rtk/"+ message.content[7:] +"/index.html")

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

  # catch all for things that are def. commands, but I do not recognize
  if message.content.startswith("?"):
    await message.channel.send("Unknown Command :thinking:")

  await translate(message)

TOKEN = getConfig()["token"]
print("かんな〜ちゃん: スタート!")
client.run(TOKEN)