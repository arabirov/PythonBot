from py.api import *
import requests


def poi_id_message(poi_id):
    if poi_id == 0:
        return "Please use only digit IDs that > 0"
    try:
        result = get_poi_by_id(poi_id).json()
        print(result)
        poi_info = result['data']['poi']
        image_url = requests.get(poi_info['images'][0]['originalUrl'])
        name = poi_info['name']
        description = poi_info['description']
        category = poi_info['category']['name']
        address = poi_info['formattedAddress']
        email = poi_info['email']
        phone = poi_info['phone']
        web = poi_info['web']
        image = image_url.content
        return [f"""POI Name: <b>{name}</b>\nPOI Description: <b>{description}</b>\nPOI Category: <b>{category}</b
            >\nPOI Address: <b>{address}</b>\nEmail: <b>{email}</b>\nPhone: <b>{phone}</b>\nWebsite: <b>{web}</b>""",
                image]
    except AttributeError:
        return get_poi_by_id(poi_id)
