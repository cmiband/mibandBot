import discord
from googleapiclient.discovery import build
import os

TOKEN = os.environ['TOKEN']
ytAPI = os.environ['YT']

client = discord.Client()
youtube = build('youtube','v3',developerKey=ytAPI)

request = youtube.channels().list(part="snippet",id="UC_KcYKZtzAgZwXczRcI55lw")
rsp = request.execute()

def getName(msg):
  return msg.split()[2]

def getIdOrUsername(msg):
  return msg.split()[1]

@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
  if message.author == client:
    return

  if message.content.startswith('!subs'):
    if getIdOrUsername(message.content)=='id':
      userId = getName(message.content)
      request = youtube.channels().list(part='statistics',id=userId)
      requestName = youtube.channels().list(part='snippet',id=userId)
      response = request.execute()
      responseName = requestName.execute()
      if response['pageInfo']['totalResults'] == 0:
        await message.channel.send("Brak wyników(złe id).")
      else:
        subs = response['items'][0]['statistics']['subscriberCount']
        channelName = responseName['items'][0]['snippet']['title']
        await message.channel.send(channelName +" ma obecnie "+subs+" subów!")
    if getIdOrUsername(message.content)=='username':
      nickName = getName(message.content)
      request = youtube.channels().list(part='statistics',forUsername=nickName)
      response = request.execute()
      if response['pageInfo']['totalResults'] == 0:
        await message.channel.send("Brak wyników(zła nazwa).")
      else:
        subs = response['items'][0]['statistics']['subscriberCount']
        await message.channel.send(nickName +" ma obecnie "+subs+" subów!")
    if getIdOrUsername(message.content)!='id' and getIdOrUsername(message.content)!='username':
      await message.channel.send("Niesprecyzowany filtr szukania")
  
  if message.content.startswith('!views'):
    if getIdOrUsername(message.content)=='id':
      userId = getName(message.content)
      request = youtube.channels().list(part='statistics',id=userId)
      response = request.execute()
      if response['pageInfo']['totalResults'] == 0:
        await message.channel.send("Brak wyników(złe id).")
      else:
        views = response['items'][0]['statistics']['viewCount']
        await message.channel.send(userId +" ma obecnie "+views+" wyświetleń!")
    if getIdOrUsername(message.content)=='username':
      nickName = getName(message.content)
      request = youtube.channels().list(part='statistics',forUsername=nickName)
      response = request.execute()
      if response['pageInfo']['totalResults'] == 0:
        await message.channel.send("Brak wyników(zła nazwa).")
      else:
        views = response['items'][0]['statistics']['viewCount']
        await message.channel.send(nickName +" ma obecnie "+views+" wyświetleń!")
    if getIdOrUsername(message.content)!='id' and getIdOrUsername(message.content)!='username':
      await message.channel.send("Niesprecyzowany filtr szukania")
  
  if message.content.startswith('jebać'):
    await message.channel.send('disa psa orka pana smierci')

  if message.content.startswith('!help'):
    await message.channel.send('!subs id/username argument - subskrypcje(rozjebane na razie)')
    await message.channel.send('!views id/username argument- wyświetlenia(rozjebane na razie)')

  if message.content.startswith('!api'):
    await message.channel.send(rsp)


client.run(TOKEN)
