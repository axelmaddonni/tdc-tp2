import sys
import time

from scapy.all import *
from route import Route, avg
from geo import Geo, fallo_importar_geo
from graficos import Graficos, fallo_importar_graficos
from outliers import thompson_tau, fallo_importar_stats


MAX_ITER = 30
MAX_TTL = 30

def icmp_traceroute(hostname):
    dst_ip = socket.gethostbyname(hostname)

    route = Route(dst_ip, MAX_TTL)

    t_start = time.clock()
    ttl_ = 0
    last_id = 0
    for i in range(MAX_ITER):
        sys.stdout.write('Enviando...  %s / %s      \r' % \
                (str(i+1).zfill(2), str(MAX_ITER).zfill(2)))
        sys.stdout.flush()
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
            if rcv.type == 0: id = rcv[1].id
            # ICMP time exceeded
            elif rcv.type == 11: id = rcv[3].id
            else: continue

            if id < base_id + 1 or id > base_id + 30:
                continue

            rtt = (rcv.time - snd.sent_time) * 1000
            route[id - base_id].add_reply((rcv.src, rcv.type, rtt))
    print ''

    # for ttl in range(1, MAX_TTL + 1):
    #     print route[ttl]

    return route

    # Para debugear o comparar
    # traceroute(dom)


if __name__ == '__main__':

    tau = thompson_tau(MAX_ITER)
    if len(sys.argv) > 1:
        hostname = sys.argv[1]
        route = icmp_traceroute(hostname)
        path, std_dev = route.get_route()

        print route.rel_rtt_mean()
        print route.rel_rtt_stddev()
        for ttl, x in path.iteritems():
            if x.no_replies():
                print ttl, '* * *'
            elif route.repeated_dst(ttl):
                break
            else:
                # Es ruta submarina
                es_sub = False if fallo_importar_stats else x.rel_zrtt() > tau

                print ttl, x.ip(), \
                    round(x.abs_rtt(), 3), \
                    round(x.rel_rtt(), 3), \
                    round(x.rel_zrtt(), 3), \
                    x.location().city(), \
                    "RUTA SUBMARINA" if es_sub else ""

        if not fallo_importar_graficos:
            gr = Graficos(route, hostname)
            gr.hacer_grafico1()
            gr.hacer_grafico2()
            if not fallo_importar_geo:
                gr.hacer_grafico3()

    else:
        print 'Te falto indicar el dominio.'
