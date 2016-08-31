import json
from collections import namedtuple

SPECIES_FILE = 'species.json'

Species = namedtuple('Species', ('name', 'num', 'att', 'dfn', 'sta'))

# Populate the records of extant species.
species = []
species_by_number = {}
species_by_name = {}

with open(SPECIES_FILE) as species_file:
    for stats in json.load(species_file):
        pokemon = Species(stats['Name'],
                          stats['#'],
                          stats['Att'],
                          stats['Def'],
                          stats['Sta'])
        species.append(pokemon)
        species_by_number[pokemon.num] = pokemon
        species_by_name[pokemon.name] = pokemon

# Clean up temporary variables.
del pokemon, species_file
