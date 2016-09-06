import json

import pokemon


class MonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, pokemon.Pokemon):
            return obj.encode_for_json()
        return json.JSONEncoder.default(self, obj)
