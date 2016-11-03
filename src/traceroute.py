import sys
from scapy.all import *

MAX_ITER = 3

def do_syn(dom, ttl_):
    synans, _= sr(
            IP(dst=dom, ttl=ttl_) / TCP(flags=0x02),
            timeout=ttl_*0.1, verbose=False)
    for snd,rcv in synans:
        if isinstance(rcv.payload, TCP):
            return rcv.src
    return None

def icmp_traceroute(dom):
    ttl_ = 0
    found = False
    while not found and ttl_ < 30:
        ttl_ += 1
        for it in range(MAX_ITER):
            printed = False
            # verbose=False para que no tire info innecesaria.
            ans, _ = sr(
                    IP(dst=dom, ttl=ttl_) / ICMP(),
                    timeout=ttl_*0.1, verbose=False)
            for snd,rcv in ans:
                if rcv.type == 0:
                    found = True
                print ttl_, rcv.src, rcv.type
                printed = True
            if len(ans) == 0:
                syn_result = do_syn(dom, ttl_)
                if syn_result is not None:
                    print ttl_, syn_result, 'SA'
                    printed = True
                    found = True
            if not printed:
                print ttl_, '* * *'


    # Para debugear o comparar
    # traceroute(dom)


if len(sys.argv) > 1:
    icmp_traceroute(sys.argv[1])
else:
    print 'Te falto indicar el dominio.'
