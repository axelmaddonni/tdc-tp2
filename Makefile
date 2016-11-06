PIP = pip2
PIP_OPTIONS = install --user

.PHONY = install-deps

install-deps:
	$(PIP) $(PIP_OPTIONS) matplotlib
	$(PIP) $(PIP_OPTIONS) numpy
	$(PIP) $(PIP_OPTIONS) pygeoip
	$(PIP) $(PIP_OPTIONS) scapy
	$(PIP) $(PIP_OPTIONS) scipy
	$(PIP) $(PIP_OPTIONS) -Iv https://sourceforge.net/projects/matplotlib/files/matplotlib-toolkits/basemap-1.0.7/basemap-1.0.7.tar.gz/download
