import discord
from googleapiclient.discovery import build
import os

TOKEN = os.environ['TOKEN']
ytAPI = os.environ['YT']

userId = "UC_KcYKZtzAgZwXczRcI55lw"

channelsIds = {
  "Minebarth" : "UC_KcYKZtzAgZwXczRcI55lw",
  "DZiX" : "UCGd9ZMiV2ZUEdUqMI3oIaEQ",
  "Gucio" : "gutekwitek"
}

client = discord.Client()
youtube = build('youtube','v3',developerKey=ytAPI)

requestMB = youtube.channels().list(part='statistics',id=channelsIds["Minebarth"])
requestDZ = youtube.channels().list(part='statistics',id=channelsIds["DZiX"])
requestGU = youtube.channels().list(part='statistics',forUsername=channelsIds["Gucio"])
responseMB = requestMB.execute()
responseDZ = requestDZ.execute()
responseGU = requestGU.execute()

channelsSubscribers = {
  "Minebarth" : responseMB['items'][0]['statistics']['subscriberCount'],
  "DZiX" : responseDZ['items'][0]['statistics']['subscriberCount'],
  "Gucio" : responseGU['items'][0]['statistics']['subscriberCount']
}

channelsViews = {
  "Minebarth" : responseMB['items'][0]['statistics']['viewCount'],
  "DZiX" : responseDZ['items'][0]['statistics']['viewCount'],
  "Gucio" : responseGU['items'][0]['statistics']['viewCount'],
}

def getName(msg):
  return msg.split()[1]

@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
  if message.author == client:
    return

  if any(nick in message.content for nick in channelsIds):
    nickName = getName(message.content)
    if message.content.startswith('!subs'):
        await message.channel.send(nickName+ " ma obecnie " +channelsSubscribers[nickName]+ " subów!")
    if message.content.startswith('!views'):
        await message.channel.send(nickName+ " ma obecnie " +channelsViews[nickName]+ " wyświetleń!")

client.run(TOKEN)
