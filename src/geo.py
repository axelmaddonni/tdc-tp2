import pygeoip

class Geo():
    def __init__(self):
        self._geoip = pygeoip.GeoIP('data/GeoLiteCity.dat')

    def locate(self, ip):
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


