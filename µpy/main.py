#A0A nubJAR POUPON
#0A0 adding mqtt button pub
#AAA fixed mqtt added Encoder (encoder.py)
#9☉☉ --> jar MUSTARD
#099 volt meter
#009 ⁂ lcd
#600 ⌚ +buzz
#630 re-write: lcd, encoder
#060 swap pin 2 to 0
#066 +temp & backlite
#666 nub'd

import upcd8544
import framebuf
import machine
import onewire
import ds18x20
from encoder import Encoder
from machine import Pin
from machine import PWM
from machine import SPI
from time import sleep_ms
from time import ticks_us
from time import ticks_diff
from utime import localtime

VERSION = "#666 15:42"
INTERVAL = 500
PUSH_PIN = const(0)
BUZZ_PIN = const(12)
LCD_RST = const(0)
LCD_CE = const(16)
LCD_DC = const(15)


push = Pin(PUSH_PIN, Pin.IN)
buzz = Pin(BUZZ_PIN, Pin.OUT)
enc = Encoder(5, 4, Pin.PULL_UP, 4, 0, 255)
ow = onewire.OneWire(Pin(3))
ds = ds18x20.DS18X20(ow)
roms = ds.scan()


pushed = False
count = 0
temp = 0

def timed_function(f, *args, **kwargs):
	myname = str(f).split(' ')[1]
	def new_func(*args, **kwargs):
		t = ticks_us()
		result = f(*args, **kwargs)
		delta = ticks_diff(ticks_us(), t)
		print('Function {} Time = {:6.3f}ms'.format(myname, delta/1000))
		return result
	return new_func

#@timed_function
def ver():
	print(VERSION)

ver()

def chirp(t = 10):
    buzz.high()
    sleep_ms(t)
    buzz.low()

chirp()

def push_handler(p):
	global pushed
	pushed = True
	print("PUSH")

push.irq(trigger=Pin.IRQ_FALLING, handler=push_handler)

spi = SPI(1, baudrate=80000000, polarity=0, phase=0)
lcd = upcd8544.PCD8544(spi, Pin(0), Pin(16), Pin(15), Pin(0))

width = 84
height = 48
pages = height // 8
buffer = bytearray(pages * width)
framebuf = framebuf.FrameBuffer1(buffer, width, height)
framebuf.text("red/watch", 0, 1, 1)
framebuf.text(VERSION, 0, 8, 1)
lcd.data(buffer)

buzz = Pin(12, Pin.OUT)

chirp()

def main():
	global lcd, temp, framebuf, pushed, count
	bar = True
	while 1:
		t = localtime()

		count = enc.value

		if pushed:
			pushed = False
			chirp()

		framebuf.fill(0)
		framebuf.text("{:d} {:.2f}'C".format(count, temp), 4, 0, 1)
		framebuf.text(VERSION, 2, 40, 1)
		framebuf.text(" {:02d}:{:02d}:{:02d}".format(t[3], t[4], t[5]), 0, 16, 1)

		if bar:
			bar = False
			for x in range(0,84):
				framebuf.pixel(x, 32, 1)
		else:
			bar = True
			ds.convert_temp()
			temp = ds.read_temp(roms[0])

		lcd.data(buffer)
		sleep_ms(INTERVAL)

main()
