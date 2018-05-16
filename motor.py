import RPi.GPIO as GPIO
from time import sleep
import os
from multiprocessing import Process

in1 = 24
in2 = 23
in3 = 16
in4 = 14

#en1 = 13
#en2 = 13

GPIO.setmode(GPIO.BCM)
GPIO.setup(in1, GPIO.OUT)
GPIO.setup(in2, GPIO.OUT)
GPIO.setup(in3, GPIO.OUT)
GPIO.setup(in4, GPIO.OUT)

#GPIO.setup(en1, GPIO.OUT)
#GPIO.setup(en2, GPIO.OUT)

GPIO.output(in1, GPIO.LOW)
GPIO.output(in2, GPIO.LOW)
GPIO.output(in3, GPIO.LOW)
GPIO.output(in4, GPIO.LOW)

#p1 = GPIO.PWM(en1, 100)
#p2 = GPIO.PWM(en2, 100)

#p1.start(100)
#p2.start(100)


print("\n")
print("The default speed & direction of motor is LOW & Forward.....")
print("r-run s-stop f-forward b-backward l-low m-medium h-high e-exit")
print("\n")
GPIO.cleanup()

def play_audio(audio):
	os.system("mpg123 " + audio)


def drive():
	temp1 = 1
	while(1):

    		x = raw_input()

    		if x == 'r':
        		print("rotate")
        		if(temp1 == 1):
            			GPIO.output(in1, GPIO.LOW)
            			GPIO.output(in3, GPIO.HIGH)
            			GPIO.output(in2, GPIO.HIGH)
            			GPIO.output(in4, GPIO.LOW)
           		 	x = 'z'
				play_audio("test.mp3")
        		else:
            			GPIO.output(in1, GPIO.LOW)
            			GPIO.output(in3, GPIO.LOW)
            			GPIO.output(in2, GPIO.HIGH)
            			GPIO.output(in4, GPIO.HIGH)
            			print("backward")
            			x = 'z'

    		elif x == 's':
        		print("stop")
        		GPIO.output(in1, GPIO.LOW)
        		GPIO.output(in2, GPIO.LOW)
        		GPIO.output(in3, GPIO.LOW)
        		GPIO.output(in4, GPIO.LOW)
        		x = 'z'

    		elif x == 'f':
        		print("forward")
        		GPIO.output(in1, GPIO.HIGH)
        		GPIO.output(in3, GPIO.HIGH)
        		GPIO.output(in2, GPIO.LOW)
        		GPIO.output(in4, GPIO.LOW)
       		 	temp1 = 1
        		x = 'z'

    		elif x == 'b':
        		print("backward")
        		GPIO.output(in1, GPIO.LOW)
        		GPIO.output(in3, GPIO.LOW)
        		GPIO.output(in2, GPIO.HIGH)
        		GPIO.output(in4, GPIO.HIGH)
        		temp1 = 0
        		x = 'z'

    		elif x == 'l':
        		print("low")
        		p1.ChangeDutyCycle(50)
        		p2.ChangeDutyCycle(50)
        		x = 'z'

    		elif x == 'm':
        		print("medium")
        		p1.ChangeDutyCycle(75)
        		p2.ChangeDutyCycle(75)
        		x = 'z'

    		elif x == 'h':
        		print("high")
        		p1.ChangeDutyCycle(100)
        		p2.ChangeDutyCycle(100)
        		x = 'z'

    		elif x == 'e':
        		GPIO.cleanup()
			break

    		else:
        		print("<<<  wrong data  >>>")

#print("please enter the defined data to continue.....")


#process2 = Process(target=drive)
#process1 = Process(target=play_audio, args=["test.mp3"])

drive()

#process2.start()
#process1.start()

#process2.join()
#process1.join()
