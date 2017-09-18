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
    #def createtarget(self, distance, angle, velocity):
    #    angleoffset=-15.
    #    anglezoom=1
    #    rx=distance*cos(anglezoom*(angle+angleoffset))
    #    ry=distance*sin(anglezoom*(angle+angleoffset))
    #    target=Target()
    #    target.position={'x':rx,'y':ry}
    #    target.velocity={'vx':None,'vy':velocity}
    #    target.device=self
    #    return target

Device.known_device = [Device(address=('192.168.1.7',6000),name='Radar_A', position=(6, 0), rotation=0),
                       Device(address=('192.168.1.8',6000),name='Radar_B', position=(7, 0), rotation=0)]
