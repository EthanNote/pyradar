import numpy as np
from filterpy.kalman import KalmanFilter
import copy
from target import Target
from device_profile import Device
import pickle
import datetime
#The Kalman-Filter
class Filter:
    def __init__(self):
       
        self.kfilter = KalmanFilter(dim_x=4, dim_z=2)

        #Transform matrix
        self.kfilter.F = np.array([[1, 0, 1, 0],
                                   [0, 1, 0, 1],
                                   [0, 0, 1, 0],
                                   [0, 0, 0, 1]])
        self.kfilter.R = np.array([[16, 0],
                                   [0, 16]])
        #Observation matrix
        #for state vector [x, y, vx, vy] mesure [x, y]
        self.kfilter.H = np.array([[1, 0, 0, 0],
                                   [0, 1, 0, 0]])

   
    def setstate(self,x,y):
        self.kfilter.x = np.array([[x],
                                   [y],
                                   [0],
                                   [0]])

    def getstate(self):
        return np.copy(self.kfilter.x)

    def update(self, x,y):
        self.kfilter.predict()
        self.kfilter.update(np.array([[x],
                                      [y]]))

class Tracer:
    tracerlist = list()
    history = list()
    def __init__(self, firsttarget: Target):
        self.filter = Filter()
        self.filter.setstate(firsttarget.transformed_pos['x'],firsttarget.transformed_pos['y'])
       
        self.targetlist = list()
        firsttarget.filtered_pos=copy.copy(firsttarget.transformed_pos)
        #self.add(self.filter.getstate(), firsttarget.device)
        self.targetlist.append(firsttarget)
        self.id=len(Tracer.tracerlist)
        
    def filt(self, target):
        x = target.transformed_pos['x']
        y = target.transformed_pos['y']
        self.filter.update(x,y)
        state = self.filter.getstate()
        target.filtered_pos = {'x':state[0][0], 'y':state[1][0]}      
        self.targetlist.append(target)
        #print('path(%i,%f,%f)'%(self.id, state[0][0],state[1][0]))
        #print(target.transformed_pos, target.filtered_pos)
                     
def tracetarget(target, maxdistance=2.):
    Tracer.history.append(target)
    #Nearest neighbor classification
    nearestTracer = None   
    nearestDistance2 = maxdistance ** 2
    for tracer in Tracer.tracerlist:
        distance2 = (target.transformed_pos['x'] - tracer.targetlist[-1].filtered_pos['x']) ** 2 \
                  + (target.transformed_pos['y'] - tracer.targetlist[-1].filtered_pos['y']) ** 2 \
                  + (target.time-tracer.targetlist[-1].time).total_seconds()**2*0.04

        if distance2 < nearestDistance2:
            nearestDistance2 = distance2
            nearestTracer = tracer

    #Kalman filtering
    if(nearestTracer != None):
        nearestTracer.filt(target)

    else:
        print('New Tracer')
        nearestTracer = Tracer(target)
        Tracer.tracerlist.append(nearestTracer)

def savehistory():
    f=open('history.dat', 'wb')
    pickle.dump(Tracer.history, f)
    f.close()
    open(('REC_%s_.dat'%datetime.datetime.now()).replace(':','.'),'wb').write(open('history.dat','rb').read())

def clearhistory():
    Tracer.history=list()

def loadhistory():
    f=open('history.dat', 'rb')
    data=pickle.load(f)
    f.close()
    if(data):
        Tracer.oldhistory=Tracer.history
        Tracer.oldtracerlist=Tracer.tracerlist
        Tracer.history=list()
        Tracer.tracerlist=list()
        for t in data:
            tracetarget(t)


def test_filter():
    tracetarget(Target(position={'x':0.0,'y':0.01},velocity={'vx':None,'vy':0},transformed_pos={'x':0.0,'y':0.01}))
    tracetarget(Target(position={'x':0.0,'y':0.04},velocity={'vx':None,'vy':0},transformed_pos={'x':0.2,'y':0.04}))
    tracetarget(Target(position={'x':0.0,'y':0.09},velocity={'vx':None,'vy':0},transformed_pos={'x':0.4,'y':0.09}))
    tracetarget(Target(position={'x':0.0,'y':0.16},velocity={'vx':None,'vy':0},transformed_pos={'x':0.6,'y':0.16}))
    tracetarget(Target(position={'x':0.0,'y':0.32},velocity={'vx':None,'vy':0},transformed_pos={'x':0.8,'y':0.32}))
    tracetarget(Target(position={'x':0.0,'y':0.64},velocity={'vx':None,'vy':0},transformed_pos={'x':1.0,'y':0.64}))
    tracetarget(Target(position={'x':0.0,'y':1.28},velocity={'vx':None,'vy':0},transformed_pos={'x':1.2,'y':1.28}))
    tracetarget(Target(position={'x':0.0,'y':0.01},velocity={'vx':None,'vy':0},transformed_pos={'x':2.0,'y':0.01}))
    tracetarget(Target(position={'x':0.0,'y':0.04},velocity={'vx':None,'vy':0},transformed_pos={'x':2.2,'y':0.04}))
    tracetarget(Target(position={'x':0.0,'y':0.09},velocity={'vx':None,'vy':0},transformed_pos={'x':2.4,'y':0.09}))
    tracetarget(Target(position={'x':0.0,'y':0.16},velocity={'vx':None,'vy':0},transformed_pos={'x':2.6,'y':0.16}))
    tracetarget(Target(position={'x':0.0,'y':0.32},velocity={'vx':None,'vy':0},transformed_pos={'x':2.8,'y':0.32}))
    tracetarget(Target(position={'x':0.0,'y':0.64},velocity={'vx':None,'vy':0},transformed_pos={'x':3.0,'y':0.64}))
    tracetarget(Target(position={'x':0.0,'y':1.28},velocity={'vx':None,'vy':0},transformed_pos={'x':3.2,'y':1.28}))
   
