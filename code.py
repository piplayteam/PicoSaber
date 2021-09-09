import audiocore
import audiomp3
import board
import audiobusio
import digitalio
import time
import busio
import adafruit_mpu6050
from digitalio import DigitalInOut, Direction, Pull
import neopixel

pixel_pin = board.GP0
num_pixels = 7
pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.0, auto_write=False)

RED = (255, 0, 0)
YELLOW = (255, 250, 0)
ORANGE = (255, 150, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
PURPLE = (180, 0, 255)
WHITE = (255, 255, 255)

SABER_COLOR = RED
# i2c = busio.I2C(board.GP3, board.GP2)
# mpu = adafruit_mpu6050.MPU6050(i2c)

btn = DigitalInOut(board.GP5)
btn.direction = Direction.INPUT
btn.pull = Pull.UP
prev_state = btn.value

whack = DigitalInOut(board.GP15)
whack.direction = Direction.INPUT
whack.pull = Pull.UP

i2s = audiobusio.I2SOut(board.GP27, board.GP28, board.GP26)

data = open("on.mp3", "rb")
saber_on = audiomp3.MP3Decoder(data)

data = open("on.mp3", "rb")
saber_off = audiomp3.MP3Decoder(data)

data = open("Clash clash.mp3", "rb")
saber_clash = audiomp3.MP3Decoder(data)
lightsaber_active = False
# led = digitalio.DigitalInOut(board.GP17)
# led.direction = digitalio.Direction.OUTPUT
# led.value = True



# print("playing")
# #i2s.play(mp3_2)
# while i2s.playing:
#   pass
# print("stopped")

# print("playing")
# #i2s.play(mp3_3)
# while i2s.playing:
#   pass
# print("stopped")

# time.sleep(0.5)

def idle_lightsaber(sound):
    while i2s.playing:
      pass
    
    i2s.play(sound, loop=True)


def start_lightsaber(sound):
    i2s.play(sound)

    pixels.brightness = 0.0
    sleep = 0.05
    pixels.fill(SABER_COLOR)
    pixels.show()

    pixels.brightness = 0.1
    pixels.show()
    time.sleep(sleep)

    pixels.brightness = 0.2
    pixels.show()
    time.sleep(sleep)

    pixels.brightness = 0.3
    pixels.show()
    time.sleep(sleep)

    pixels.brightness = 0.4
    pixels.show()
    time.sleep(sleep)

    pixels.brightness = 0.5
    pixels.show()
    time.sleep(sleep)

    pixels.brightness = 0.6
    pixels.show()
    time.sleep(sleep)

    pixels.brightness = 0.7
    pixels.show()
    time.sleep(sleep)

    pixels.brightness = 0.8
    pixels.show()
    time.sleep(sleep)

    pixels.brightness = 0.9
    pixels.show()
    time.sleep(sleep)

    pixels.brightness = 1.0
    pixels.show()
    lightsaber_active = True
    return lightsaber_active


def stop_lightsaber(sound):
    i2s.stop()

    i2s.play(sound)

    pixels.brightness = 0.7
    sleep = 0.05
    pixels.fill(SABER_COLOR)
    pixels.show()

    pixels.brightness = 0.6
    pixels.show()
    time.sleep(sleep)

    pixels.brightness = 0.5
    pixels.show()
    time.sleep(sleep)

    pixels.brightness = 0.4
    pixels.show()
    time.sleep(sleep)

    pixels.brightness = 0.3
    pixels.show()
    time.sleep(sleep)

    pixels.brightness = 0.2
    pixels.show()
    time.sleep(sleep)

    pixels.brightness = 0.1
    pixels.show()
    time.sleep(sleep)

    pixels.brightness = 0.0
    pixels.show()
    lightsaber_active = False
    return lightsaber_active

while True:
    print("lightsaber_active: ", lightsaber_active)
    cur_state = btn.value
    if cur_state != prev_state:
        if not cur_state:
            print("BTN is down")
            lightsaber_active = start_lightsaber(saber_on)
            #idle_lightsaber(saber_on)

        else:
          print("BTN is up")
          lightsaber_active = stop_lightsaber(saber_off)

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
      pixels.fill(SABER_COLOR)
      pixels.brightness = 1.0
      pixels.show()
    # led.value = False

    # pixels.fill(RED)
    # pixels.show()
    #time.sleep(1)
    #pixels.fill(ORANGE)
    #pixels.show()
    #time.sleep(1)
    # pixels.fill(YELLOW)
    # pixels.show()
    # time.sleep(1)
    # pixels.fill(GREEN)
    # pixels.show()
    # time.sleep(1)
    # pixels.fill(CYAN)
    # pixels.show()
    # time.sleep(1)
    # pixels.fill(BLUE)
    # pixels.show()
    # time.sleep(1)
    # pixels.fill(PURPLE)
    # pixels.show()

    # print("Acceleration: X:%.2f, Y: %.2f, Z: %.2f m/s^2"%(mpu.acceleration))
    # print("Gyro X:%.2f, Y: %.2f, Z: %.2f degrees/s"%(mpu.gyro))
    # print("Temperature: %.2f C"%mpu.temperature)
    # print("")
    # cur_state = btn.value
    # print(btn.value)
    # if cur_state != prev_state:
    #     if not cur_state:
    #         print("BTN is down")
    #     else:
    #         print("BTN is up")