# -*- coding: utf-8 -*-
"""
Created on Fri Sep  10 09:00:00 2021

@author: DEPELSEMACKER Karl, ALFONSO Vincent
"""

from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from Detection_synchrone import Detection_synchrone
import tkinter.font as tkFont
from Motor import Motor
import pyvisa
import pyfirmata
from scipy.optimize import curve_fit
import numpy as np
import matplotlib.pyplot as plt
import time


class Interface:

    def __init__(self, master):
        self.master = master
        master.title('PCL902')

        self.master.geometry("820x700")
        self.master.resizable(width=False, height=False)

        self.notebook = ttk.Notebook(master)
        self.notebook.pack()

        self.tabMotor, self.tabLockin, self.tabGraph, self.tabMeasure = ttk.Frame(self.notebook, width=810, height=690), ttk.Frame(self.notebook, width=810,
                                                                                                                                   height=690), ttk.Frame(
            self.notebook,
            width=810,
            height=690), ttk.Frame(
            self.notebook, width=890, height=690)

        self.notebook.add(self.tabMotor, text='Motor')
        self.notebook.add(self.tabLockin, text='Lock-in')
        self.notebook.add(self.tabGraph, text='Graphic')
        self.notebook.add(self.tabMeasure, text='Measure')

        # %% Motor :

        self.v1, self.v2, self.v3 = StringVar(), StringVar(), StringVar()

        Label(self.tabMotor, text='Angle', font=24).place(x=150, y=80)
        self.angle = Entry(self.tabMotor, state=DISABLED, textvariable=self.v1, justify='center', width=10, font=24)
        self.angle.place(x=220, y=80, height=30)

        Label(self.tabMotor, text='Pas', font=24).place(x=160, y=180)
        self.pas = Entry(self.tabMotor, state=DISABLED, textvariable=self.v2, justify='center', width=10, font=24)
        self.pas.place(x=220, y=180, height=30)

        Label(self.tabMotor, text="Step", font=24).place(x=155, y=280)
        self.step = Entry(self.tabMotor, state=DISABLED, textvariable=self.v3, justify='center', width=10, font=24)
        self.step.place(x=220, y=280, height=30)

        self.applyMotor = Button(self.tabMotor, text="Apply", state=DISABLED, command=self.Motor, width=20, height=5, font=24)
        self.applyMotor.place(x=300, y=400)

        self.onOffMotor = Button(self.tabMotor, text='Deactivated', bg='red', command=self.ComChoice, width=20, height=5, font=24)
        self.onOffMotor.place(x=50, y=400)

        self.initMotor = Button(self.tabMotor, text='Initialisation', state=DISABLED, command=lambda: self.ButtonMotor(3), width=20, height=5, font=24)
        self.initMotor.place(x=550, y=400)

        font30 = tkFont.Font(size=30, weight='bold')

        self.stepMinus = Button(self.tabMotor, text=' < ', state=DISABLED, command=lambda: self.ButtonMotor(2), font=font30)
        self.stepMinus.place(x=500, y=100)

        self.stepPlus = Button(self.tabMotor, text=' > ', state=DISABLED, command=lambda: self.ButtonMotor(1), font=font30)
        self.stepPlus.place(x=600, y=100)

        self.continueMinus = Button(self.tabMotor, text='<<', state=DISABLED, command=lambda: self.ButtonMotor(2), repeatdelay=100, repeatinterval=100, font=font30)
        self.continueMinus.place(x=500, y=200)

        self.continuePlus = Button(self.tabMotor, text='>>', state=DISABLED, command=lambda: self.ButtonMotor(1), repeatdelay=100, repeatinterval=100, font=font30)
        self.continuePlus.place(x=600, y=200)

        # %% Lock-in :

        self.w1, self.w2, self.w3, self.w6, self.w7, self.w8, self.w9, self.w10 = StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar(), StringVar()

        self.w4, self.w5 = DoubleVar(), DoubleVar()

        Label(self.tabLockin, text='Amplitude', font=24).place(x=120, y=67)
        self.amp = Entry(self.tabLockin, state=DISABLED, textvariable=self.w1, justify='center', width=10, font=24)
        self.amp.insert(0, '0.0')
        self.amp.place(x=220, y=67)

        Label(self.tabLockin, text='Frequency', font=24).place(x=115, y=134)
        self.fq = Entry(self.tabLockin, state=DISABLED, textvariable=self.w2, justify='center', width=10, font=24)
        self.fq.insert(0, '0.0')
        self.fq.place(x=220, y=134)

        Label(self.tabLockin, text='Harmonic', font=24).place(x=120, y=201)
        self.harm = Entry(self.tabLockin, state=DISABLED, textvariable=self.w3, justify='center', width=10, font=24)
        self.harm.insert(0, '0.0')
        self.harm.place(x=220, y=201)

        Label(self.tabLockin, text='Time constant', font=24).place(x=90, y=268)
        self.timeCste = Entry(self.tabLockin, state=DISABLED, textvariable=self.w4, justify='center', width=10, font=24)
        self.timeCste.place(x=220, y=268)

        Label(self.tabLockin, text='Sensitivity', font=24).place(x=120, y=335)
        self.sensitivity = Entry(self.tabLockin, state=DISABLED, textvariable=self.w5, justify='center', width=10, font=24)
        self.sensitivity.place(x=220, y=335)

        Label(self.tabLockin, text='Current', font=24).place(x=490, y=67)
        self.current = Spinbox(self.tabLockin, state=DISABLED, textvariable=self.w6, values=('1MEG', '100MEG'), justify='center',
                               width=10, font=24)
        self.current.place(x=570, y=67)

        Label(self.tabLockin, text='Offset', font=24).place(x=495, y=134)
        self.offset = Entry(self.tabLockin, state=DISABLED, textvariable=self.w7, justify='center', width=10, font=24)
        self.offset.insert(0, '0.0')
        self.offset.place(x=570, y=134)

        Label(self.tabLockin, text='Voltage', font=24).place(x=485, y=201)
        self.voltage = Spinbox(self.tabLockin, state=DISABLED, textvariable=self.w8, values=('A', 'A-B'), justify='center', width=10,
                               font=24)
        self.voltage.place(x=570, y=201)

        Label(self.tabLockin, text='Current Mode', font=24).place(x=445, y=268)
        self.currentMode = Spinbox(self.tabLockin, state=DISABLED, textvariable=self.w9, values=('AC', 'DC'), justify='center',
                                   width=10, font=24)
        self.currentMode.place(x=570, y=268)

        Label(self.tabLockin, text='Source', font=24).place(x=490, y=335)
        self.source = Spinbox(self.tabLockin, state=DISABLED, textvariable=self.w10, values=('INT', 'EXT'), justify='center', width=10,
                              font=24)
        self.source.place(x=570, y=335)

        self.applyLockin = Button(self.tabLockin, text="Apply", state=DISABLED, command=self.Lockin, width=20, height=5, font=24)
        self.applyLockin.place(x=450, y=450)

        self.onOffLockin = Button(self.tabLockin, text='Deactivated', bg='red', command=self.OnOffLockin, width=20, height=5, font=24)
        self.onOffLockin.place(x=150, y=450)

        # %% Graphic

        self.app3 = Button(self.tabGraph, text='Start', command=self.Graphic, width=10, height=2, font=24)
        self.app3.place(x=10, y=10)

        self.app4 = Button(self.tabGraph, text='Curve Fit', command=self.CurveFit, width=10, height=2, font=24)
        self.app4.place(x=370, y=10)

        self.app5 = Button(self.tabGraph, text='Clear', command=self.Clear, width=10, height=2, font=24)
        self.app5.place(x=700, y=10)

        self.fig = plt.figure(1, dpi=125)
        self.ax = self.fig.add_subplot(111)
        self.ax.set_ylabel('Tension (mV)')
        self.ax.set_xlabel('Angle (°)')
        self.ax.set_xlim(-20, 20)
        self.xs = []
        self.ys = []
        self.canvas = Canvas(self.tabGraph, height=700)
        self.canvas.place(x=10, y=70, width=900)
        self.ax.plot(self.xs, self.ys)
        self.ax.grid()
        self.fig.savefig('courbe.png')
        self.photo = PhotoImage(master=self.tabGraph, file='courbe.png')
        self.canvas.create_image(0, 0, image=self.photo, anchor='nw')
        self.canvas.update()

        # %% Measure

        self.m_angle = Entry(self.tabMeasure, justify='center', bg='#B8B6B5')
        self.m_angle.insert(0, 'Angle (°)')
        self.m_angle.grid(row=0, column=0)

        self.m_tension = Entry(self.tabMeasure, justify='center', bg='#B8B6B5')
        self.m_tension.insert(0, 'Tension (mV)')
        self.m_tension.grid(row=0, column=1)

        self.sigma = Entry(self.tabMeasure, justify='center', bg='#B8B6B5')
        self.sigma.insert(0, 'σ (°)')
        self.sigma.grid(row=0, column=2)

        self.amplitude = Entry(self.tabMeasure, justify='center', bg='#B8B6B5')
        self.amplitude.insert(0, 'Amplitude (mV.°)')
        self.amplitude.grid(row=0, column=3)

        self.mu = Entry(self.tabMeasure, justify='center', bg='#B8B6B5')
        self.mu.insert(0, 'μ (°)')
        self.mu.grid(row=0, column=4)

        return

        # %% Function

    def Motor(self):
        self.v1 = float(self.angle.get())
        self.v2 = float(self.pas.get())
        self.v3 = float(self.step.get())
        return

    def ComChoice(self):

        self.com = StringVar()

        self.comChoiceWindow = Toplevel(self.master)

        self.comChoiceWindow.geometry('200x100')
        self.comChoiceWindow.title('COM')
        self.comChoiceWindow.resizable(width=False, height=False)

        self.comChoiceEntry = Entry(self.comChoiceWindow, justify='center', textvariable=self.com)
        self.comChoiceEntry.place(x=40, y=30)

        self.comChoiceButton = Button(self.comChoiceWindow, text='Apply', command=self.OnOffMotor)
        self.comChoiceButton.place(x=80, y=55)

        return

    def OnOffMotor(self):

        self.comChoiceWindow.destroy()
        if self.onOffMotor['bg'] == 'red':
            try:
                self.arduino = pyfirmata.Arduino(self.com)
            except:
                messagebox.showinfo('Error', 'Arduino not found')
            else:
                self.board = Motor(self.arduino)
                self.onOffMotor['text'] = 'Activated'
                self.onOffMotor['bg'] = 'green'
                self.applyMotor['state'] = NORMAL
                self.initMotor['state'] = NORMAL
                self.stepMinus['state'] = NORMAL
                self.stepPlus['state'] = NORMAL
                self.continueMinus['state'] = NORMAL
                self.continuePlus['state'] = NORMAL
                self.pas['state'] = NORMAL
                self.step['state'] = NORMAL
                self.angle['state'] = NORMAL

        else:
            self.arduino.exit()
            self.onOffMotor['text'] = 'Deactivated'
            self.onOffMotor['bg'] = 'red'
            self.applyMotor['state'] = DISABLED
            self.initMotor['state'] = DISABLED
            self.stepMinus['state'] = DISABLED
            self.stepPlus['state'] = DISABLED
            self.continueMinus['state'] = DISABLED
            self.continuePlus['state'] = DISABLED
            self.pas['state'] = DISABLED
            self.step['state'] = DISABLED
            self.angle['state'] = DISABLED
        return

    def ButtonMotor(self, button_id):
        if button_id == 1:
            self.board.h()
        if button_id == 2:
            self.board.a()
        if button_id == 3:
            self.board.zero()
        return

    def OnOffLockin(self):

        if self.onOffLockin['bg'] == 'red':
            try:
                self.rm = pyvisa.ResourceManager()
                self.rm = self.rm.open_resource('USB0::0xB506::0x2000::002730::INSTR', read_termination='\n')
            except pyvisa.VisaIOError:
                messagebox.showinfo('Error', 'Lock-In not found')
            else:
                self.ds = Detection_synchrone(self.rm)
                self.onOffLockin['bg'] = 'green'
                self.onOffLockin['text'] = 'Activated'
                self.applyLockin['state'] = NORMAL
                self.amp['state'] = NORMAL
                self.fq['state'] = NORMAL
                self.harm['state'] = NORMAL
                self.timeCste['state'] = NORMAL
                self.sensitivity['state'] = NORMAL
                self.current['state'] = NORMAL
                self.offset['state'] = NORMAL
                self.voltage['state'] = NORMAL
                self.currentMode['state'] = NORMAL
                self.source['state'] = NORMAL
        else:
            self.rm.close()
            self.onOffLockin['bg'] = 'red'
            self.onOffLockin['text'] = 'Deactivated'
            self.applyLockin['state'] = DISABLED
            self.amp['state'] = DISABLED
            self.fq['state'] = DISABLED
            self.harm['state'] = DISABLED
            self.timeCste['state'] = DISABLED
            self.sensitivity['state'] = DISABLED
            self.current['state'] = DISABLED
            self.offset['state'] = DISABLED
            self.voltage['state'] = DISABLED
            self.currentMode['state'] = DISABLED
            self.source['state'] = DISABLED
        return

    def Lockin(self):
        self.w1 = str(self.amp.get())
        self.w2 = str(self.fq.get())
        self.w3 = str(self.harm.get())
        self.w4 = float(self.timeCste.get())
        self.w5 = float(self.sensitivity.get())
        self.w6 = str(self.current.get())
        self.w7 = str(self.offset.get())
        self.w8 = str(self.voltage.get())
        self.w9 = str(self.currentMode.get())
        self.w10 = str(self.source.get())

        self.ds.lockin_set_freq(self.w2)
        self.ds.lockin_time_const(self.w4)
        self.ds.lockin_sensitivity(self.w5)
        self.ds.initialize_lockin(harm=self.w3, current=self.w6, voltage=self.w8, current_mod=self.w9, source=self.w10,
                             offset=self.w7, amp=self.w1)
        return

    def Graphic(self):

        self.xs = []
        self.ys = []
        self.x = -self.v1
        self.ax.clear()
        self.ax.set_ylabel('Tension (mV)')
        self.ax.set_xlabel('Angle (°)')

        self.board.initialisation(self.v1)
        time.sleep(0.1)
        self.board.sens_horaire2(self.v1, self.v2, 3*self.w4, self.v3)

        while self.x <= 20:
            self.xs.append(float(self.x))
            self.x, self.y = self.x + self.v2, self.rm.query(self.ds, 'OUTP? 2')
            self.ys.append(float(self.y))
            self.ax.plot(self.xs, self.ys, 'r.', linewidth=1)
            self.ax.grid(visible=True)
            self.fig.savefig('courbe.png')
            self.photo = PhotoImage(master=self.tabGraph, file='courbe.png')
            self.canvas.create_image(0, 0, image=self.photo, anchor='nw')
            self.canvas.update()
            time.sleep(3 * self.w4)

        self.numberLines = len(self.xs)
        self.numberColumns = 2
        self.data = [self.xs, self.ys]

        fichier = open('data.txt', 'w')
        fichier.write('Angle')
        fichier.write(' Tension')

        # Ecriture dans le fichier data.txt des valeurs obtenues

        for i in range(self.numberLines):
            fichier.write('\n')
            fichier.write(str(self.data[0][i]))
            fichier.write(' ')
            fichier.write(str(self.data[1][i]))
        fichier.close()

        # Création du tableau de valeurs

        for i in range(self.numberLines):
            line = []
            for j in range(self.numberColumns):
                cell = Entry(self.tabMeasure, justify='center')
                cell.insert(0, round(self.data[0][i], 2))
                line.append(cell)
                cell.grid(row=i + 1, column=0)
            self.data.append(line)

        for i in range(self.numberLines):
            line = []
            for j in range(self.numberColumns):
                cell = Entry(self.tabMeasure, justify='center')
                cell.insert(0, round(self.data[1][i], 3))
                line.append(cell)
                cell.grid(row=i + 1, column=1)
            self.data.append(line)
        return

    def CurveFit(self):

        x, y = np.loadtxt('data.txt', skiprows=1, unpack=True)

        def gaussienne(x, A, sigma, mu):
            return (A / sigma / (2 * np.pi) ** 0.5) * np.exp(-(x - mu) ** 2 / 2 / sigma ** 2)

        fit, o = curve_fit(gaussienne, x, y)

        self.ax.plot(x, gaussienne(x, fit[0], fit[1], fit[2]), 'k')
        self.fig.savefig('courbe.png')
        self.photo = PhotoImage(master=self.tabGraph, file='courbe.png')
        self.canvas.create_image(0, 0, image=self.photo, anchor='nw')
        self.canvas.update()

        self.amplitude_v = Entry(self.tabMeasure, justify='center')
        self.amplitude_v.insert(0, round(fit[0], 3))
        self.amplitude_v.grid(row=1, column=3)

        self.sigma_v = Entry(self.tabMeasure, justify='center')
        self.sigma_v.insert(0, round(fit[1], 3))
        self.sigma_v.grid(row=1, column=2)

        self.mu_v = Entry(self.tabMeasure, justify='center')
        self.mu_v.insert(0, round(fit[2], 3))
        self.mu_v.grid(row=1, column=4)

        fichier = open('data.txt', 'a')
        fichier.write('\n\nSigma')
        fichier.write(' Amplitude')
        fichier.write(' Mu\n')
        fichier.write(str(fit[1]))
        fichier.write(' ')
        fichier.write(str(fit[0]))
        fichier.write(' ')
        fichier.write(str(fit[2]))
        fichier.close()
        return

    def Clear(self):
        self.ax.clear()
        self.ax.set_ylabel('Tension (mV)')
        self.ax.set_xlabel('Angle (°)')
        self.ax.set_xlim(-20, 20)
        self.xs = []
        self.ys = []
        self.ax.plot(self.xs, self.ys)
        self.ax.grid(visible=True)
        self.fig.savefig('courbe.png')
        self.photo = PhotoImage(master=self.tabGraph, file='courbe.png')
        self.canvas.create_image(0, 0, image=self.photo, anchor='nw')
        self.canvas.update()
        return

root = Tk()
my_gui = Interface(root)
root.mainloop()
