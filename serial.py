import json

import pokemon


class MonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, pokemon.Pokemon):
            return obj.encode_for_json()
        return json.JSONEncoder.default(self, obj)


def mon_hook(dct):
    if pokemon.Pokemon.looks_like_json_dct(dct):
        return pokemon.Pokemon.decode_from_json(dct)
    else:
        return dct
