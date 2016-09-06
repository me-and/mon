from collections import namedtuple
from enum import Enum


class OverallAppraisal(Enum):
    # Based on https://pokemongo.gamepress.gg/pokemon-appraisal

    # 82.2% – 100%  /  37–45
    # Overall, your Pokemon is a wonder! What a breathtaking Pokemon!
    wonder = 1
    # Overall, your Pokemon simply amazes me. It can accomplish anything!
    amazes = 1
    # Overall, your Pokemon looks like it can really battle with the best of
    # them!
    best = 1

    # 66.7% – 80%  /  30–36
    # Overall, your Pokemon has certainly caught my attention.
    attention = 2
    # Overall, your Pokemon is a strong Pokemon. You should be proud!
    # Overall, your Pokemon is really strong!
    strong = 2

    # 51.1% – 64.4%  /  23–29
    # Overall, your Pokemon is above average.
    average = 3
    # Overall, your Pokemon is a decent Pokemon.
    # Overall, your Pokemon is pretty decent!
    decent = 3

    # 0% – 48.9%  /  0–22
    # Overall, your Pokemon is not likely to make much headway in battle.
    likely = 4
    # Overall, your Pokemon may not be great in battle, but I still like it!
    like = 4
    # Overall, your Pokemon has room for improvement as far as battling goes.
    room = 4


OVERALL_APPRAISAL_MINIMUM_TOTALS = {OverallAppraisal.wonder: 37,
                                    OverallAppraisal.attention: 30,
                                    OverallAppraisal.average: 23,
                                    OverallAppraisal.likely: 0}
OVERALL_APPRAISAL_MAXIMUM_TOTALS = {OverallAppraisal.wonder: 45,
                                    OverallAppraisal.attention: 36,
                                    OverallAppraisal.average: 29,
                                    OverallAppraisal.likely: 22}


class TopIV(Enum):
    # Based on https://pokemongo.gamepress.gg/pokemon-appraisal

    # 15
    # Its stats exceed my calculations. It's incredible!
    exceed = 1
    # I'm blown away by its stats. WOW!
    blown = 1
    # Its stats are the best I've ever seen! No doubt about it!
    best = 1

    # 13–14
    # I am certainly impressed by its stats, I must say.
    impressed = 2
    # It's got excellent stats! How exciting!
    excellent = 2
    # Its stats are really strong! Impressive.
    strong = 2

    # 8–12
    # Its stats are noticeably trending to the positive.
    trending = 3
    # Its stats indicate that in battle, it'll get the job done.
    job = 3
    # It's definitely got some good stats. Definitely!
    good = 3

    # 0-7
    # Its stats are not out of the norm, in my estimation.
    norm = 4
    # Its stats don't point to greatness in battle.
    point = 4
    # Its stats are all right, but kinda basic, as far as I can see.
    basic = 4

IV_APPRAISAL_MINIMUM_VALUE = {TopIV.exceed: 15,
                              TopIV.impressed: 13,
                              TopIV.trending: 8,
                              TopIV.norm: 0}
IV_APPRAISAL_MAXIMUM_VALUE = {TopIV.exceed: 15,
                              TopIV.impressed: 14,
                              TopIV.trending: 12,
                              TopIV.norm: 7}


class Appraisal(namedtuple('Appraisal', ('overall', 'top_att', 'top_dfn',
                                         'top_hp', 'top_iv'))):

    __slots__ = ()

    def valid_iv(self, iv):
        if iv.total < OVERALL_APPRAISAL_MINIMUM_TOTALS[self.overall]:
            return False
        if iv.total > OVERALL_APPRAISAL_MAXIMUM_TOTALS[self.overall]:
            return False

        top_iv = max(iv.att, iv.dfn, iv.sta)

        if top_iv < IV_APPRAISAL_MINIMUM_VALUE[self.top_iv]:
            return False
        if top_iv > IV_APPRAISAL_MAXIMUM_VALUE[self.top_iv]:
            return False

        if self.top_att and top_iv != iv.att:
            return False
        if not self.top_att and top_iv == iv.att:
            return False
        if self.top_dfn and top_iv != iv.dfn:
            return False
        if not self.top_dfn and top_iv == iv.dfn:
            return False
        if self.top_hp and top_iv != iv.sta:
            return False
        if not self.top_hp and top_iv == iv.sta:
            return False

        return True

    def encode_for_json(self):
        return {'Overall': self.overall.name,
                'Att': self.top_att,
                'Def': self.top_dfn,
                'HP': self.top_hp,
                'Stats': self.top_iv.name}

    @staticmethod
    def looks_like_json_obj(dct):
        if dct is None:
            return True
        return (isinstance(dct, dict) and
                len(dct) == 5 and
                'Overall' in dct and 'Att' in dct and 'Def' in dct and
                'HP' in dct and 'Stats' in dct)

    @classmethod
    def decode_from_json(cls, dct):
        if dct is None:
            return None
        return cls(OverallAppraisal[dct['Overall']],
                   dct['Att'], dct['Def'], dct['HP'],
                   TopIV[dct['Stats']])
