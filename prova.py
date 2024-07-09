import requests
import json

import TestDrive


# def get_speed_limit(latitude, longitude):
#     overpass_url = "http://overpass-api.de/api/interpreter"
#     overpass_query = """
#     [out:json];
#     way(around:10, {latitude}, {longitude})["maxspeed"];
#     out body;
#     """.format(latitude=latitude, longitude=longitude)
#
#     response = requests.get(overpass_url, params={'data': overpass_query})
#
#     if response.status_code == 200:
#         data = response.json()
#         if 'elements' in data and len(data['elements']) > 0:
#             max_speed = data['elements'][0].get('tags', {}).get('maxspeed', 'Unknown')
#             return max_speed
#         else:
#             return 'Speed limit not found'
#     else:
#         return 'Error fetching data'
#
#
# # Esempio di utilizzo:
# latitude = 40.3159422
# longitude = 18.0786997

#speed_limit = get_speed_limit(latitude, longitude)
#print("Limite di velocità:", speed_limit)
