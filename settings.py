"""Foobar.py: Description of what foobar does."""

__author__ = "Alex 'Chozabu' P-B"
__copyright__ = "Copyright 2016, Chozabu"

machine_name = "unknown"
pkey = "unknown"
running = True
ui_port = 8080
auto_accept = True
ext_ip = None
serve_port = 9999

try:
    from urllib.request import urlopen
    ext_ip = urlopen('http://ip.42.pl/raw').read()
    print("detected IP as", ext_ip)
except:
    print("could not get external IP")

def load_data(data):
    global machine_name, pkey, ui_port, serve_port
    machine_name = data['machine_name']
    pkey = data['pkey']
    ui_port = data['ui_port']
    serve_port = data['serve_port']
