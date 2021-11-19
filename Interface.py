from tkinter import *
from tkinter import ttk
import numpy as np
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
NavigationToolbar2Tk)
import matplotlib.pyplot as plt


class Interface:

    def __init__(self, master):
        self.master = master
        master.title('PCL902')

        self.master.geometry("800x600")
        self.master.resizable(width=False, height=False)

        self.notebook = ttk.Notebook(master)
        self.notebook.grid()

        self.tabMotor, self.tabLockin, self.tabGraphic, self.tabFit, self.tabMeasure = ttk.Frame(self.notebook,width=790,height=590), ttk.Frame(self.notebook, width=790, height=590), ttk.Frame(self.notebook, width=790, height=590), ttk.Frame(self.notebook, width=790, height=590), ttk.Frame(self.notebook, width=790, height=590)

        self.notebook.add(self.tabMotor, text='Motor')
        self.notebook.add(self.tabLockin, text='Lock-in')
        self.notebook.add(self.tabGraphic, text='Graphic')
        self.notebook.add(self.tabFit, text='Curve fit')
        self.notebook.add(self.tabMeasure, text='Measure')
        
        # Motor :

        self.v1, self.v2, self.v3, self.v4 = DoubleVar(), DoubleVar(), DoubleVar(), DoubleVar()

        Label(self.tabMotor, text='Angle', font=(24)).place(x=150, y=100)
        self.angle = Entry(self.tabMotor, textvariable=self.v1, justify='center', width=10, font=(24))
        self.angle.place(x=220, y=100, height=30)

        Label(self.tabMotor, text='Pas', font=(24)).place(x=160, y=250)
        self.pas = Entry(self.tabMotor, textvariable=self.v2, justify='center', width=10, font=(24))
        self.pas.place(x=220, y=250, height=30)

        Label(self.tabMotor, text="Integration Time", font=(24)).place(x=420, y=100)
        self.tps = Entry(self.tabMotor, textvariable=self.v3, justify='center', width=10, font=(24))
        self.tps.place(x=570, y=100, height=30)

        Label(self.tabMotor, text="Step", font=(24)).place(x=500, y=250)
        self.step = Entry(self.tabMotor, textvariable=self.v4, justify='center', width=10, font=(24))
        self.step.place(x=570, y=250, height=30)

        self.app1 = Button(self.tabMotor, text="Apply", command=self.appmot, width=20, height=5, font=(24))
        self.app1.place(x=320, y=400)

        # Lock-in

        self.w1, self.w2, self.w3, self.w4, self.w5, self.w6, self.w7, self.w8, self.w9, self.w10 = DoubleVar(), DoubleVar(), DoubleVar(), DoubleVar(), DoubleVar(), DoubleVar(), DoubleVar(), DoubleVar(), DoubleVar(), DoubleVar()

        Label(self.tabLockin, text='Amplitude', font=(24)).place(x=120, y=67)
        self.amp = Entry(self.tabLockin, textvariable=self.w1, justify='center', width=10, font=(24))
        self.amp.place(x=220, y=67)

        Label(self.tabLockin, text='Frequency', font=(24)).place(x=115, y=134)
        self.fq = Entry(self.tabLockin, textvariable=self.w2, justify='center', width=10, font=(24))
        self.fq.place(x=220, y=134)

        Label(self.tabLockin, text='Harmonic', font=(24)).place(x=120, y=201)
        self.harm = Entry(self.tabLockin, textvariable=self.w3, justify='center', width=10, font=(24))
        self.harm.place(x=220, y=201)

        Label(self.tabLockin, text='Time constant', font=(24)).place(x=90, y=268)
        self.timeCste = Entry(self.tabLockin, textvariable=self.w4, justify='center', width=10, font=(24))
        self.timeCste.place(x=220, y=268)

        Label(self.tabLockin, text='Filter', font=(24)).place(x=150, y=335)
        self.filt = Entry(self.tabLockin, textvariable=self.w5, justify='center', width=10, font=(24))
        self.filt.place(x=220, y=335)

        Label(self.tabLockin, text='Current', font=(24)).place(x=490, y=67)
        self.current = Entry(self.tabLockin, textvariable=self.w6, justify='center', width=10, font=(24))
        self.current.place(x=570, y=67)

        Label(self.tabLockin, text='Offset', font=(24)).place(x=495, y=134)
        self.offset = Entry(self.tabLockin, textvariable=self.w7, justify='center', width=10, font=(24))
        self.offset.place(x=570, y=134)

        Label(self.tabLockin, text='Voltage', font=(24)).place(x=485, y=201)
        self.voltage = Entry(self.tabLockin, textvariable=self.w8, justify='center', width=10, font=(24))
        self.voltage.place(x=570, y=201)

        Label(self.tabLockin, text='Current Mode', font=(24)).place(x=445, y=268)
        self.currentMode = Entry(self.tabLockin, textvariable=self.w9, justify='center', width=10, font=(24))
        self.currentMode.place(x=570, y=268)

        Label(self.tabLockin, text='Source', font=(24)).place(x=490, y=335)
        self.source = Entry(self.tabLockin, textvariable=self.w10, justify='center', width=10, font=(24))
        self.source.place(x=570, y=335)

        self.app2 = Button(self.tabLockin, text="Apply", command=self.applock, width=20, height=5, font=(24))
        self.app2.place(x=320, y=400)

        # Graphic

        self.app3 = Button(self.tabGraphic, text='Start', command=self.graphic(master=self.master),width=10, height=2, font=(24))
        self.app3.place(x=10, y=10)

    def appmot(self):
        self.v1 = float(self.angle.get())
        self.v2 = float(self.pas.get())
        self.v3 = float(self.tps.get())
        self.v4 = float(self.step.get())
        return (print(self.v1, self.v2, self.v3, self.v4))

    def applock(self):
        self.w1 = float(self.amp.get())
        self.w2 = float(self.fq.get())
        self.w3 = float(self.harm.get())
        self.w4 = float(self.timeCste.get())
        self.w5 = float(self.filt.get())
        self.w6 = float(self.current.get())
        self.w7 = float(self.offset.get())
        self.w8 = float(self.voltage.get())
        self.w9 = float(self.currentMode.get())
        self.w10 = float(self.source.get())
        return (print(self.w1, self.w2, self.w3, self.w4, self.w5, self.w6, self.w7, self.w8, self.w9, self.w10))

    def graphic(self, master):

        x = np.linspace(0,10,11)

        y = x**2

        self.fig = plt.figure(figsize=(5,5), dpi=100)
        self.plot = self.fig.add_subplot(111)
        #self.plot.plot(x,y)

        canvas = FigureCanvasTkAgg(self.fig, master=master)
        canvas.draw()
        canvas.get_tk_widget().grid()

        canvas.get_tk_widget().grid()



root = Tk()
my_gui = Interface(root)
root.mainloop()