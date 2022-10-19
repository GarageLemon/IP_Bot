from os import path

ROOT_DIR = path.dirname(path.abspath(__file__))
DOCUMENT_DIR = path.join(ROOT_DIR, 'ip_parsers')
JSON_DOCUMENT_FOR_UPLOAD_DIR = path.join(ROOT_DIR, 'json_maker', 'json_data')

ip_info_config = {
    'status': 'IP Check status',
    'message': 'IP Check message',
    'country': 'Country',
    'countryCode': 'Country Code',
    'city': 'City',
    'zip_code': 'Zip Code',
    'lat': 'Latitude',
    'lon': 'Longitude',
    'timezone': 'Timezone',
    'query': 'IP',
    'continent': 'Continent',
    'continentCode': 'Continent Code',
    'region': 'Region',
    'regionName': 'Region Name',
    'district': 'District',
    'offset': 'Timezone UTC DST offset in seconds',
    'currency': 'Currency',
    'isp': 'ISP name',
    'org': 'Organization name',
    'as_org_number_rir': 'AS number and organization, separated by space (RIR)',
    'asname_rir': 'AS name (RIR)',
    'reverse': 'Reverse DNS of the IP',
    'mobile': 'Mobile (cellular) connection',
    'proxy': 'Proxy, VPN or Tor exit address',
    'hosting': 'Hosting, colocated or data center'
}