import requests
from py import constants


def get_poi_by_id(poi_id):
    return requests.get(constants.WWG_API + '/poi/' + poi_id)
