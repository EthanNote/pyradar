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

Device.known_device = [Device(address=('192.168.1.7',6000),name='Radar_A', position=(-4.75, 0.73), rotation=68.75),
                       Device(address=('192.168.1.8',6000),name='Radar_B', position=(-6, 0), rotation=90)]