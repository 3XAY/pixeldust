import board
import neopixel
from digitalio import DigitalInOut, Direction, Pull
import rotaryio
import supervisor
supervisor.runtime.autoreload = False

pixel_pin = board.GP28
num_pixels = 64

pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.3, auto_write=False,
                           pixel_order=(1, 0, 2, 3))

btn = DigitalInOut(board.GP4)
btn.direction = Direction.INPUT
btn.pull = Pull.UP

rotBtn = DigitalInOut(board.GP8)
rotBtn.direction = Direction.INPUT
rotBtn.pull = Pull.UP

rot = rotaryio.IncrementalEncoder(board.GP19, board.GP18)
lastPos = rot.position
b = 0.02
while True:
    position = rot.position
    posChange = position - lastPos
    if(btn.value and rotBtn.value):
        pixels.fill((255, 0, 0, 0))
    elif(not btn.value):
        pixels.fill((0, 255, 0, 0))
    else:
        pixels.fill((0, 0, 0, 255))
    if(posChange > 0):
        for _ in range(posChange):
            b=b-0.02
    elif(posChange < 0):
        for _ in range(-posChange):
            b=b+0.02
    if(b > 1.0):
        b = 1.0
    elif(b < 0):
        b = 0
    pixels.brightness = b
    pixels.show()
    print(b)
    lastPos = position
