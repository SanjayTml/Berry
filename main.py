import os

token = os.environ['TOKEN']

import discord

client = discord.Client(intents=discord.Intents.default())


@client.event
async def on_ready():
  print('Logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
  if message.author == client.user:
    print('Returned!')
    return

  if message.content.startswith('hello'):
    await message.channel.send('Hello {0.author.name}!'.format(message))


client.run(token)