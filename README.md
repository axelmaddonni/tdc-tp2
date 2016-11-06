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

* basemap

* numpy

* matplotlib



Todo eso se puede instalar corriendo

    make install-deps



## Universidades

* Gonza: www.es.osaka-u.ac.jp

### TODO

* informe

