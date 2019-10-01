import requests
from py import constants


def get_poi_by_id(poi_id):
    if requests.get(constants.WWG_API + '/poi/' + poi_id).status_code == 200:
        return requests.get(constants.WWG_API + '/poi/' + poi_id)
    else:
        return "Oopsie! POI doesn't exist or not approved yet. Try different POI."
