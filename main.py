import os

#API-KEYS
token = os.environ['TOKEN']
facts_api_key = os.environ['facts-api-key']

#Importing libraries
import discord
import requests
import json

#Discord intent
client = discord.Client(intents=discord.Intents.default())

#Constants
limit = 1
facts_api_url = 'https://api.api-ninjas.com/v1/facts?limit={}'.format(limit)
jokes_api_url = 'https://api.chucknorris.io/jokes/random'


#retrieve a fact using api call
def get_fact():
  response = requests.get(facts_api_url, headers={'X-Api-Key': facts_api_key})
  if response.status_code == requests.codes.ok:
    print(response.text)
    json_data = json.loads(response.text)
    return (json_data[0]['fact'])
  else:
    print("Error:", response.status_code, response.text)
    return ('Can not retrieve a fact at this moment, please try again later.')


#retrive a joke using api callable
def get_joke():
  response = requests.get(jokes_api_url)
  if response.status_code == requests.codes.ok:
    print(response.text)
    json_data = json.loads(response.text)
    return (json_data['value'])
  else:
    print("Error:", response.status_code, response.text)
    return ('Can not retrieve a joke at this moment, please try again later.')


#bot online event listener
@client.event
async def on_ready():
  print('Logged in as {0.user}'.format(client))


#message event listener
@client.event
async def on_message(message):
  if message.author == client.user:
    print('Returned!')
    return

  if message.content.startswith('hello'):
    await message.channel.send('Hello {0.author.name}!'.format(message))

  if 'fact' in message.content:
    fact = get_fact()
    await message.channel.send(fact)

  if message.content.startswith('joke'):
    joke = get_joke()
    await message.channel.send(joke)


client.run(token)
