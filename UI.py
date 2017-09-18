import numpy as np
import tkinter as tk
import plot
import device_profile
import device_server
import filter

import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

matplotlib.use('TkAgg')

class UI:
    def __init__(self, **kwargs):        
        self.top = tk.Tk()
        self.top.geometry('1350x1000')
        self.top.title('Radar')
        self.menu=tk.Menu(self.top)
        

        self.command = tk.Frame(self.top)

        self.logtext = tk.Text(self.top, height=2, state='disable', bg='Ivory')
        self.fig = Figure(figsize=(5,5), dpi=100) 
        self.mcanvas = FigureCanvasTkAgg(self.fig, master=self.top)
        self.mcanvas.get_tk_widget().configure({'width':1000,'height':1000})
        self.subplot=self.fig.add_subplot(111)
        #self.subplot.xlim((-6,6))
        #self.subplot.ylim((0,12))

        self.mcanvas.get_tk_widget().pack(side=tk.RIGHT)
        
        self.testbutton=tk.Button(self.command, text='Test', padx=10, command=filter.test_filter)
        self.testbutton.pack(anchor=tk.W, fill=tk.Y, side=tk.LEFT)
        self.scatterbutton = tk.Button(self.command,text='History', padx=10, command=self.scatter_all)
        self.plotbutton=tk.Button(self.command,text='Path', padx=10, command=self.plot_all_path)
        self.clearbutton = tk.Button(self.command,text='Clear',padx=10, command=self.clearplot)
        self.clearhistorybutton = tk.Button(self.command,text='Clear History',padx=30, command=self.clearhistory)
        self.savebutton = tk.Button(self.command,text='Save',padx=10, command=filter.savehistory)
        self.loadbutton = tk.Button(self.command,text='Load',padx=10, command=self.loadhistory)
        self.statustext = tk.Text(self.top, height=20, state='disable', bg='lightgray')
        self.command.pack(fill=tk.X)
        self.scatterbutton.pack(anchor=tk.W, fill=tk.Y, side=tk.LEFT)
        self.plotbutton.pack(anchor=tk.W, fill=tk.Y, side=tk.LEFT)
        self.clearbutton.pack(anchor=tk.W, fill=tk.Y, side=tk.LEFT)
        self.savebutton.pack(anchor=tk.W, fill=tk.Y, side=tk.LEFT)
        self.loadbutton.pack(anchor=tk.W, fill=tk.Y, side=tk.LEFT)

        self.statustext.pack(fill=tk.X)
        self.logtext.pack(expand=True, fill=tk.BOTH)

        self.mcanvas.show()
        self.clearplot()
        
    def clear(self):
        self.logtext.config({'state':'normal'})
        self.logtext.delete(1.0, tk.END)
        self.logtext.config({'state':'disable'})
        filter.Tracer.history.clear()

        self.clearplot()
           
    
    def clearplot(self):
        self.subplot.clear()
        self.subplot.set_xlim(0,15)
        self.subplot.set_ylim(0,15)
        filter.Tracer.history.clear()
        self.mcanvas.show()            

    def clearhistory(self):
        self.clearplot()
        filter.clearhistory()

    def loadhistory(self):
        #print('loadhistory')
        filter.loadhistory()
        self.scatter_all()

    def log(self,text):
        self.logtext.config({'state':'normal'})
        self.logtext.insert(tk.END,text)
        self.logtext.insert(tk.END,'\n')
        self.logtext.config({'state':'disable'})    
        self.logtext.yview(1e6)
        self.update_device()

    def update_device(self):
        #update device information
        self.statustext.config({'state':'normal'})    
        self.statustext.delete(1.0,tk.END)
        for d in device_profile.Device.known_device:
            for v in d.status.items():          
                self.statustext.insert(tk.END,'%-16s    %-24s\n' % (str(v[0]), str(v[1])))
            self.statustext.insert(tk.END,'\n\n')
        self.statustext.config({'state':'disable'})

        self.subplot.scatter([t.filtered_pos['x'] for t in filter.Tracer.history],
                        [t.filtered_pos['y'] for t in filter.Tracer.history],color='black')
        for t in filter.Tracer.history:
            self.subplot.plot([t.transformed_pos['x'], t.filtered_pos['x']], 
                              [t.transformed_pos['y'], t.filtered_pos['y']], color='gray') 
        self.plot_radarcover()

        self.mcanvas.show()
    
    def scatter_all(self):
        #print('plot all')
        self.subplot.scatter([t.filtered_pos['x'] for t in filter.Tracer.history],
                        [t.filtered_pos['y'] for t in filter.Tracer.history],color='black')
        for t in filter.Tracer.history:
            self.subplot.plot([t.transformed_pos['x'], t.filtered_pos['x']], 
                              [t.transformed_pos['y'], t.filtered_pos['y']], color='gray') 
        self.mcanvas.show()
        

    def plot_all_path(self):
        #print('lists=%d'%(len(filter.Tracer.tracerlist)))
        for l in filter.Tracer.tracerlist:
            #print('  len=%d'%(len(l.targetlist)))
            xs=[t.filtered_pos['x'] for t in l.targetlist]
            ys=[t.filtered_pos['y'] for t in l.targetlist]
            self.subplot.scatter(xs, ys)
            self.subplot.plot(xs, ys)
            for t in l.targetlist:
                self.subplot.plot([t.transformed_pos['x'], t.filtered_pos['x']], 
                                  [t.transformed_pos['y'], t.filtered_pos['y']], color='gray')    
                #print(t.transformed_pos, t.filtered_pos)
        self.mcanvas.show()

    def plot_radarcover(self):
        for d in device_profile.Device.known_device:
            if d.status['Detection']>0 :
                cx=d.position[0]
                cy=d.position[1]
                lx=np.sin((d.rotation-15)*0.0174533)*1000+cx
                ly=np.cos((d.rotation-15)*0.0174533)*1000+cy
                rx=np.sin((d.rotation+15)*0.0174533)*1000+cx
                ry=np.cos((d.rotation+15)*0.0174533)*1000+cy
                mx=np.sin(d.rotation*0.0174533)*1000+cx
                my=np.cos(d.rotation*0.0174533)*1000+cy
                self.subplot.plot([lx, cx, rx],[ly, cy, ry], color='gray')
                self.subplot.plot([mx, cx],[my, cy],color='gray')


ui=UI()
#filter.test_filter()
ui.update_device()
device_server.DeviceServer.logfunc = ui.log
server = device_server.DeviceServer()
server.startthread()
tk.mainloop()
