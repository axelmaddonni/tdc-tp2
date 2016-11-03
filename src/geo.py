import pygeoip
import json
from urllib2 import urlopen
import time

API_KEY = '20b96dca8b9a5d37b0355e9461c66e76eed30a2274422fa6213d9de6ffb2b34e'

class Geo():
    def __init__(self):
        self._geoip = pygeoip.GeoIP('data/GeoLiteCity.dat')

    def locate(self, ip, use_service = False):
        try:
            if not use_service:
                raise
            query_url = 'http://api.ipinfodb.com/v3/ip-city/?key=' + \
                    API_KEY + '&ip=' + ip + '&format=json'
            response = urlopen(query_url)
            data = json.load(response)
            time.sleep(1)
            if data['statusCode'] != 'OK':
                raise
            return data['cityName'] + ', ' + data['countryName'], \
                data['latitude'], data['longitude']

        except:
            # https://github.com/maxmind/geoip-api-python/tree/master/examples
            gir = self._geoip.record_by_addr(ip)
            if gir is None or gir['country_name'] is None:
                location = '*'
            elif gir['city'] is None:
                location = gir['country_name']
            else:
                location = '%s, %s' % (gir['city'], gir['country_name'])

            latitude  = '*' if gir is None else gir['latitude']
            longitude = '*' if gir is None else gir['longitude']
            return location, latitude, longitude


