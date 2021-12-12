# -*- coding: utf-8 -*-
"""
Created on Fri Sep  10 09:00:00 2021

@author: ALFONSO Vincent
"""
import pyvisa

class Detection_synchrone :

	def __init__(self, instrument):
		self.instrument = instrument

	def lockin_set_freq(self, f):
		buf = self.instrument.write('FREQ ' + str(f))

	def lockin_time_const(self,time):
	#Set the Time Constant; 1microS (0), <=> 30 ks (21)
	#List of Time Constants:: 1micros(0), 3micros(1), 1ms(6), 3ms(7),
	# 10ms(8), 30ms(9), 100ms(10), 300ms(11), 1s(12), 3s(13),
	# 10s(14), 30s(15)
		if 3.e-6 > time and time >= 1.e-6 :
			buf=self.instrument.write("OFLT 0")
		if 10.e-6 > time and time >= 3.e-6 :
			buf=self.instrument.write("OFLT 1")
		if 30.e-6 > time and time >= 10.e-6 :
			buf=self.instrument.write("OFLT 2")
		if 100.e-6 > time and time >= 30.e-6 :
			buf=self.instrument.write("OFLT 3")
		if 300.e-6 > time and time >= 100.e-6 :
			buf=self.instrument.write("OFLT 4")
		if 1.e-3 > time and time >= 300.e-6 :
			buf=self.instrument.write("OFLT 5")
		if 3.e-3 > time and time >= 1.e-3 :
			buf=self.instrument.write("OFLT 6")
		if 10.e-3 > time and time >= 3.e-3 :
			buf=self.instrument.write("OFLT 7")
		if 30.e-3 > time and time >= 10.e-3 :
			buf=self.instrument.write("OFLT 8")
		if 100.e-3 > time and time >= 30.e-3 :
			buf=self.instrument.write("OFLT 9")
		if 300.e-3 > time and time >= 100.e-3 :
			buf=self.instrument.write("OFLT 10")
		if 1. > time and time >= 300.e-3 :
			buf=self.instrument.write("OFLT 11")
		if 3. > time and time >= 1. :
			buf=self.instrument.write("OFLT 12")
		if 10. > time and time >= 3. :
			buf=self.instrument.write("OFLT 13")
		if 30. > time and time >= 10. :
			buf=self.instrument.write("OFLT 14")
		if 100. > time and time >= 30. :
			buf=self.instrument.write("OFLT 15")
		if 300. > time and time >= 100. :
			buf=self.instrument.write("OFLT 16")
		if 1000. > time and time >= 300. :
			buf=self.instrument.write("OFLT 17")
		if 3000. > time and time >= 1000. :
			buf=self.instrument.write("OFLT 18")
		if 10000. > time and time >= 3000. :
			buf=self.instrument.write("OFLT 19")
		if 30000. > time and time >= 10000. :
			buf=self.instrument.write("OFLT 20")
		if time >= 300. :
			buf=self.instrument.write("OFLT 21")

	def lockin_sensitivity(self,v_level):
		#Set the Sensitivity; 1V (0), <=> 1nV (27)
		#List of Sensitivities: 1V(0), 500mV(1), 200mV(2),
		# 10mV(6), 5mV(7), 2mV(8), 1mV(9)
		# 500microV(10),200microV(11),100microV(12)
		if 0.5 < v_level and v_level <= 1 :
			self.instrument.write("SCAL 0")
		if 0.2 < v_level and v_level <= 0.5 :
			self.instrument.write("SCAL 1")
		if 0.1 < v_level and v_level <= 0.2 :
			self.instrument.write("SCAL 2")
		if 0.05 < v_level and v_level <= 0.1 :
			self.instrument.write("SCAL 3")
		if 0.02 < v_level and v_level <= 0.05 :
			self.instrument.write("SCAL 4")
		if 0.01 < v_level and v_level <= 0.02 :
			self.instrument.write("SCAL 5")
		if 0.005 < v_level and v_level <= 0.01 :
			self.instrument.write("SCAL 6")
		if 0.002 < v_level and v_level <= 0.005 :
			self.instrument.write("SCAL 7")
		if 0.001 < v_level and v_level <= 0.002 :
			self.instrument.write("SCAL 8")
		if 500.e-6 < v_level and v_level <= 0.001 :
			self.instrument.write("SCAL 9")
		if 200.e-6 < v_level and v_level <= 500.e-6 :
			self.instrument.write("SCAL 10")
		if 100.e-6 < v_level and v_level <= 200.e-6 :
			self.instrument.write("SCAL 11")
		if 50.e-6 < v_level and v_level <= 100.e-6 :
			self.instrument.write("SCAL 12")
		if 20.e-6 < v_level and v_level <= 50.e-6 :
			self.instrument.write("SCAL 13")
		if 10.e-6 < v_level and v_level <= 20.e-6 :
			self.instrument.write("SCAL 14")
		if 5.e-6 < v_level and v_level <= 10.e-6 :
			self.instrument.write("SCAL 15")
		if 2.e-6 < v_level and v_level <= 5.e-6 :
			self.instrument.write("SCAL 16")
		if 1.e-6 < v_level and v_level <= 2.e-6 :
			self.instrument.write("SCAL 17")
		if 0.5e-6 < v_level and v_level <= 1.e-6 :
			self.instrument.write("SCAL 18")
		if 0.2e-6 < v_level and v_level <= 0.5e-6 :
			self.instrument.write("SCAL 19")
		if 0.1e-6 < v_level and v_level <= 0.2e-6 :
			self.instrument.write("SCAL 20")
		if 0.05e-6 < v_level and v_level <= 0.1e-6 :
			self.instrument.write("SCAL 21")
		if v_level <= 50.e-9 :
			self.instrument.write("SCAL 22")
	
	def initialize_lockin(self, harm, current, voltage, current_mod, source, offset, amp):

		# DEFAULT SETTINGS FOR THE self
		# Set set the voltage input mode to : A (i=0) A-B (i=1)

		self.instrument.write("ISRC " + voltage)

		# Set the Current to : AC (i=0) , DC (i=1)
		self.instrument.write("ICPL " + current_mod)

		# Setting the harmonic to the 0
		self.instrument.write("HARM " + str(harm))

		# Set the offset in mV
		self.instrument.write("SOFF " + str(offset) + " MV")

		# Set the amplitude in mV
		self.instrument.write("SLVL " + str(amp) + " MV")

		# Set the current range to 10micA or 1nA
		self.instrument.write("ICUR " + str(current))

		# Set reference source
		self.instrument.write("RSRC " + source)

		self.instrument.write("PHAS -180")