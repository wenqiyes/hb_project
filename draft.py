import requests

GEOCODING_API_KEY = 'AIzaSyDIkaVpykXxXb2I6HA360qobU_iYSd9hy0'
GEOCODING_URL = "https://maps.googleapis.com/maps/api/geocode/json?"
NAME_PARAMS = {
  'address': 'Eagan',
  'key': GEOCODING_API_KEY
}

first_response = requests.get(url=GEOCODING_URL,
                             params= NAME_PARAMS).json()
# print(first_response)
lat = first_response['results'][0]['geometry']['location']['lat']

LAT_PARAM = {
  'address': 'Eagan',
  'key': GEOCODING_API_KEY
}

