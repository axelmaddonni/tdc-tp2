import matplotlib.pyplot as plt
import numpy as np

from route import avg

class Graficos():
    def __init__(self, route, hostname):
        self._route = route
        self._hostname = hostname

    def hacer_grafico1(self):
        ttls = self._route.ttls_with_reply()
        datos = [self._route[ttl].abs_rtts() for ttl in ttls]
        plt.figure()
        plt.boxplot(datos, 0, 'rs', 0)
        plt.yticks(range(1,len(datos)+1), self._route[ttl].ip())
        plt.ylabel('Gateway')
        plt.xlabel('RTT (ms)')
        plt.ylim(-1, len(datos)+1)
        plt.xlim(-1, max(map(avg, datos))+50)
        plt.title('RTT absoluto - ' + self._hostname)
        plt.show()
        # RTTs para cada gateway.




