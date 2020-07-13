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


@client.event
async def on_message(message):
  # if the user is the client user itself, ignore the message
  if message.author == client.user:
    return

  # if the message is not in a designated channel, ignore the message
  if message.channel.id not in getConfig()["bound_channels"]:
    return

  # if the message is in a normie language, ignore the message
  if translator.detect(message.content).lang != 'ja':
    return

  # get an english translation
  trans = translator.translate(message.content).text

  # get romaji
  romaji = translator.translate(message.content, dest='ja').pronunciation

  await message.channel.send("Romaji: ```" + romaji + "```\n Translation: ```" + trans + "```")

TOKEN = getConfig()["token"]
print("かんな〜ちゃん: スタート!")
client.run(TOKEN)