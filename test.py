from __future__ import print_function
import RPi.GPIO as GPIO
from time import sleep
import time as t
from picamera import PiCamera
from detect import process_image
import os
from multiprocessing import Process

sensor_pin = 27
sensor_pin1 = 22

green_led_pin = 5
red_led_pin = 6
yellow_led_pin = 10

button1_pin = 2
button2_pin = 12

clk = 3
dt = 4

touch_pin = 25

# Motor Controller
in1 = 24
in2 = 23
in3 = 16
in4 = 14


def setup():

    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)

    # IR sensors
    GPIO.setup(sensor_pin, GPIO.IN)
    GPIO.setup(sensor_pin1, GPIO.IN)

    GPIO.setup(green_led_pin, GPIO.OUT)  # LED Green
    GPIO.setup(red_led_pin, GPIO.OUT)  # LED Red
    GPIO.setup(yellow_led_pin, GPIO.OUT)  # LED Yellow

    # Buttons
    GPIO.setup(button1_pin, GPIO.IN)
    GPIO.setup(button2_pin, GPIO.IN)

    # Rotary encoder
    GPIO.setup(clk, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(dt, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    # Touch sensor
    GPIO.setup(touch_pin, GPIO.IN)

    # Motor Controller
    GPIO.setup(in1, GPIO.OUT)
    GPIO.setup(in2, GPIO.OUT)
    GPIO.setup(in3, GPIO.OUT)
    GPIO.setup(in4, GPIO.OUT)

    GPIO.output(in1, GPIO.LOW)
    GPIO.output(in2, GPIO.LOW)
    GPIO.output(in3, GPIO.LOW)
    GPIO.output(in4, GPIO.LOW)


def ir_sensor(pin):
    sensor = 0
    while not sensor:
        sensor = GPIO.input(pin)
        if sensor:
            print('Object Close')
        else:
            print('Pathway Clear')

        sleep(0.5)


def leds(pin, color):

    GPIO.output(pin, GPIO.HIGH)
    print("{} LED is on".format(color))
    sleep(1)
    GPIO.output(pin, GPIO.LOW)


def button(pin, msg):

    pressed = 0
    print(msg)

    while not pressed:

        pressed = GPIO.input(pin)

        if pressed:
            leds(green_led_pin, 'green')
            leds(red_led_pin, 'red')
            leds(yellow_led_pin, 'yellow')


def rotary_sensor():

    print("Spin me right round baby like a record baby")

    counter = 0
    clkLastState = GPIO.input(clk)
    while counter < 50:
        clkState = GPIO.input(clk)
        dtState = GPIO.input(dt)

        if clkState != clkLastState:
            if dtState != clkState:
                counter += 1
                print(counter, 'Right')
            else:
                counter += 1
                print(counter, 'Left')
                clkLastState = clkState

        sleep(0.01)


def touch_sensor():

    touch = 0
    print("Touch me")
    while not touch:
        touch = GPIO.input(touch_pin)

        if touch:
            print("Ouch not so hard")


def camera():

    camera = PiCamera()

    camera.capture('front_view.png')
    now = t.time()
    process_image('front_view.png')
    print("Elapsed Time: {}".format(t.time() - now))


def forward(pin1, pin2):

   GPIO.output(in1, GPIO.LOW)
   GPIO.output(in2, GPIO.HIGH)
   GPIO.output(in3, GPIO.LOW)
   GPIO.output(in4, GPIO.HIGH)

   GPIO.output(in1, GPIO.LOW)
   GPIO.output(in2, GPIO.LOW)
   GPIO.output(in3, GPIO.LOW)
   GPIO.output(in4, GPIO.LOW)

def backward(tf):

    GPIO.output(in1, GPIO.HIGH)
    GPIO.output(in2, GPIO.LOW)
    GPIO.output(in3, GPIO.HIGH)
    GPIO.output(in4, GPIO.LOW)
    sleep(tf)


setup()


def sound_test():
	os.system("mpg123 test.mp3")

def led_test():
	while True:

		GPIO.output(green_led_pin, GPIO.HIGH)
		sleep(0.5)
		GPIO.output(green_led_pin, GPIO.LOW)
		GPIO.output(red_led_pin, GPIO.HIGH)
		sleep(0.5)
		GPIO.output(red_led_pin, GPIO.LOW)


#p0 = Process(target=sound_test)
#p1 = Process(target=led_test)

#p0.start()
#p1.start()

#p0.join()
#p1.join()



ir_sensor(sensor_pin)
ir_sensor(sensor_pin1)

#button(button1_pin, "DONT press the RED button")
button(button2_pin, "DONT press the other RED button")

rotary_sensor()
touch_sensor()

#Popen(['mpg123', 'xxi73-z4sq2.mp3', '--loop 100'])
#forward(sensor_pin, sensor_pin1)

GPIO.cleanup()

# camera()
