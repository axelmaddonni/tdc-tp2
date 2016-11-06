fallo_importar_graficos = False

try:
    import matplotlib.pyplot as plt
    import numpy as np
    from mpl_toolkits.basemap import Basemap
except:
    print 'Te olvidaste de instalar las dependencias! No se van a generar ' \
        'los graficos'
    print 'Corre'
    print '    make install-deps'
    print ''
    fallo_importar_graficos = True




from route import avg

class Graficos():
    def __init__(self, route, hostname):
        self._route = route
        self._hostname = hostname

    def _gateway_name(self, ttl):
        return self._route[ttl].location().city() + '\n' + self._route[ttl].ip()

    def _bordes_mapa(lon, lats):
	for i in range(len(lons)):
	    lons[i] = lons[i] % 360
	w = max(lons) - min(lons)
	h = max(lats) - min(lats)
	llcrnrlon = min(lons) - w * 0.1
	llcrnrlat = min(lats) - h * 0.1
	urcrnrlon = max(lons) + w * 0.1
	urcrnrlat = max(lats) + h * 0.1
	return llcrnrlon, llcrnrlat, urcrnrlon, urcrnrlat


    def hacer_grafico1(self):
        # RTTs para cada gateway.
        ttls = self._route.ttls_with_reply()
        datos = [self._route[ttl].abs_rtts() for ttl in ttls]

        plt.figure(figsize=(20,10))
        plt.boxplot(datos, 0, 'rs', 0)
        plt.yticks(range(1,len(datos)+1), map(self._gateway_name, ttls), rotation='horizontal')
        plt.ylabel('Gateway')
        plt.xlabel('RTT (ms)')
        plt.ylim(0, len(datos) + 1)
        plt.xlim(-1, max(map(avg, datos))+50)
        plt.title('RTTs - ' + self._hostname)
        plt.tight_layout()
        plt.savefig ('grafico1-'+self._hostname.replace('.', '-')+'.pdf')


    def hacer_grafico2(self, tau):
        # ZRTT para cada gateway.
        ttls = self._route.ttls_with_reply()
        datos = [self._route[ttl].rel_zrtt() for ttl in ttls]


        plt.figure(figsize=(15,8))
        plt.barh(range(len(datos)), datos)
        plt.yticks(map(lambda x: x+0.5, range(len(datos))), map(self._gateway_name, ttls), rotation='horizontal')
        plt.ylabel('Gateway')
        plt.xlabel('ZRTT')
        plt.ylim(-1, len(datos)+1)
        plt.xlim(-1, max(datos)*1.25)
        plt.title('ZRTT - ' + self._hostname)
        plt.axvline(x = tau, ymin = 0, ymax = len(datos),color='g', ls='--',
                label='Tau = '+str(round(tau,3)))
        plt.legend()
        plt.tight_layout()
        plt.savefig ('grafico2-'+self._hostname.replace('.', '-')+'.pdf')


    def hacer_grafico3(self):
        # Mapa del traceroute.
        plt.figure()
        ttls = self._route.ttls_with_reply()
        lons, lats = [], []
        for ttl in ttls:
            loc = self._route[ttl].location()
            if loc.longitude() == '0' and loc.latitude() == '0':
                continue
            lons.append(float(loc.longitude()) % 360)
            lats.append(float(loc.latitude()))
	w = max(lons) - min(lons)
	h = max(lats) - min(lats)
	llcrnrlon = min(lons) - w * 0.1
	llcrnrlat = min(lats) - h * 0.1
	urcrnrlon = max(lons) + w * 0.1
	urcrnrlat = max(lats) + h * 0.1

        # http://matplotlib.org/basemap/users/examples.html
        mapa = Basemap(projection='cyl',
            llcrnrlon=llcrnrlon, llcrnrlat=llcrnrlat,
            urcrnrlon=urcrnrlon, urcrnrlat=urcrnrlat)

        last_ttl = 1

        for ttl in ttls[1:]:
            loc1 = self._route[last_ttl].location()
            loc2 = self._route[ttl].location()
            if loc2.latitude() == '0' and loc2.longitude() == '0':
                continue
            elif loc1.latitude() == '0' and loc1.longitude() == '0':
                last_ttl = ttl
                continue
            xs = []
            ys = []
            for l in [loc1, loc2]:
                x, y = mapa(float(l.longitude())%360, float(l.latitude()))
                xs.append(x)
                ys.append(y)

            mapa.plot(xs, ys, linewidth=2, color='b')
            mapa.plot(xs, ys, 'go')
            mapa.plot(float(loc2.longitude())%360, float(loc2.latitude()))
            last_ttl = ttl
        mapa.drawcoastlines()
        mapa.fillcontinents()

        plt.title('Traceroute - ' + self._hostname)
        plt.savefig('grafico3-'+self._hostname.replace('.', '-')+'.pdf')



