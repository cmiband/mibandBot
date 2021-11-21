import discord
from googleapiclient.discovery import build
import os
import unicodedata
from random import seed
from random import randint

seed(1)

TOKEN = os.environ['TOKEN']
ytAPI = os.environ['YT']

client = discord.Client()
youtube = build('youtube','v3',developerKey=ytAPI)

def getName(msg):
  return msg.split()[2]

def getIdOrUsername(msg):
  return msg.split()[1]

def makeLink(part):
  return "https://www.youtube.com/watch?v="+part

def normalize_caseless(text):
    return unicodedata.normalize("NFKD", text.casefold())

def caseless_equal(left, right):
    return normalize_caseless(left) == normalize_caseless(right)

#ty stackoverflow <3
def find_channel_by_custom_url(
        youtube, custom_url, max_results = 10):
    resp = youtube.search().list(
        q = custom_url,
        part = 'id',
        type = 'channel',
        fields = 'items(id(kind,channelId))',
        maxResults = max_results
    ).execute()
    assert len(resp['items']) <= max_results

    ch = []
    for item in resp['items']:
        assert item['id']['kind'] == 'youtube#channel'
        ch.append(item['id']['channelId'])

    if not len(ch):
        return None

    resp = youtube.channels().list(
        id = ','.join(ch),
        part = 'id,snippet',
        fields = 'items(id,snippet(customUrl))',
        maxResults = len(ch)
    ).execute()
    assert len(resp['items']) <= len(ch)
    
    for item in resp['items']:
        url = item['snippet'].get('customUrl')
        if url is not None and \
            caseless_equal(url, custom_url):
            assert item['id'] is not None
            return item['id']

    return None

@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
  if message.author == client:
    return

  if message.author.name == "DZiX":
    await message.author.send("Stop spamming")

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
      channelId = find_channel_by_custom_url(youtube,nickName)
      if channelId is not None:
        request = youtube.channels().list(part='statistics',id=channelId)
        response = request.execute()
        subs = response['items'][0]['statistics']['subscriberCount']
        await message.channel.send(nickName +" ma obecnie "+subs+" subów!")
      else:
        await message.channel.send("Brak wyników(zła nazwa)")
  
  if message.content.startswith('!views'):
    if getIdOrUsername(message.content)=='id':
      userId = getName(message.content)
      request = youtube.channels().list(part='statistics',id=userId)
      requestName = youtube.channels().list(part='snippet',id=userId)
      response = request.execute()
      responseName = requestName.execute()
      if response['pageInfo']['totalResults'] == 0:
        await message.channel.send("Brak wyników(złe id).")
      else:
        views = response['items'][0]['statistics']['viewCount']
        channelName = responseName['items'][0]['snippet']['title']
        await message.channel.send(channelName +" ma obecnie "+views+" wyświetleń!")
    if getIdOrUsername(message.content)=='username':
      nickName = getName(message.content)
      channelId = find_channel_by_custom_url(youtube,nickName)
      if channelId is not None:
        request = youtube.channels().list(part='statistics', id=channelId)
        response = request.execute()
        views = response['items'][0]['statistics']['viewCount']
        await message.channel.send(nickName +" ma obecnie "+views+" wyświetleń!")
      else:
        await message.channel.send("Brak wyników(zła nazwa).")  
  
  if message.content.startswith('jebać'):
    await message.channel.send('disa psa orka pana smierci')

  if message.content.startswith('!miband'):
    await message.channel.send("https://www.youtube.com/channel/UC_KcYKZtzAgZwXczRcI55lw")

  if message.content.startswith('!montage'):
    request = youtube.playlistItems().list(part="snippet",playlistId="PLUQBK_ASrqgvnii8HJS_k1bfCX7G8KvUm")
    requestForLink = youtube.playlistItems().list(part='contentDetails',playlistId='PLUQBK_ASrqgvnii8HJS_k1bfCX7G8KvUm')
    responseForLinkPart = requestForLink.execute()
    rsp = request.execute() 
    playlistLen = len(rsp['items'])
    newestLinkPart = responseForLinkPart['items'][playlistLen-1]['contentDetails']['videoId']
    newestMontage = rsp['items'][playlistLen-1]['snippet']['title']
    await message.channel.send("Najnowszy montage: " +newestMontage + "\n" +makeLink(newestLinkPart))

  if message.content.startswith('!monke'):
    val = randint(100,1000);
    await message.channel.send("https://www.placemonkeys.com/"+str(val))

  if message.content.startswith('!help'):
    await message.channel.send('!subs id/username argument - subskrypcje(rozjebane na razie)')
    await message.channel.send('!views id/username argument- wyświetlenia(rozjebane na razie)')
    await message.channel.send('"!miband" - ja B)')
    await message.channel.send('"!montage" - najnowszy montage(nie wiem czemu nie wyswietla najnowszego)')
    await message.channel.send('"!monke" - monke OOH OOH A A')

client.run(TOKEN)
