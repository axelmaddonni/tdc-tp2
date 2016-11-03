from collections import defaultdict
import math

def avg(l):
    return sum(map(float, l)) / len(l)

def analyze_rtts(responses):
    ips = defaultdict(list)
    for x in responses:
        ips[x[0]].append(x[2])
    best_ip = ''
    best_rtts = []
    for ip, rtts in ips.iteritems():
        if len(rtts) > len(best_rtts):
            best_ip = ip
            best_rtts = rtts
    if len(best_rtts) == 0:
        return None
    else:
        return (best_ip, avg(best_rtts))


class Route:
    def __init__(self, dst_ip=None, max_ttl=None):
        self.dst_ip = dst_ip
        self._hops = defaultdict(list)
        self._max_ttl = max_ttl

    def __getitem__(self, ttl):
        return self._hops[ttl]


    def get_route(self):
        path = {}
        for ttl in range(1, self._max_ttl + 1):
            responses = self._hops[ttl]
            path[ttl] = analyze_rtts(responses)
            if all(map(lambda x: x[1] == 0, responses)) and len(responses) > 0:
                break
        last_rtt = 0.0
        rtts = []
        for ttl, x in path.iteritems():
            if x is not None:
                path[ttl] = (x[0], x[1], max(0.0, x[1] - last_rtt))
                rtts.append(max(0.0, x[1] - last_rtt))
                last_rtt = x[1]
        x_avg = avg(rtts)
        std_dev = math.sqrt(avg(map(lambda x_i: (x_i - x_avg)**2.0, rtts)))
        for ttl, x in path.iteritems():
            if x is not None:
                path[ttl] = (x[0], x[1], x[2], (x[2] - x_avg) / std_dev)
        return path, std_dev

