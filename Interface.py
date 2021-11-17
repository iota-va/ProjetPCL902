"""
Created on Fri Sep 24 09:00 2021
@author:DEPELSEMACKER Karl, ALFONSO Vincent, KESTEL Samuel
"""

from tkinter import *
import matplotlib.pyplot as plt
import pyfirmata
import time as t
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
import pyvisa
from DetectionSynchrone import *
import serial

plt.style.use('seaborn')

class GUI():
    def __init__(self,root):
        self.root = root
        self.root.title("Aquisiteur 9000")

        self.buttons = LabelFrame(self.root, text="Buttons", bg= 'white')
        self.buttons.grid(row=0,column=0)

        self.para = LabelFrame(self.root, text="Paramètres")
        self.para.grid(row=1,column=0)

        self.button1 = Button(self.buttons, text="Moteur", command=self.moteur, font=('Courier',15), bg='white')
        self.button1.grid(row=0,rowspan=1,column=0)

        self.button2 = Button(self.buttons, text="Graph", command=self.graph, font=('Courier',15), bg='white')
        self.button2.grid(row=0,rowspan=1,column=2)

        self.button3 = Button(self.buttons, text="Curve fit", command=self.courbe, font=('Courier',15), bg='white')
        self.button3.grid(row=0,rowspan=1,column=3)

        self.button4 = Button(self.buttons, text = "Lock-IN", command=self.lock, font=('Courier',15), bg='white')
        self.button4.grid(row=0,rowspan=1,column=1)

        self.button5 = Button(self.buttons, text="Mesure", command=self.mesure, font=('Courier',15), bg='white')
        self.button5.grid(row=0,rowspan=1,column=4)

    def moteur(self):

        self.Lmot = LabelFrame(self.para,text = "Moteur")
        self.Lmot.grid(row=0,column=0)

        self.v1, self.v2, self.v3, self.v4 = DoubleVar(), DoubleVar(), DoubleVar(), DoubleVar()
        
        Label(self.Lmot,text='angle', font=('Courier',15)).grid(row=0, column=0)
        self.angle = Entry(self.Lmot, textvariable=self.v1, width=5, font=('Courier',15))
        self.angle.grid(row=0, column=1)

        Label(self.Lmot,text='pas', font=('Courier',15)).grid(row=1, column=0)
        self.pas = Entry(self.Lmot, textvariable=self.v2, width=5, font=('Courier',15))
        self.pas.grid(row=1, column=1)

        Label(self.Lmot,text="temps d'integration", font=('Courier',15)).grid(row=2, column=0)
        self.tps = Entry(self.Lmot, textvariable=self.v3, width=5, font=('Courier',15))
        self.tps.grid(row=2, column=1)

        Label(self.Lmot,text="step", font=('Courier',15)).grid(row=3, column=0)
        self.step = Entry(self.Lmot, textvariable=self.v4, width=5, font=('Courier',15))
        self.step.grid(row=3, column=1)

        self.app1 = Button(self.Lmot, text="Appliquer", command=self.appmot, font=('Courier',15))
        self.app1.grid(row=4, column=0,padx=10)

        self.kill = Button(self.Lmot, text="Quitter", command=lambda:self.Lmot.destroy(), font=('Courier',15))
        self.kill.grid(row=4, column=1)

    def lock(self):
        self.w1, self.w2, self.w3, self.w4 = DoubleVar(), DoubleVar(), DoubleVar(), DoubleVar()

        self.Llock = LabelFrame(self.para,text = "Lock-In")
        self.Llock.grid(row=0,column=1)

        Label(self.Llock,text='Amplitude', font=('Courier',15)).grid(row=0, column=0)
        self.amp = Entry(self.Llock, textvariable=self.w1, width=5, font=('Courier',15))
        self.amp.grid(row=0, column=1)

        Label(self.Llock,text='fq', font=('Courier',15)).grid(row=1, column=0)
        self.fq = Entry(self.Llock, textvariable=self.w2, width=5, font=('Courier',15))
        self.fq.grid(row=1, column=1)

        Label(self.Llock,text="off", font=('Courier',15)).grid(row=2, column=0)
        self.off = Entry(self.Llock, textvariable=self.w3, width=5, font=('Courier',15))
        self.off.grid(row=2, column=1)

        Label(self.Llock,text="harm", font=('Courier',15)).grid(row=3, column=0)
        self.harm = Entry(self.Llock, textvariable=self.w4, width=5, font=('Courier',15))
        self.harm.grid(row=3, column=1)

        self.app2 = Button(self.Llock, text="Appliquer", command=self.applock, font=('Courier',15))
        self.app2.grid(row=4, column=0,padx=10)

        self.kill = Button(self.Llock, text="Quitter", command=lambda:self.Llock.destroy(), font=('Courier',15))
        self.kill.grid(row=4, column=1)

    def graph(self):
        self.Lgraph = LabelFrame(self.para, text="Graphique")
        self.Lgraph.grid(row=0,column=2)

        self.canvas = Canvas(self.Lgraph)
        self.canvas.grid(row=0,column=0)

        self.kill = Button(self.Lgraph, text="Quitter", command=lambda:self.Lgraph.destroy(), font=('Courier',15))
        self.kill.grid(row=1, column=1)

        self.perso = Button(self.Lgraph, text='Personnaliser', command=self.Perso1, font=('Courier',15))
        self.perso.grid(row=1, column=0)

        
    def courbe(self):
        return(print("hello"))

    def appmot(self):
        self.v1 = float(self.angle.get())
        self.v2 = float(self.pas.get())
        self.v3 = float(self.tps.get())
        self.v4 = float(self.step.get())
        return(print(self.v1,self.v2,self.v3,self.v4))

    def applock(self):
        self.w1 = float(self.amp.get())
        self.w2 = float(self.fq.get())
        self.w3 = float(self.off.get())
        self.w4 = float(self.harm.get())
        return(print(self.w1,self.w2,self.w3,self.w4))

    def mesure(self):
        return(print('suck it'))

    def Perso1(self):
        return(print('pffff'))

root = Tk()
GUI(root)
root.mainloop()