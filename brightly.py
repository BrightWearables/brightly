
"""
`brigtly_animations` - Animations class for use with
the Brightly Code Generator"
====================================================
* Author: Debra Ansell (GeekMomProjects)
"""
import time
import random
import neopixel

"""
Class to perforn color and animation operations on a strip of Neopixels. 
The functions match those available on the Brightly code generator: 
http:\\www.BrightWearaables.com\brightly\index.html
"""
class Brightly:

	def __init__(self, strip, numpix):
		self.strip = strip
		self.numpix = numpix
		self.buf_i = bytearray(self.numpix*3)    #Working buffers for RGB tuples
		self.buf_f = bytearray(self.numpix*3)    #for functions requiring buffers
		random.seed(int(time.monotonic()*1000))
		
	def __read_buf_tuple__(self, buf, index):
		offset = index*3;
		return (buf[offset], buf[offset+1], buf[offset+2])
		
	def __write_buf_tuple__(self, buf, index, tup):
		offset = index*3;
		buf[offset] = tup[0]
		buf[offset+1] = tup[1]
		buf[offset+2] = tup[2]
		
	def __set_strip_from_buf__(self, buf):
		for i in range(numpix):
			self.strip[i] = self.__read_buf_tuple__(buf, i)
			
	def __set_buf_from_strip__(self, buf):
		for i in range(self.numpix):
			self.__write_buf_tuple__(buf, i, self.strip[i])
			
	def __is_color__(self, item):
		return (type(item) is tuple)
	  
	def __is_number__(self, item):
		return (type(item) in (int, float))
		
	def __clear_pix__(self):
		self.strip.fill((0,0,0))
		self.strip.show()
		
	#returns RGB value from color __wheel__ position 0 - 255. 
	# From adafruit neopxiel CircuitPython sample code
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
	
	#Brightly uses a 360 degree wheel, so convert to 
	def __wheel_degrees__(self, deg):
		return self.__wheel__(int(deg*256/360))

	def random_color(self):
		return(self.__wheel__(random.randint(0,255)))
		
	#rotates the pixels in the strip - wraps ends
	def rotate_pix(self, npos):
		self.__set_buf_from_strip__(self.buf_i)
		for i in range(self.numpix):
			self.strip[(i + npos) % self.numpix] = self.__read_buf_tuple__(self.buf_i, i)
		self.strip.show()

	def set_one_pixel(self, index, col, show):
		if(index < self.numpix):
			if (self.__is_number__(col)):
				col = self.__wheel_degrees__(col)
			self.strip[index] = col
		if show:
			self.strip.show()

	def set_pixels(self, pixcols):
		if self.__is_number__(pixcols):
			pixcols = self.__wheel_degrees__(pixcols)
		if self.__is_color__(pixcols):
			self.strip.fill(pixcols)
		else:
			for i in range(min(len(pixcols), self.numpix)):
				if (self.__is_number__(pixcols[i])):
					self.strip[i] = self.__wheel_degrees__(pixcols[i])
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
			
	#interpolation functions for use with incremental color change		
	def __interp_val__(self, first, last, cur, nstep):
		return first + (last - first) * cur/nstep

	def __interp_tuple__(self, t1, t2, cur, nstep):
		return tuple(int(round(self.__interp_val__(t1[i], t2[i], cur, nstep))) for i in range(len(t1)))

	#start/end are both bytearray buffers holding RGB values
	def __smooth_transition__(self, start, end, wait=0, nstep=8):
		for i in range(nstep+1):
			for j in range(self.numpix):
				self.strip[j] = self.__interp_tuple__(self.__read_buf_tuple__(start, j), self.__read_buf_tuple__(end, j), i, nstep)
			self.strip.show()
			if wait:
				time.sleep(wait)
				
	#returns a pattern of repeating colors created from the array cols
	def repeat_pattern(self, cols):
		led_pattern = [(0,0,0)]*self.numpix
		j = 0;
		for i in range(self.numpix):
			if self.__is_color__(cols[j]):
				led_pattern[i] = cols[j]
			elif self.__is_number__(cols[j]):
				led_pattern[i] = self.__wheel__(cols[j])
			j = (j + 1) % len(cols)
		return led_pattern
					
	#returns list of RGB tuples
	def rainbow(self, start, end):
		inc = (end-start)/self.numpix
		return [self.__wheel_degrees__(int(round(start + i*inc))) for i in range(self.numpix)]
			
	#interpolates nsteps when changing between colors			
	def smooth_change_to(self, pixcols, wait=0, nstep=8):
		self.__set_buf_from_strip__(self.buf_i)
	
		if self.__is_number__(pixcols):
			pixcols = self.__wheel_degrees__(pixcols)
					
		if self.__is_color__(pixcols):
			for i in range(self.numpix):
				self.__write_buf_tuple__(self.buf_f, i, pixcols)
		else:
			for i in range(min(len(pixcols), self.numpix)):
				if self.__is_number__(pixcols[i]):
					self.__write_buf_tuple__(self.buf_f, i, self.__wheel_degrees__(pixcols[i]))
				else:
					self.__write_buf_tuple__(self.buf_f, i, pixcols[i])
					
		self.__smooth_transition__(self.buf_i, self.buf_f, wait, nstep)
		
	def smooth_rotate_pix(self, npos, wait=0, nstep=8):
		self.__set_buf_from_strip__(self.buf_i)

		for i in range(self.numpix):
			self.__write_buf_tuple__(self.buf_f, i, self.strip[(i + npos) % self.numpix])

		self.__smooth_transition__(self.buf_i, self.buf_f, wait, nstep)
		
	def twinkle(self, nleds, cols, duration):
		nsteps = 10   # number of brightness steps in a pixel's lifetime. must be even.
		self.strip.fill((0,0,0))
		leds = {}
		for i in range(0,nleds):
			j = random.randint(0,self.numpix-1)
			k = random.randint(0,len(cols)-1)
			while j in leds:					#pick an unlit LED
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
					while j in leds:            #pick an unlit LED
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

    #"wipes" a color or pattern from one side of strip to the other			
	def wipe(self, wait, dir, cols):
		first = 0
		last = self.numpix
		inc = 1
		if (self.__is_number__(cols)):
			cols = self.__wheel_degrees__(cols)
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
	
	#scans a group of 3 pixels back and forth across "len" leds for duration seconds
	def scan(self, col, len, wait, duration):
		dir = 1
		pos = 1
		longpos = 1
		prev = pos - dir
		next = (pos + dir) % self.numpix
		if (self.__is_number__(col)):
			col = self.__wheel_degrees__(col)
		start = time.monotonic()
		while (time.monotonic() -   start < duration):
			self.strip[prev] = (0,0,0)
			self.strip[next] = (0,0,0)
			if (longpos == 0 and dir == -1):
				dir = 1
			elif (longpos == len-1 and dir == 1):
				dir = -1
			pos = (pos + dir) % self.numpix
			prev = (prev + dir) % self.numpix
			next = (next + dir) % self.numpix
			longpos = (longpos + dir) % len
			self.strip[pos] = col
			self.strip[prev] = [col[0] >> 1, col[1] >> 1, col[2] >> 2]
			self.strip[next] = self.strip[prev]
			self.strip.show()
			time.sleep(wait)
		
	#theater chase effect
	def theater_chase(self, col, wait, duration):
		start = time.monotonic()
		while (time.monotonic() - start < duration):
			for i in range(3):
				for j in range (0, self.numpix-2, 3):
					self.strip[i+j] = col
				self.strip.show()
				time.sleep(wait)
				for j in range (0, self.numpix-2, 3):
					self.strip[i+j] = [0,0,0]
			
					
			
	#TBD - make this function more efficient. Works ok for now though.
	def scroll_morse(self, str, col, DIR=1, delay=0.1):
		MORSE = [".-","-...","-.-.","-..",".","..-.","--.","....","..",".---","-.-",".-..","--","-.","---",".--.","--.-",".-.","...","-","..-","...-",".--","-..-","-.--","--..","-----",".----","..---","...--","....-",".....","-....","--...","---..","----."]
		FIRST = 0
		if (DIR == -1):
			FIRST = self.numpix-1

		str = str.upper()
		length = len(str)
		binStr = ""
		newWord = False
		for i in range(length): #deconstruct one letter at a time
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
			self.strip.show()
			time.sleep(delay)
		
		for i in range(self.numpix-1):
			self.shift_pix(DIR, True)
			time.sleep(delay)       

		
