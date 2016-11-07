# tdc-tp2
tdc-tp2 2c 2016

## Como usar

Primero hay que setear las capabilities de python:

    sudo setcap cap_net_raw=eip /usr/bin/python2.7

Cambien python2.7 por como se llame su binario de python. Luego, pueden ejecutar el programa normalmente,

    python2 src/traceroute.py www.google.com

Si quieren que tarde menos en correr, cambien `MAX_ITER` dentro de `traceroute.py`. Es importante que se corra desde `.` y no desde `src` para que pueda acceder a la carpeta data.

### Requerimientos


Generales:

* scapy


Localizacion:

* pygeoip

Tau de Thompson:

* scipy


Generar gráficos:

* libgeos (para basemap). Se puede obtener del package manager de su distribución (en caso de tenerla), o compilando el source.
Si se obtiene del package manager, puede haber un problema al linkear (al menos en Ubuntu se presentó este problema), ya que busca la librería "libgeos.so", pero se instala como "libgeos-3.4.2.so"; una solución es generar un symlink ("sudo ln -s /usr/lib/libgeos-3.4.2.so /usr/lib/libgeos.so").
Para compilar:

wget http://download.osgeo.org/geos/geos-3.4.2.tar.bz2
tar xjf geos-3.4.2.tar.bz2
cd geos-3.4.2
./configure
make
sudo make install
export GEOS_DIR="/usr/local/lib"

* basemap

* numpy

* matplotlib



Todo eso se puede instalar corriendo

    make install-deps



## Universidades

* Gonza: www.es.osaka-u.ac.jp

### TODO

* informe

