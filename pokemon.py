from collections import namedtuple
from math import sqrt

import iv


StartSnapshot = namedtuple('StartSnapshot',
                           ('species', 'cp', 'hp', 'dust', 'half_levels'))
PowerUpSnapshot = namedtuple('PowerUpSnapshot',
                             ('cp', 'hp', 'dust', 'power_ups'))
EvolutionSnapshot = namedtuple('EvolutionSnapshot',
                               ('species', 'cp', 'hp', 'dust', 'power_ups'))


class Pokemon(object):
    def __init__(self, snapshots, name=None):
        self.snapshots = snapshots
        self._name = name

    @classmethod
    def new(cls, species, cp, hp, dust, name=None, half_levels=False):
        snapshot = StartSnapshot(species, cp, hp, dust, half_levels)
        return cls([snapshot], name=name)

    def power_up(self, cp, hp, dust, power_ups=1):
        snapshot = PowerUpSnapshot(cp, hp, dust, power_ups)
        self.snapshots.append(snapshot)

    def evolve(self, species, cp, hp, dust, power_ups=0):
        snapshot = EvolutionSnapshot(species, cp, hp, dust, power_ups)
        self.snapshots.append(snapshot)

    @property
    def species(self):
        for snapshot in self.snapshots[::-1]:
            try:
                return snapshot.species
            except AttributeError:  # Didn't have a species attribute
                continue

    @property
    def name(self):
        if self._name is None:
            return self.species.name
        else:
            return self._name

    def rename(self, name):
        self._name = name

    @staticmethod
    def calc_cp(species, iv):
        # Based on
        # https://docs.google.com/spreadsheets/d/1wbtIc33K45iU1ScUnkB0PlslJ-eLaJlSZY47sPME2Uk
        # by /u/aggixx
        species.att
        iv.att
        cp = int((species.att + iv.att) *
                 sqrt(species.dfn + iv.dfn) *
                 sqrt(species.sta + iv.sta) *
                 iv.cp_scalar / 10)
        return max(cp, 10)

    @staticmethod
    def calc_hp(species, iv):
        # Based on
        # https://docs.google.com/spreadsheets/d/1wbtIc33K45iU1ScUnkB0PlslJ-eLaJlSZY47sPME2Uk
        # by /u/aggixx
        hp = int((species.sta + iv.sta) * sqrt(iv.cp_scalar))
        return max(hp, 10)

    def calc_ivs(self):
        for snapshot in self.snapshots:
            try:
                species = snapshot.species
            except AttributeError:
                # This snapshot doesn't define a new species, so just continue
                # using the previous value (and assume something will have set
                # the value previously).
                pass

            if isinstance(snapshot, StartSnapshot):
                possible_ivs = iv.IV.possible_ivs(
                    snapshot.dust, snapshot.half_levels)
            else:
                possible_ivs = {iv.increment_level(snapshot.power_ups)
                                for iv in possible_ivs}

            possible_ivs = {iv for iv in possible_ivs if
                            self.calc_cp(species, iv) == snapshot.cp and
                            self.calc_hp(species, iv) == snapshot.hp}

        return possible_ivs
