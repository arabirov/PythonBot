from py.api import *
from io import BytesIO, StringIO
from PIL import Image
import requests


def poi_id_message(poi_id):
    if poi_id == 0:
        return "Please use only digit IDs that > 0"
    else:
        result = get_poi_by_id(poi_id).json()
        print(result)
        if result['success']:
            poi_info = result['data']['poi']
            image_url = requests.get(poi_info['images'][0]['originalUrl'])
            name = poi_info['name']
            description = poi_info['description']
            category = poi_info['category']['name']
            address = poi_info['formattedAddress']
            email = poi_info['email']
            phone = poi_info['phone']
            image = Image.open(BytesIO(image_url.content))  # TODO Fix images
            image.close()
            return [f"""POI Name: <b>{name}</b>\nPOI Description: <b>{description}</b>\nPOI Category: <b>{category}</b
            >\nPOI Address: <b>{address}</b>\nEmail: <b>{email}</b>\nPhone: <b>{phone}</b>""", image]
        else:
            return "Oopsie! Try different POI."
