#Imports
import board
import time
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
pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=1.0, auto_write=False,
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

bright = 1.0 #Defaults the brightness value to 100%
channel = 5 #Defaults to changing the brightness of the LEDs

#RGBW variables to control each color channel
r = 0
g = 0
b = 0
w = 255

#The colors tuple makes it easier to update based on presets
colors = (r, g, b, w)

#Presets
presets = [(255, 255, 255, 255, 1), (255, 0, 0, 0, 1), (0, 255, 0, 0, 1), (0, 0, 255, 0, 1), (0, 0, 0, 255, 1)]
presetNum = 0
rainbowPreset = False

#The following code is from the Adafruit RGBW Neopixel Demo
def colorwheel(pos):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    if pos < 0 or pos > 255:
        return (0, 0, 0, 0)
    if pos < 85:
        return (255 - pos * 3, pos * 3, 0, 0)
    if pos < 170:
        pos -= 85
        return (0, 255 - pos * 3, pos * 3, 0)
    pos -= 170
    return (pos * 3, 0, 255 - pos * 3, 0)

def rainbow_cycle():
	for j in range(255):
		for i in range(num_pixels):
			rc_index = (i * 256 // num_pixels) + j
			pixels[i] = colorwheel(rc_index & 255)
		pixels.show()
		btn.update() #The following is added to allow users to exit this mode
		if(btn.rose):
			return False

#End Adafruit code

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

	#Set the presets
	if(btn.rose):
		presetNum = presetNum  + 1 #Move to the next preset
		if(presetNum == len(presets)): #Special rainbow mode
			presetNum = 0 #Reset first
			rainbowPreset = True
		else:
			rainbowPreset = False
		if(presetNum > len(presets)): #Make sure the preset is valid, otherwise loop back to the start
			presetNum = 0
		colors = presets[presetNum] #Update the colors tuple
		r, g, b, w, bright = colors

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
		colors = (r, g, b, w)

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
		colors = (r, g, b, w)

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
		colors = (r, g, b, w)

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
	colors = (r, g, b, w)
	
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
		colors = (r, g, b, w)

	if(rainbowPreset): #When the rainbow is rainbowing
		rainbowPreset = rainbow_cycle()
		if(rainbowPreset == None):
			rainbowPreset = True
	else: #Normal situation
		#Updates the pixel's colors + brightness
		pixels.brightness = bright
		pixels.fill(colors)

		#Send the data to the pixels
		pixels.show()
		print(colors)
		#Update the lastPos variable so it can be compared with the rotary encoder's new position on the next iteration
		lastPos = position
