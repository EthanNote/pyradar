from socketserver import BaseRequestHandler, ThreadingTCPServer
from struct import Struct
from datetime import datetime
from threading import Thread
from device_profile import *
import filter

#statics={0:0, 1:0,2:0,3:0,4:0,5:0,6:0,7:0,8:0,9:0,10:0 }
class DataHandler(BaseRequestHandler):
   
    def handle(self):
        print('Got connection from ', self.client_address)
        DeviceServer.log('Got connection from ' + str(self.client_address))
        for device in Device.known_device:
            if device.address == self.client_address:
                print('Known device ', device.name)
                DeviceServer.log('Known device ' + device.name)
                self.device = device
                break
        else:
            print('Unknown device')
            DeviceServer.log('Unknown device')
            print(dir(self.client_address))
            return

        while True:
            msg = self.request.recv(8192)
            if not msg:
                DeviceServer.log('Device %s disconnected' % device.name)
                break
            #print('Data from: ',self.client_address, ' length: ', len(msg))
            self.onMessage(msg)
            

    def onMessage(self, msg):
        if msg[0:2] == b'U\xaa':           
            datasize = Struct('!h').unpack(msg[3:5])
            #print('Message type: ',hex(msg[2]),' size: ',datasize)

        else:
            print('Unknown header: ',hex(msg[0]), hex(msg[1]))
            return

        if(msg[2] == 18):
            self.onTargetList(msg)
    
    def onTargetList(self, msg):
        
        targetcount = msg[5]
        
        for i in range(targetcount):
            #distance, angle, x, y, velocity = Struct('!ihiih').unpack()
            start = 6 + 17 * i
            end = start + 16
            data = Struct('!ihiih').unpack(msg[start:end])
            distance = data[0] * 0.01
            angle = data[1] * 0.01
            x = data[2] * 0.01
            y = data[3] * 0.01
            velocity = data[4] * 0.01
            power = msg[end]

            now = datetime.now()
           
            #report = {'distance':distance, 'angle':angle,
            #        'x':x, 'y':y, 'velocity':velocity,
            #        'power':power,'device':self.device.name,
            #        'time':'%d-%d-%d_%d:%d:%s' % (now.year, now.month,
            #        now.day,
            #         now.hour, now.minute,
            #         now.second+now.microsecond/1000000.0)}
            #print(report)
            #transformed_position = {'x':self.device.position[0] + distance * sin(angle*0.0174533),
            #                      'y':self.device.position[1] + distance * cos(angle*0.0174533)}
            world_angle=(-angle+self.device.rotation+self.device.antana_angle_correction+30)*0.0174533                      
            
            transformed_position = {'x':self.device.position[0] + distance * sin(world_angle),
                                   'y':self.device.position[1] + distance * cos(world_angle)}
            if distance < 16:
                self.device.status['Last target'] = (distance, angle, velocity)
                self.device.status['Detection']+=1
                #print({distance,angle},self.device.rotation, ' -> ', transformed_position)
                DeviceServer.log('%04d-%02d-%02d_%02d:%02d:%02d:%03d  "%s"  %12f  %12f  %12f  %12f  %12f  %12f' % (now.year, now.month, now.day, now.hour, now.minute, 
                    now.second,now.microsecond / 1000.0,self.device.name,
                    distance, angle, x, y, velocity, power))
                filter.tracetarget(Target(position={'x':x, 'y':y},
                                          velocity={'vx':None, 'vy':velocity},
                                          device=self.device, transformed_pos=transformed_position, time=now))

class DeviceServer:
    logfunc = None
    @classmethod
    def log(self,text):
        if DeviceServer.logfunc:
            DeviceServer.logfunc(text)

    def __init__(self):
        self.server = ThreadingTCPServer(('', 5100),DataHandler)
        self.thread = Thread(target=DeviceServer.start,args=(self,))
      

    def start(self):
        self.server.serve_forever()
    
    def startthread(self):
        self.thread.start()
        DeviceServer.log('Server thread start ' + str(self.server.server_address))

if __name__=='__main__':
    print('start server')
    server=DeviceServer()
    server.start()