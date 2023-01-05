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
from replit import db

#Discord intent
client = discord.Client(intents=discord.Intents.default())

#Constants
facts_limit = 1
facts_api_url = 'https://api.api-ninjas.com/v1/facts?limit={}'.format(
  facts_limit)
jokes_api_url = 'https://api.chucknorris.io/jokes/random'
google_search_url = 'https://www.googleapis.com/customsearch/v1?'


#take a user-specific note
def take_note(message, user_id):
  message = '> ' + message + '\n'
  db_key = 'notes' + user_id
  if db_key in db.keys():
    notes = db[db_key]
    notes.append(message)
    db[db_key] = notes
    return "Message was sucessfully added to your notes!"
  else:
    db[db_key] = [message]
    return "A new notekeeper was created and message was added!"


#delete a user-specific note
def delete_note(index, user_id):
  db_key = 'notes' + user_id
  notes = db[db_key]
  if len(notes) > index:
    note = notes[index]
    del notes[index]
    db[db_key] = notes
    return "Following note deleted:" + note
  else:
    return "Couldn't find the index note in your notes"


#get user-specific notes
def get_notes(user_id):
  db_key = 'notes' + user_id
  if db_key in db.keys():
    notes = db[db_key]
    format_notes = append_list(notes)
    return format_notes
  else:
    return "No notes found for you. Try adding one first :)"


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
  for i in range(4):
    output = output + '```' + items[i]['title'] + '\n' + items[i][
      'link'] + '\n' + items[i]['snippet'] + '```' + '\n'
  return output


#Message parser
def parse_message(message, term):
  clean_messege = message.split('<', 1)[0]
  result = clean_messege.replace(term, '', 1)
  return result


#Append list into message
def append_list(list):
  message = 'Look what I found: \n'
  for i in range(len(list)):
    message = message + list[i]
  return message


#help message
HELP_MESSAGE = "```" + "Hi there, it\'s Berry!\n The following commands are available\n *.help* : Bring this helping message\n *.search* : Gives top google search results for the prompt followed by command\n *.fact* : Gives a random fact\n *.joke* : Gives a random Chuck Norris joke\n *.takenote* : Saves a private note in Berry\'s database\n *.notes* : Gives your private list of notes\n *.deletenote* : Deletes your note of index followed by the command\n **Thank you!**" + "```"


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

  if message.content.startswith('.hello'):
    print(message)
    await message.channel.send('Hello {0.author.name}!'.format(message))

  if '.fact' in message.content:
    fact = get_fact()
    await message.channel.send(fact)

  if message.content.startswith('.joke'):
    joke = get_joke()
    await message.channel.send(joke)

  if message.content.startswith('.search'):
    search_term = parse_message(message.content, '.search')
    print(search_term)
    search_res = google_search(search_term)
    await message.channel.send(search_res)

  if message.content.startswith('.takenote'):
    note = parse_message(message.content, '.takenote')
    print(note)
    user_id = str(message.author.id)
    status = take_note(note, user_id)
    await message.channel.send(status)

  if message.content.startswith('.notes'):
    user_id = str(message.author.id)
    notes = get_notes(user_id)
    await message.channel.send(notes)

  if message.content.startswith('.deletenote'):
    user_id = str(message.author.id)
    db_key = 'notes' + user_id
    if db_key in db.keys():
      index = int(message.content.split(".deletenote", 1)[1])
      status = delete_note(index, user_id)
      await message.channel.send(status)
    else:
      await message.channel.send("No notes found!")

  if message.content.startswith('.help'):
    await message.channel.send(HELP_MESSAGE)


client.run(token)
