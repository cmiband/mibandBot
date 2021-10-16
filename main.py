import discord
from googleapiclient.discovery import build
import os

val = os.environ['TOKEN']
ytAPI = os.environ['YT']

userId = "UC_KcYKZtzAgZwXczRcI55lw"

client = discord.Client()
youtube = build('youtube','v3',developerKey=ytAPI)

request = youtube.channels().list(part='statisics',id=userId)
response = request.execute()
print(response)

@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
  if message.author == client:
    return

  if message.content.startswith('$hello'):
    await message.channel.send('Hello!')

client.run(val)
