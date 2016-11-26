
import json
from pprint import pprint
from network import send_packet
import network
import settings


machines = []
machines_dict = {}

def get_by_ip(ip):
    for m in machines:
        if m.ip == ip:
            return m

class Machine:
    def __init__(self, name="unknown", pkey="unknown", pkeyhash="unknown", ip=None, port=None, autoconnect=False):
        self.name = name
        self.pkey = pkey
        self.pkeyhash = pkeyhash
        self.ip = ip
        self.port = port
        self.autoconnect = autoconnect
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
            autoconnect=m.get("autoconnect", False),
        )
        machines.append(machine)
        machines_dict[machine.pkey] = machine

def add_machine(name, pkey, ip, port):
    machine = Machine(
        name=name,
        pkey=pkey,
        pkeyhash=str(hash(pkey)),
        ip=ip,
        port=port,
    )
    machines.append(machine)
    machines_dict[machine.pkey] = machine
    return machine

def init(root=None):
    network.hook_type("machine", got_data)

def autoconnect():
    meta = {
        "type": "machine",
        "subtype": "auto_peer_request"
    }
    data = {
        "name": settings.machine_name,
        "pkey": settings.pkey,
        "pkeyhash": settings.pkey+"_hash",
        "ip": str(settings.ext_ip)
    }
    for m in machines:
        if m.autoconnect:
            print("attempting to connect to", m.name)
            m.send_packet(data, meta)

def got_data(data, machine, meta):
    print(settings.machine_name, data, getattr(machine, "name", "unknown"))
    if meta['subtype'] == "auto_peer_request":
        if settings.auto_accept == True:
            print("accepting FR", data)
            mdata = data['data']
            add_machine(**mdata)
