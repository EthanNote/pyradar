import numpy as np
import matplotlib.pyplot as plt
from math import *
from filter import Tracer

def plot_tracer(tracer,show=True):
    positions = np.array([[t['x'], t['y']] for t in tracer.targetlist])
    plt.scatter(positions[:,0],positions[:,1])
    plt.plot(positions[:,0],positions[:,1])
    if show:
        plt.show()

def plot_tracers(split=False, show=True):
    print('plot_tracers')
    plt.figure()
    if not split:        
        for t in Tracer.tracerlist:
            plot_tracer(t,False)
            
        
    else:
        l = len(Tracer.tracerlist)
        if(l<1):
            return

        h = int(l / sqrt(l))
        if h == 0:
            h = 1

        w = int(l / h)
        if w * h < l:
            w = int(l / h) + 1

        for i in range(l):
            plt.subplot(h,w,i+1)
            plt.title('Path %d'%i)
            plot_tracer(Tracer.tracerlist[i], False)

    if show:
        plt.show()

