from math import sin, cos
from target import Target
from collections import OrderedDict
class Device:
    known_device = list()
    def __init__(self, address, position=(0,0), rotation=0, name=''):
        self.name = name
        self.address = address
        self.position = position
        self.rotation = rotation
        self.status=OrderedDict()
        self.status['Name']=name
        self.status['Address']=address
        self.status['Position']=position
        self.status['Rotation']=rotation
        self.status['Detection']=0
        self.status['Last target']=None
        self.antana_angle_correction=-5 

Device.known_device = [Device(address=('192.168.1.8',6000),name='Radar_B', position=(1.45, -11), rotation=15),
                       Device(address=('192.168.1.7',6000),name='Radar_A', position=(6.5, 0), rotation=195)]
