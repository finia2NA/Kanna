import json
import discord
from googletrans import Translator

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
  if translator.detect(message.content).lang != 'ja':
    return

  # get an english translation
  trans = translator.translate(message.content).text

  # get romaji
  romaji = translator.translate(message.content, dest='ja').pronunciation

  await message.channel.send("Romaji: ```" + romaji + " ```\n Translation: ```" + trans + " ```")

async def help(message):
  await message.channel.send(
    "🎶 `かんな〜ちゃん v0.1` 🎶\n\n"+
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

  # if the message is not in a designated channel, ignore the message
  if message.channel.id not in getConfig()["bound_channels"]:
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