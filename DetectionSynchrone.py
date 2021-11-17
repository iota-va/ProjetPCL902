import pyvisa

class DetectionSynchrone :

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