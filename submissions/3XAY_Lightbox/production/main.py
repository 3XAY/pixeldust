#Imports
import board
import neopixel
from digitalio import DigitalInOut, Direction, Pull
import rotaryio
import supervisor
from adafruit_debouncer import Debouncer
supervisor.runtime.autoreload = False #Turn off auto-reload

#Set the neopixel data pin and the # of LEDs
pixel_pin = board.GP28
num_pixels = 64

#Create the neopixel object with the correct pin order for RGBW and a default brightness
pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.02, auto_write=False,
                           pixel_order=(1, 0, 2, 3))

#Create the button (mechanical switch) pin and the associated Debouncer object
btnPin = DigitalInOut(board.GP4)
btnPin.direction = Direction.INPUT
btnPin.pull = Pull.UP
btn = Debouncer(btnPin)

#Create the button (rotary encoder) pin and the associated Debouncer object
rotBtnPin = DigitalInOut(board.GP8)
rotBtnPin.direction = Direction.INPUT
rotBtnPin.pull = Pull.UP
rotBtn = Debouncer(rotBtnPin)

#Create the rotary encoder object
rot = rotaryio.IncrementalEncoder(board.GP19, board.GP18, divisor=2) #divisor=2 ensures that this encoder sends 1 tick in software for every physical tick
lastPos = rot.position #Sets the position to the current position so it can be used as a reference for when the value changes

bright = 0.02 #Defaults the brightness value to 2%
channel = 5 #Defaults to changing the brightness of the LEDs

r = 0
g = 0
b = 0
w = 255

while True: #Main loop
	#Update the encoder so I know how many ticks to change things by since the last iteration of the loop
	position = rot.position
	posChange = position - lastPos
    
	#Update the button objects' states
	rotBtn.update()
	btn.update()

	#Handle the "channels" (RGBW + Brightness), updates on release
	if(rotBtn.rose):
		channel = channel + 1
		if(channel > 5):
			channel = 1

	#Changes the red value when the encoder is on the right channel
	if(channel == 1):
		if(posChange > 0):
			for _ in range(posChange):
				r = r - 1
		elif(posChange < 0):
			for _ in range(-posChange):
				r = r + 1
		if(r > 255):
				r = 255
		if(r < 0):
			r = 0

	#Changes the green value when the encoder is on the right channel
	if(channel == 2):
		if(posChange > 0):
			for _ in range(posChange):
				g = g - 1
		elif(posChange < 0):
			for _ in range(-posChange):
				g = g + 1
		if(g > 255):
				g = 255
		if(g < 0):
			g = 0

	#Changes the blue value when the encoder is on the right channel
	if(channel == 3):
		if(posChange > 0):
			for _ in range(posChange):
				b = b - 1
		elif(posChange < 0):
			for _ in range(-posChange):
				b = b + 1
		if(b > 255):
				b = 255
		if(b < 0):
			b = 0

	#Changes the white value when the encoder is on the right channel
	if(channel == 4):
		if(posChange > 0):
			for _ in range(posChange):
				w = w - 1
		elif(posChange < 0):
			for _ in range(-posChange):
				w = w + 1
		if(w > 255):
				w = 255
		if(w < 0):
			w = 0
	
	#Changes the brightness when the encoder is on the right channel
	if(channel == 5):
		if(posChange > 0):
			for _ in range(posChange):
				bright = bright - 0.02
		elif(posChange < 0):
			for _ in range(-posChange):
				bright = bright + 0.02
		if(bright > 1.0):
				bright = 1.0
		if(bright < 0):
			bright = 0

	#Updates the pixel's colors + brightness
	pixels.brightness = bright
	pixels.fill((r, g, b, w))

	#Send the data to the pixels
	pixels.show()

	#Update the lastPos variable so it can be compared with the rotary encoder's new position on the next iteration
	lastPos = position
