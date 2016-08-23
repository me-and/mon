import json

SPECIES_FILE = 'species.json'


class Species(object):

    '''A species of Pokémon.'''

    __slots__ = ('name', 'num', 'att', 'dfn', 'sta')

    def __init__(self, name, num, att, dfn, sta):
        self.name = name
        self.num = num
        self.att = att
        self.dfn = dfn
        self.sta = sta

    def __repr__(self):
        return '{}({!r}, {!r}, {!r}, {!r}, {!r})'.format(
            self.__class__.__name__,
            self.name,
            self.num,
            self.att,
            self.dfn,
            self.sta)

    def __str__(self):
        return self.name

    def __eq__(self, other):
        return (self.name == other.name and
                self.num == other.num and
                self.att == other.att and
                self.dfn == other.dfn and
                self.sta == other.sta)

    def __hash__(self):
        return (hash(self.name) ^
                hash(self.num) ^
                (hash(self.att) << 8) ^
                (hash(self.dfn) << 16))


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
