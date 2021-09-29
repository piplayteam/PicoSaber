import audiocore
import audiomp3
import board
import audiobusio
import digitalio
import time
import busio
from digitalio import DigitalInOut, Direction, Pull
import neopixel
# from adafruit_led_animation.color import RED, MAGENTA, ORANGE, TEAL, WHITE, PURPLE

i2s = audiobusio.I2SOut(board.GP27, board.GP28, board.GP26)
data = open("on.mp3", "rb")
saber_on = audiomp3.MP3Decoder(data)
i2s.play(saber_on)

pixel_pin = board.GP0
num_pixels = 59
pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=1.0, auto_write=False)

RED = (255, 0, 0)
YELLOW = (255, 250, 0)
ORANGE = (255, 150, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
PURPLE = (180, 0, 255)
WHITE = (255, 255, 255)

SABER_COLOR = RED


activation_btn = DigitalInOut(board.GP5)
activation_btn.direction = Direction.INPUT
activation_btn.pull = Pull.UP
prev_state = activation_btn.value

whack = DigitalInOut(board.GP15)
whack.direction = Direction.INPUT
whack.pull = Pull.UP


data = open("on.mp3", "rb")
saber_on = audiomp3.MP3Decoder(data)

data = open("on.mp3", "rb")
saber_off = audiomp3.MP3Decoder(data)

data = open("Clash clash.mp3", "rb")
saber_clash = audiomp3.MP3Decoder(data)

data = open("hum.mp3", "rb")
saber_hum = audiomp3.MP3Decoder(data)

lightsaber_active = False
play_hum = False

def color_chase(color, wait):
    pixels.brightness=1.0
    for i in range(num_pixels):
        pixels[i] = color
        time.sleep(wait)
        pixels.show()

def reverse_color_chase(color, wait):
    pixels.brightness=1.0
    for i in reversed(range(num_pixels)):
        pixels[i] = color
        time.sleep(wait)
        pixels.show()


def idle_lightsaber(sound):
    while i2s.playing:
      pass
    
    i2s.play(sound, loop=True)


def start_lightsaber(sound):
    global lightsaber_active
    i2s.play(sound)
    color_chase(SABER_COLOR,0.004)

    lightsaber_active = True


def stop_lightsaber(sound):
    global lightsaber_active
    if lightsaber_active == True:
        play_hum = False
        i2s.stop()

        i2s.play(sound)
        reverse_color_chase(0,0.004)
    
    lightsaber_active = False

while True:
    print("lightsaber_active: ", lightsaber_active)
    cur_state = activation_btn.value
    if cur_state != prev_state:
        if not cur_state:
            print("BTN is down")
            start_lightsaber(saber_on)

        else:
          print("BTN is up")
          stop_lightsaber(saber_off)

    prev_state = cur_state

    if not whack.value and lightsaber_active == True:
      print("whack is down")
      i2s.stop()
      i2s.play(saber_clash)
      pixels.fill(BLUE)
      pixels.brightness = 0.2
      pixels.show()
      time.sleep(1)
      pixels.brightness = 0.0
      pixels.show()


    if lightsaber_active == True:
        pixels.brightness = 1.0
        pixels.show()
    else:
        pixels.brightness = 0.0
        pixels.show()
    # idle_lightsaber(saber_hum)
    #   if play_hum == False:
    #     i2s.play(saber_clash, loop=True)
    #     play_hum = True

