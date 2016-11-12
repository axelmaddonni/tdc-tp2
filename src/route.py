from collections import defaultdict
import math

from geo import Geo

# RTT absoluto quiere decir desde mi pc hasta el hop i.
# RTT relativo (o RTT a secas) quiere decir desde el hop i-1 hasta el hop i.

def avg(l):
    return sum(map(float, l)) / len(l)

global_geo = Geo()

class Location():
    def __init__(self, ip):
        self._ip = ip

        location = global_geo.locate(ip)
        self._city = location[0]
        self._latitude = location[1]
        self._longitude = location[2]

    def city(self):
        return self._city

    def latitude(self):
        return self._latitude

    def longitude(self):
        return self._longitude

class Hop():
    def __init__(self, ttl, route):
        self._ttl = ttl
        self._replies = []
        self._route = route
        self._ip = ''
        self._location = None

    def location(self):
        if self._location is None:
            self._location = Location(self._ip)
        return self._location

    def _get_ip_and_absolute_rtts(self):
        ips = defaultdict(list)
        for x in self._replies:
            ips[x[0]].append(x[2])
        best_ip = ''
        best_rtts = []
        for ip, rtts in ips.iteritems():
            if len(rtts) > len(best_rtts):
                best_ip = ip
                best_rtts = rtts
        self._ip = best_ip
        return best_rtts

    def ip(self):
        return self._ip

    def no_replies(self):
        return len(self._replies) == 0

    def is_dst(self):
        # Todas las replies son echo reply.
        return all(map(lambda x: x[1] == 0, self._replies)) and \
                len(self._replies) > 0

    def add_reply(self, r):
        self._replies.append(r)

    def abs_rtts(self):
        return self._get_ip_and_absolute_rtts()

    def abs_rtt(self):
        rtts = self.abs_rtts()
        return 0 if len(rtts) == 0 else avg(rtts)

    def rel_rtt(self):
        if self._ttl == 1:
            return self.abs_rtt()
        else:
            prev = self._ttl - 1
            while self._route[prev].no_replies() and prev > 1: prev -= 1
            return max(0.0, self.abs_rtt() - self._route[prev].abs_rtt())

    def rel_rtts(self):
        if self._ttl == 1:
            return self.abs_rtts()
        else:
            prev = self._ttl - 1
            while self._route[prev].no_replies() and prev > 1: prev -= 1
            return map(lambda x: x - self._route[prev].abs_rtt(), self.abs_rtts())

    def rel_zrtt(self):
        return (self.rel_rtt() - self._route.rel_rtt_mean()) / self._route.rel_rtt_stddev()


class Route:
    def __init__(self, dst_ip=None, max_ttl=None):
        self.dst_ip = dst_ip
        # En _hops hay triplas (ip origen, tipo de respuesta, tiempo)
        self._hops = {ttl : Hop(ttl, self) for ttl in range(1, max_ttl + 1)}
        self._max_ttl = max_ttl

    def __getitem__(self, ttl):
        return self._hops[ttl]

    def repeated_dst(self, ttl):
        return ttl > 1 and (self[ttl].is_dst() and self[ttl-1].is_dst())

    def valid(self, ttl):
        return (not self[ttl].no_replies()) and (not self.repeated_dst(ttl))

    def ttls_with_reply(self):
        return [ttl for ttl in range(1, self._max_ttl + 1) if self.valid(ttl)]

    def rel_rtt_mean(self):
        return avg([self[ttl].rel_rtt() for ttl in self.ttls_with_reply()])

    def rel_rtt_stddev(self):
        rtt_mean = self.rel_rtt_mean()
        ttls = self.ttls_with_reply()
        return math.sqrt(
            sum([(self[ttl].rel_rtt() - rtt_mean)**2 for ttl in ttls]) / len(ttls))

    def get_route(self):
        return self._hops, self.rel_rtt_stddev()

