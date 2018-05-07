#Auto generated CircuitPython Code
import board
import neopixel
import time
import brightly
numpix = 14

strip = neopixel.NeoPixel(board.D1, numpix, brightness=0.15, auto_write=False)
brightly = brightly.Brightly(strip, numpix)

while True:
    brightly.wipe(0.05, 1, (255, 0, 0))
    brightly.wipe(0.05, -1, (0,0,255))
    brightly.twinkle(8, [(255,0,0),(0,255,0),(0,0,255)], 5)
    brightly.scroll_morse("hi there", (255,0,0))
    brightly.smooth_change_to((0,255,0))
    brightly.smooth_change_to([(255,0,0),(201,54,0),(147,108,0),(90,165,0),(36,219,0),(0,237,18),(0,183,72),(0,126,129),(0,75,180),(0,18,237),(33,0,222),(90,0,165),(144,0,111),(198,0,57)])
    for i in range(16):
        brightly.smooth_rotate_pix(1)
    for i in range(16):
        brightly.set_pixels([(255,0,0), (0,0,0), (255,0,0), (0,0,0), (255,0,0), (0,0,0), (255,0,0), (0,0,0), (255,0,0), (0,0,0), (255,0,0), (0,0,0), (255, 0, 0), (0,0,0)])
        time.sleep(0.4)
        brightly.smooth_change_to([(0,0,0), (255,0,0), (0,0,0), (255,0,0), (0,0,0), (255,0,0), (0,0,0), (255,0,0), (0,0,0), (255,0,0), (0,0,0), (255, 0, 0), (0,0,0), (255, 0, 0)])
