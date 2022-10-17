from os import path

ROOT_DIR = path.dirname(path.abspath(__file__))
DOCUMENT_DIR = path.join(ROOT_DIR, 'ip_parsers')

base_ip_info_config = {
    'status': 'IP Check status',
    'message': 'IP Check message',
    'country': 'Country',
    'countryCode': 'Country Code',
    'city': 'City',
    'zip_code': 'Zip Code',
    'lat': 'Latitude',
    'lon': 'Longitude',
    'timezone': 'Timezone',
    'query': 'IP'
}