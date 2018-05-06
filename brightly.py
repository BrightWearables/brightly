
"""
`brigtly_animations` - Animations class for use with
the Brightly Code Generator"
====================================================
* Author: Debra Ansell (GeekMomProjects)
"""
import time
import random
import neopixel

class Brightly:

	def __init__(self, strip, numpix):
		self.strip = strip
		self.numpix = numpix
		random.seed(int(time.monotonic()*1000))

	def __is_color__(self, item):
		return (type(item) is tuple)
	  
	def __is_number__(self, item):
		return (type(item) in (int, float))
		
	def __clear_pix__(self):
		self.strip.fill((0,0,0))
		self.strip.show()
		
	#returns RGB value from color __wheel__ position 0 - 255
	def __wheel__(self, pos): 
		if (pos < 0 or pos > 255):
			return (0,0,0)
		elif pos < 85:
			return (int(255-pos*3), int(pos*3), 0)
		elif pos < 170:
			pos -= 85
			return (0,int(255-pos*3),int(pos*3))
		else:
			pos -= 170
			return (int(pos*3),0, int(255 - pos*3))

	def random_color(self):
		return(self.__wheel__(random.randint(0,255)))
		
	def rotate_pix(self, npos):
		arr_i = [(0,0,0)]*self.numpix
		for i in range(self.numpix):
			arr_i[i] = self.strip[i]
		for i in range(self.numpix):
			self.strip[(i + npos) % self.numpix] = arr_i[i]
		self.strip.show()

	def set_one_pixel(self, index, col, show):
		if(index < self.numpix):
			if (self.__is_number__(col)):
				col = self.__wheel__(col*256/360)
			self.strip[index] = col
		if show:
			self.strip.show()

	def set_pixels(self, pixcols):
		if self.__is_number__(pixcols):
			pixcols = self.__wheel__(pixcols*256/360)
		if self.__is_color__(pixcols):
			self.strip.fill(pixcols)
		else:
			for i in range(min(len(pixcols), self.numpix)):
				if (self.__is_number__(pixcols[i])):
					self.strip[i] = self.__wheel__(int(pixcols[i]*256/360))
				else:
					self.strip[i] = pixcols[i]
		self.strip.show()
		
	def shift_pix(self, npos, doWrite=True):
		if (abs(npos) < self.numpix):
			if (npos > 0):
				for i in range(npos, self.numpix):
					self.strip[self.numpix-i] = self.strip[self.numpix - i - npos]
				for i in range(npos):
					self.strip[i] = (0,0,0)
			elif (npos < 0):
				npos = abs(npos)
				for i in range(npos, self.numpix):
					self.strip[i-npos] = self.strip[i]
				for i in range(npos):
					self.strip[self.numpix - i - 1] = (0,0,0)
		else:
			self.__clear_pix__()
		if(doWrite):
			self.strip.show()	
			
	def __interp_val__(self, first, last, cur, nstep):
		return round(first + (last - first) * cur/nstep)

	def __interp_tuple__(self, t1, t2, cur, nstep):
		return(self.__interp_val__(t1[0], t2[0], cur, nstep), self.__interp_val__(t1[1], t2[1], cur, nstep), self.__interp_val__(t1[2], t2[2], cur, nstep))

	#assumes start/end are both arrays of tuples with self.numpix elements - holding color values
	def __smooth_transition__(self, start, end, wait=0, nstep=8):
		single_color = self.__is_color__(end)
		for i in range(nstep):
			for j in range(self.numpix):
				if single_color:
					self.strip[j] = self.__interp_tuple__(start[j], end, i+1, nstep)
				else:
					self.strip[j] = self.__interp_tuple__(start[j], end[j], i+1, nstep)
			self.strip.show()
			if wait:
				time.sleep(wait)
			
	def smooth_change_to(self, pixcols, wait=0, nstep=8):
		arr_i = [(0,0,0)]*self.numpix
		arr_f = [(0,0,0)]*self.numpix

		if self.__is_number__(pixcols):
			pixcols = self.__wheel__(int(pixcols*256/360))
		
		if self.__is_color__(pixcols):
			for i in range(self.numpix):
				arr_i[i] = self.strip[i]
				arr_f[i] = pixcols
		else:
			for i in range(min(len(pixcols), self.numpix)):
				arr_i[i] = self.strip[i]
				if self.__is_number__(pixcols[i]):
					arr_f[i] = self.__wheel__(int(pixcols[i]*256/360))
				else:
					arr_f[i] = pixcols[i]
		self.__smooth_transition__(arr_i, arr_f, wait, nstep)
		
	def smooth_rotate_pix(self, npos, wait=0, nstep=8):
		arr_i = [(0,0,0)]*self.numpix
		arr_f = [(0,0,0)]*self.numpix

		for i in range(self.numpix):
			arr_i[i] = self.strip[i]
			arr_f[i] = self.strip[(i + npos) % self.numpix]
		self.__smooth_transition__(arr_i, arr_f, wait, nstep)
		
	def twinkle(self, nleds, cols, duration):
		nsteps = 10   #must be even
		self.strip.fill((0,0,0))
		leds = {}
		for i in range(0,nleds):
			j = random.randint(0,self.numpix-1)
			k = random.randint(0,len(cols)-1)
			while j in leds:
				j = random.randint(0,self.numpix-1)
			leds[j] = [k, int(i*nsteps/nleds)]
		
		start = time.monotonic()
		while (time.monotonic() - start < duration):
			for k,v in leds.items():
				if v[1] == nsteps:
					leds.pop(k, None)
					self.set_one_pixel(k, (0,0,0), False)
					j = random.randint(0,self.numpix-1)
					i = random.randint(0,len(cols)-1)
					while j in leds:
						j = random.randint(0,self.numpix-1)
					leds[j] = [i, 0]
				else:
					factor = (2.0*v[1]/nsteps)
					if (v[1] > nsteps/2):
						factor = 2-factor
					if self.__is_number__(cols[v[0]]):
						self.set_one_pixel(k, int(cols[v[0]]*factor), False)
					else:
						tup = cols[v[0]]
						self.set_one_pixel(k, (int(tup[0]*factor), int(tup[1]*factor), int(tup[2]*factor)), False)
					v[1] = v[1] + 1
			self.strip.show()
			time.sleep(0.02)

	def wipe(self, wait, dir, cols):
		first = 0
		last = self.numpix
		inc = 1
		if (self.__is_number__(cols)):
			cols = self.__wheel__(int(cols*255/360))
		single_color = self.__is_color__(cols)
		col = (0,0,0)
		if single_color:
			col = cols
		if (dir < 0):
			first = self.numpix-1
			last = -1
			inc = -1
		for j in range (first, last, inc):
			if (not single_color):
				col = cols[j]      
			self.strip[j] = col
			self.strip.show()
			time.sleep(wait)
			
	def scroll_morse(self, str, col, DIR=1, delay=0.1):
		MORSE = [".-","-...","-.-.","-..",".","..-.","--.","....","..",".---","-.-",".-..","--","-.","---",".--.","--.-",".-.","...","-","..-","...-",".--","-..-","-.--","--..","-----",".----","..---","...--","....-",".....","-....","--...","---..","----."]
		FIRST = 0
		if (DIR == -1):
			FIRST = self.numpix-1

		str = str.upper()
		length = len(str)
		binStr = ""
		newWord = False
		for i in range(length):
			ch = str[i]   
			chStr = ""
			if (ch <= '9' and ch >= '0'):
				chStr = MORSE[ord(ch) - 22]
			elif (ch <= 'Z' and ch >= 'A'):
				chStr = MORSE[ord(ch) - 65]
			elif ch == ' ':
				newWord = True
		
			chLen = len(chStr)
			for j in range(chLen):
				if chStr[j] == '.':
					binStr += "1"
				elif chStr[j] == '-':
					binStr += "111"
				if (j == chLen - 1): #end of char
					binStr += "   "
				else:
					binStr += " "
			
			if (newWord):
				binStr += "    "
				newWord = False
		 
		for b in binStr:
			next_led = (0,0,0)
			if (b == '1'):
				next_led = col
			self.shift_pix(DIR, False)
			self.strip[FIRST] = next_led
			self.strip.write()
			time.sleep(delay)
		
		for i in range(self.numpix-1):
			self.shift_pix(DIR, True)
			time.sleep(delay)       

		
