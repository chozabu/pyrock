
import json
from pprint import pprint
from network import send_packet
import settings


machines = []
machines_dict = {}

def get_by_ip(ip):
    for m in machines:
        if m.ip == ip:
            return m

class Machine:
    def __init__(self, name="unknown", pkey="unknown", pkeyhash="unknown", ip=None, port=None):
        self.name = name
        self.pkey = pkey
        self.pkeyhash = pkeyhash
        self.ip = ip
        self.port = port
    #def send_data(self, data):
    #    return send_data(self.ip, self.port, data)
    def send_packet(self, data, meta):
        return send_packet(self.ip, self.port, data, meta)
    def connect(self):
        pass

def send_all(data, meta):
    for m in machines:
        m.send_packet(data, meta)

def loadcontacts(machinesfile='machines.json'):
    with open(machinesfile) as data_file:
        data = json.load(data_file)
    #pprint(data)
    for m in data:
        machine = Machine(
            name=m['name'],
            pkey=m['pkey'],
            pkeyhash=m['pkeyhash'],
            ip=m['ip'],
            port=m['port'],
        )
        machines.append(machine)
        machines_dict[machine.pkey] = machine
