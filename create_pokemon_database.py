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
# types_col_name = 'types'
pkmn_col_name = 'pokemon'
species_col_name = 'species'

# We know that there exist 898 pokemon  
n_pokemon = 898

populate_pokemon = False
populate_species = False


client = pymongo.MongoClient(os.environ.get('MONGO_URI'))

if db_name not in client.list_database_names():
    print('{} not found, creating it'.format(db_name))

db = client[db_name]

if pkmn_col_name not in db.list_collection_names():
    print('{} collection not found, creating it'.format(pkmn_col_name))

pokemon = db[pkmn_col_name]

if species_col_name not in db.list_collection_names():
    print('{} collection not found, creating it'.format(species_col_name))

species = db[species_col_name]

# Populate pokemons collection
if populate_pokemon:
    pokemon_ids = range(1, n_pokemon +1)
    print("there are {} different pokemon".format(n_pokemon))

    print("Populating pokemon collection")
    for p_id in pokemon_ids:    
        print(urljoin(api_url, 'pokemon/{}/'.format(p_id)))

        res = requests.get(urljoin(api_url, 'pokemon/{}/'.format(p_id)))
        res_data = json.loads(res.text)

        data = res_data.copy()
        
        # Remove fields that wont be used for sure
        del data['sprites']
        del data['location_area_encounters']
        # We only keep species name
        data['species'] = data['species']['name']
        # Types and stats are allways the same amount so change how they are stored to keep it simpler
        del data['types']
        del data['stats']
        stats = {stat['stat']['name']: stat['base_stat'] for stat in res_data['stats']}
        
        if len(res_data['types']) > 1:
            types = {
                'type1': res_data['types'][0]['type']['name'],
                'type2': res_data['types'][1]['type']['name']
            }
        else:
            types = {
                'type1': res_data['types'][0]['type']['name'],
                'type2': None
            }      

        # Merge all data and insert
        data.update(stats)
        data.update(types)      
        pokemon.insert_one(data)
        time.sleep(0.1) # Just in case

if populate_species:
    pokemon_ids = range(387, n_pokemon +1)
    print("there are {} different pokemon species".format(n_pokemon))

    print("Populating pokemon species")
    for p_id in pokemon_ids:    
        print(urljoin(api_url, 'pokemon-species/{}/'.format(p_id)))

        res = requests.get(urljoin(api_url, 'pokemon-species/{}/'.format(p_id)))
        res_data = json.loads(res.text)

        data = res_data.copy()

        # Delete unwanted fields
        del data['egg_groups']
        del data['evolves_from_species']
        del data['flavor_text_entries']
        del data['form_descriptions']
        del data['genera']
        del data['growth_rate']
        del data['names']
        del data['pal_park_encounters']
        del data['pokedex_numbers']
        del data['varieties']
        del data['has_gender_differences']

        # Simplify some fields
        data['color'] = data['color']['name']        
        data['evolution_chain'] = data['evolution_chain']['url'].split('/')[-2]
        try:
            data['evolves_from'] = res_data['evolves_from_species']['name']
        except TypeError:
            data['evolves_from'] = None
        data['generation'] = data['generation']['name']
        try:
            data['habitat'] = data['habitat']['name']
        except TypeError:
            data['habitat'] = None
        data['gender_diff'] = res_data['has_gender_differences']
        data['shape'] = data['shape']['name']
        
        species.insert_one(data)
        time.sleep(0.1) # Just in case



