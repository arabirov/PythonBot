from py.api import *


def poi_id_message(poi_id):
    if poi_id == 0:
        return "Please use only digit IDs that > 0"
    else:
        result = get_poi_by_id(poi_id).json()
        if result['success']:
            name = result['data']['poi']['name']
            return name
        else:
            return "Oopsie! Try different POI."
