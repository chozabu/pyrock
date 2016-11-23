"""Foobar.py: Description of what foobar does."""

__author__ = "Alex 'Chozabu' P-B"
__copyright__ = "Copyright 2016, Chozabu"

machine_name = "unknown"
pkey = "unknown"
running = True
ui_port = 8080
auto_accept = True
ext_ip = None

try:
    from urllib.request import urlopen

    ext_ip = urlopen('http://ip.42.pl/raw').read()
    print("detected IP as", ext_ip)
except:
    print("could not get external IP")
