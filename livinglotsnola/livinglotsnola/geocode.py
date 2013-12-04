import requests


NOMINATIM_BASE_URL = 'http://nominatim.openstreetmap.org/search'


def nominatim(street=None, city=None, state=None, country='us'):
    """
    Simple geocoding with OpenStreetMap's Nominatim:

        http://nominatim.openstreetmap.org/

    """
    params = {
        'format': 'json',
        'street': street,
        'city': city,
        'state': state,
        'country': country,
    }
    r = requests.get(NOMINATIM_BASE_URL, params=params)
    result = r.json()[0]
    return {
        'lat': float(result['lat']),
        'lon': float(result['lon']),
    }
