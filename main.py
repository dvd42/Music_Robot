from __future__ import print_function
import RPi.GPIO as GPIO
from time import sleep
import time as t
from picamera import PiCamera
from detect import process_image


sensor_pin = 27
sensor_pin1 = 22

green_led_pin = 5
red_led_pin = 6

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

en2 = 13 # PWM


def setup():

    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)

    # IR sensors
    GPIO.setup(sensor_pin, GPIO.IN)
    GPIO.setup(sensor_pin1, GPIO.IN)

    GPIO.setup(green_led_pin, GPIO.OUT)  # LED Green
    GPIO.setup(red_led_pin, GPIO.OUT)  # LED Red

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

    #GPIO.setup(en2,GPIO.OUT)

    return PiCamera()


def rotate(rt, v):

    #p2.start(v)
    GPIO.output(in1, GPIO.LOW)
    GPIO.output(in2, GPIO.HIGH)
    GPIO.output(in3, GPIO.HIGH)
    GPIO.output(in4, GPIO.LOW)
    sleep(rt)
    stop()

def forward():

    GPIO.output(in1, GPIO.HIGH)
    GPIO.output(in3, GPIO.HIGH)
    GPIO.output(in2, GPIO.LOW)
    GPIO.output(in4, GPIO.LOW)


def stop():

    GPIO.output(in1, GPIO.LOW)
    GPIO.output(in2, GPIO.LOW)
    GPIO.output(in3, GPIO.LOW)
    GPIO.output(in4, GPIO.LOW)
    #p2.start(0)


def leds(pin, color):

    GPIO.output(pin, GPIO.HIGH)
    sleep(1)
    GPIO.output(pin, GPIO.LOW)

def search_mode(id, camera):

    camera.capture('{}.png'.format(id))
    persons = process_image('{}.png'.format(id))

    if not persons:
        rotate(2, 100)
        search_mode(id + 1, camera)

    return


def navigate(pin, pin1):

    forward()

    sensor = 0
    sensor1 = 0
    while not sensor or not sensor1:
        sensor = GPIO.input(pin)
        sensor1 = GPIO.input(pin)

        sleep(0.1)


    stop()
    GPIO.output(green_led_pin, GPIO.LOW)

camera = setup()

#p2 = GPIO.PWM(en2, 100)
GPIO.output(green_led_pin, GPIO.HIGH)
search_mode(0, camera)

navigate(sensor_pin, sensor_pin1)



GPIO.cleanup()
