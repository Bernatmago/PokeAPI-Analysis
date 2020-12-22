import os
from os.path import join, dirname
import time

import requests
from requests.compat import urljoin
import json

from dotenv import load_dotenv

import pymongo


# Load environment variables
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

api_url = 'https://pokeapi.co/api/v2/'

db_name = 'pokebda'
types_col_name = 'types'
pkmn_col_name = 'pokemon'

populate_pokemon = False
populate_types = True


client = pymongo.MongoClient(os.environ.get('MONGO_URI'))

if db_name not in client.list_database_names():
    print('{} not found, creating it'.format(db_name))

db = client[db_name]

if types_col_name not in db.list_collection_names():
    print('{} collection not found, creating it'.format(types_col_name))

types = db[types_col_name]

if pkmn_col_name not in db.list_collection_names():
    print('{} collection not found, creating it'.format(pkmn_col_name))

pokemon = db[pkmn_col_name]

# Populate pokemons collection
if populate_pokemon:
    # We know that there exist 898 pokemon
    n_pokemon = 898
    pokemon_ids = range(1, n_pokemon +1)
    print("there are {} different pokemon".format(n_pokemon))

    print("Populating pokemon collection")
    for p_id in pokemon_ids:    
        print(urljoin(api_url, 'pokemon/{}/'.format(p_id)))

        res = requests.get(urljoin(api_url, 'pokemon/{}/'.format(p_id)))
        res_data = json.loads(res.text)

        pokemon.insert_one(res_data)
        
        time.sleep(0.2) # Just in case


