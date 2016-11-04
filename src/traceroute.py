import sys
import time

from scapy.all import *
from route import Route, avg
from geo import Geo

MAX_ITER = 30
MAX_TTL = 30

def icmp_traceroute(hostname):
    dst_ip = socket.gethostbyname(hostname)

    route = Route(dst_ip, MAX_TTL)

    t_start = time.clock()
    ttl_ = 0
    last_id = 0
    for _ in range(MAX_ITER):
        base_id = last_id

        pkts = []
        for ttl in range(1, MAX_TTL + 1):
            pkts.append(IP(dst=dst_ip, ttl=ttl) / ICMP(id=base_id+ttl))
        last_id = base_id + MAX_TTL

        try:
            ans, _ = sr(pkts, verbose=False, timeout=1)
        except socket.error as e:
            sys.exit(e)

        for snd, rcv in ans:
            # ICMP echo reply
            if rcv.type == 0:
                id = rcv[1].id
            # ICMP time exceeded
            elif rcv.type == 11:
                id = rcv[3].id

            else:
                continue

            if id < base_id + 1 or id > base_id + 30:
                continue

            rtt = (rcv.time - snd.sent_time) * 1000
            route[id - base_id].add_reply((rcv.src, rcv.type, rtt))

    # for ttl in range(1, MAX_TTL + 1):
    #     print route[ttl]

    return route

    # Para debugear o comparar
    # traceroute(dom)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        route = icmp_traceroute(sys.argv[1])
        path, std_dev = route.get_route()

        geo = Geo()


        print route.rel_rtt_mean()
        print route.rel_rtt_stddev()
        for ttl, x in path.iteritems():
            if x.no_replies():
                print ttl, '* * *'
            elif route.repeated_dst(ttl):
                break
            else:
                print ttl, x.ip(), x.abs_rtt(), x.rel_rtt(), x.rel_zrtt(), \
                geo.locate(x.ip())[0], \
                "RUTA SUBMARINA" if x.rel_zrtt() > 1.91 else ""
    else:
        print 'Te falto indicar el dominio.'
