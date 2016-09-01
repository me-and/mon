from collections import namedtuple
from itertools import count, product
from math import sqrt

DUST_LEVELS = [200, 400, 600, 800, 1000, 1300, 1600, 1900, 2200, 2500, 3000,
               3500, 4000, 4500, 5000, 6000, 7000, 8000, 9000, 10000]
DUST_TO_MIN_LEVEL = dict(zip(DUST_LEVELS, count(1, 2)))
DUST_TO_INTEGER_LEVELS = {k: (DUST_TO_MIN_LEVEL[k], DUST_TO_MIN_LEVEL[k] + 1)
                          for k in DUST_LEVELS}
DUST_TO_DECIMAL_LEVELS = {k: (DUST_TO_MIN_LEVEL[k] + 0.5,
                              DUST_TO_MIN_LEVEL[k] + 1.5)
                          for k in DUST_LEVELS}


class IV(namedtuple('IV', ('lvl', 'att', 'dfn', 'sta'))):

    __slots__ = ()

    @classmethod
    def possible_ivs(cls, dust, half_levels):

        levels = DUST_TO_INTEGER_LEVELS[dust]
        if half_levels:
            levels += DUST_TO_DECIMAL_LEVELS[dust]

        for att, dfn, sta in product(range(16), repeat=3):
            for level in levels:
                yield cls(level, att, dfn, sta)

    @property
    def cp_scalar(self):
        # Based on https://gaming.stackexchange.com/questions/280491
        if self.lvl <= 10:
            return ((0.01885225 * self.lvl) - 0.01001625)
        elif self.lvl <= 20:
            return ((0.01783805 * (self.lvl - 10)) + 0.17850625)
        elif self.lvl <= 30:
            return ((0.01784981 * (self.lvl - 20)) + 0.35688675)
        else:
            return ((0.00891892 * (self.lvl - 30)) + 0.53538485)

    @property
    def percentage(self):
        return self.total / 45 * 100

    @property
    def total(self):
        return self.att + self.dfn + self.sta

    def increment_level(self, jumps):
        return self._replace(lvl=(self.lvl + (0.5 * jumps)))
