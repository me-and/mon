import json
from collections import namedtuple

SPECIES_FILE = 'species.json'

Species = namedtuple('Species', ('name', 'num', 'att', 'dfn', 'sta'))

# Populate the records of extant species.  For simplicity, `species` will index
# by both name and number, so `species['Bulbasaur']` and `species[1]` will both
# work.
species = {}

with open(SPECIES_FILE) as species_file:
    for stats in json.load(species_file):
        pokemon = Species(stats['Name'],
                          stats['#'],
                          stats['Att'],
                          stats['Def'],
                          stats['Sta'])
        species[pokemon.num] = pokemon
        species[pokemon.name] = pokemon

# Clean up temporary variables.
del pokemon, species_file
