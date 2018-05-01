from __future__ import print_function
import RPi.GPIO as GPIO 
from time import sleep
import time as t
from picamera import PiCamera
from detect import process_image



sensor_pin = 27

green_led_pin = 5 
red_led_pin = 13
yellow_led_pin = 10

button1_pin = 12
button2_pin = 23

clk = 24
dt = 4

touch_pin = 25


def setup():

	GPIO.setwarnings(False)
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(sensor_pin, GPIO.IN)  # IR sensor

	GPIO.setup(green_led_pin, GPIO.OUT) # LED Green
	GPIO.setup(red_led_pin, GPIO.OUT) # LED Red
	GPIO.setup(yellow_led_pin, GPIO.OUT) # LED Yellow
	
	# Buttons
	GPIO.setup(button1_pin,GPIO.IN)
	GPIO.setup(button2_pin,GPIO.IN)

	# Rotary encoder
	GPIO.setup(clk, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
	GPIO.setup(dt, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


	# Touch sensor
	GPIO.setup(touch_pin,GPIO.IN)


def ir_sensor(): 
		sensor = 0
		while not sensor:
			sensor = GPIO.input(sensor_pin) 	
			if sensor: 
				print('Object Close') 
			else:
				print('Pathway Clear')

			sleep(0.5)

def leds(pin, color):


	GPIO.output(pin,GPIO.HIGH)
	print("{} LED is on".format(color))
	sleep(1)
	GPIO.output(pin,GPIO.LOW)


def button(pin,msg):

	pressed = 0
	print(msg)
	
	while not pressed: 
		
		pressed = GPIO.input(pin)

		if pressed:	
			leds(green_led_pin,'green')
			leds(red_led_pin,'red')
			leds(yellow_led_pin,'yellow')

def rotary_sensor():

	print("Spin me right round baby like a record baby")

	counter = 0
	clkLastState = GPIO.input(clk)
	while counter < 10:
		clkState = GPIO.input(clk)
		dtState = GPIO.input(dt)

		if clkState != clkLastState:
			if dtState != clkState:
				counter += 1
				print(counter,'Right')
			else:
				counter -= 1
				print(counter,'Left')
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
	camera.start_preview()
	sleep(5)
	camera.stop_preview()

	camera.capture('front_view.png')	
	now = t.time()
	process_image('front_view.png')
	print("Elapsed Time: {}".format(t.time() - now))	



setup()
ir_sensor()

button(button1_pin,"DONT press the RED button")
button(button2_pin,"DONT press the other RED button")

rotary_sensor()
touch_sensor()

GPIO.cleanup()	

camera()
	


