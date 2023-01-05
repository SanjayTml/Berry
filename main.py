import os

#API-KEYS
token = os.environ['TOKEN']  #Discord api token
facts_api_key = os.environ['facts-api-key']
search_api_key = os.environ['google-search-api-key']
cse_id = os.environ['google-cse-id']

#Importing libraries
import discord
import requests
import json
# from googleapiclient.discovery import build

#Discord intent
client = discord.Client(intents=discord.Intents.default())

#Constants
limit = 1
facts_api_url = 'https://api.api-ninjas.com/v1/facts?limit={}'.format(limit)
jokes_api_url = 'https://api.chucknorris.io/jokes/random'
google_search_url = 'https://www.googleapis.com/customsearch/v1?'


#retrieve a fact using api-ninja api
def get_fact():
  response = requests.get(facts_api_url, headers={'X-Api-Key': facts_api_key})
  if response.status_code == requests.codes.ok:
    print(response.text)
    json_data = json.loads(response.text)
    return (json_data[0]['fact'])
  else:
    print("Error:", response.status_code, response.text)
    return ('Can not retrieve a fact at this moment, please try again later.')


#retrive a joke using chuck norris api
def get_joke():
  response = requests.get(jokes_api_url)
  if response.status_code == requests.codes.ok:
    print(response.text)
    json_data = json.loads(response.text)
    return (json_data['value'])
  else:
    print("Error:", response.status_code, response.text)
    return ('Can not retrieve a joke at this moment, please try again later.')


#retrieve google search using custom google search
def google_search(search_term, **kwargs):
  # service = build("customsearch", "v1", developerKey=search_api_key)
  # response = service.cse().list(q=search_term, cx=cse_id, **kwargs).execute()
  response = requests.get(google_search_url + 'key=' + search_api_key +
                          '&cx=' + cse_id + '&q=' + search_term + '&start=0')
  if response.status_code == requests.codes.ok:
    data = response.json()
    res = parse_results(data)
    return res
  else:
    print("Error:", response.status_code, response)
    return (
      'Can not retrieve search results at this moment, please try again later.'
    )

#Google search results parser
def parse_results(data):
  items = data["items"]
  output = "Search Results:\n"
  # print(data)
  for i in range(6):
    output = output + items[i]['title'] + '\n ---- \n' + items[i]['link'] + '\n ---- \n' + items[i]['snippet'] + '\n ---- \n'
  return output

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

  if message.content.startswith('search'):
    clean_messege = message.content.split('<', 1)[0]
    search_term = clean_messege.replace('search', '', 1)
    print(search_term)
    search_res = google_search(search_term)
    await message.channel.send(search_res)


client.run(token)
