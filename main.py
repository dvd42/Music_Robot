from __future__ import print_function
import numpy as np
import subprocess
import RPi.GPIO as GPIO
from time import sleep
from picamera import PiCamera
from detect import process_image
import os
import time as t
import client

sensor_pin = 27
sensor_pin1 = 22

green_led_pin = 5
red_led_pin = 6

button_pin = 12

clk = 3
dt = 4

touch_pin = 25

# Motor Controller
in1 = 24
in2 = 23
in4 = 16
in3 = 14
en1 = 13

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(en1, GPIO.OUT)

pwm_1 = GPIO.PWM(en1, 100)


def setup():

    # IR sensors
    GPIO.setup(sensor_pin, GPIO.IN)
    GPIO.setup(sensor_pin1, GPIO.IN)

    GPIO.setup(green_led_pin, GPIO.OUT)  # LED Green
    GPIO.setup(red_led_pin, GPIO.OUT)  # LED Red

    # Buttons
    GPIO.setup(button_pin, GPIO.IN)

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


def rotate(tf):

    pwm_1.start(100)
    GPIO.output(in1, GPIO.LOW)
    GPIO.output(in2, GPIO.HIGH)
    GPIO.output(in3, GPIO.HIGH)
    GPIO.output(in4, GPIO.LOW)
    sleep(tf)
    stop()


def forward():

    pwm_1.start(100)
    GPIO.output(in1, GPIO.HIGH)
    GPIO.output(in3, GPIO.HIGH)
    GPIO.output(in2, GPIO.LOW)
    GPIO.output(in4, GPIO.LOW)


def stop():

    pwm_1.start(0)
    GPIO.output(in1, GPIO.LOW)
    GPIO.output(in2, GPIO.LOW)
    GPIO.output(in3, GPIO.LOW)
    GPIO.output(in4, GPIO.LOW)


def backward(tf):

    pwm_1.start(100)
    GPIO.output(in1, GPIO.LOW)
    GPIO.output(in3, GPIO.LOW)
    GPIO.output(in2, GPIO.HIGH)
    GPIO.output(in4, GPIO.HIGH)
    sleep(tf)


def rotary_sensor():

    counter = 0
    clkLastState = GPIO.input(clk)
    clkState = GPIO.input(clk)

    if clkState != clkLastState:

        now = t.time()

        while t.time() - now < 2:

            clkState = GPIO.input(clk)

            if clkState != clkLastState:

                counter += 1
                clkLastState = clkState

            sleep(0.01)

    return counter/4


def reposition():

    rotate(2.5)
    forward()
    now = t.time()

    sensor = 0
    sensor1 = 0

    while t.time() - now < 10:

        sensor = GPIO.input(sensor_pin)
        sensor1 = GPIO.input(sensor_pin1)

        sleep(0.2)

        print(sensor_pin, sensor)
        print(sensor_pin1, sensor1)

        if sensor and sensor1:
            backward(2)
            rotate(2.5)
            forward()

    stop()


def aplay_audio(audio):
    player = subprocess.Popen(["omxplayer", audio, "&"], stdin=subprocess.PIPE,
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    return player


def play_audio(audio):
    os.system("omxplayer " + audio)


def close_audio(audio_process):

    try:
        if audio_process is not None:
            audio_process.stdin.write("q")
            sleep(0.5)
    except IOError:
        pass


def scan(pic, camera, rotation_count):

    GPIO.output(green_led_pin, GPIO.HIGH)

    camera.capture('{}.png'.format(pic))
    persons = process_image('{}.png'.format(pic))

    if not persons:
        wii = aplay_audio("pre_made/wii.mp3")
        sleep(2)
        rotate(2)
        rotation_count += 1

    return persons, rotation_count


def navigate():

    forward()
    sir = aplay_audio("pre_made/sir.mp3")

    sensor = 0
    sensor1 = 0

    while not sensor and not sensor1:
        sensor = GPIO.input(sensor_pin)
        sensor1 = GPIO.input(sensor_pin1)

        sleep(0.1)

    stop()
    GPIO.output(green_led_pin, GPIO.LOW)

    close_audio(sir)


def generate_music(hat_counter):

    params = {}
    params['time'] = 1500
    params['tempo'] = 5
    params['scale'] = [2, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1]

    client.send_params(params)

    files = sorted(os.listdir("magenta_audio"))

    play_audio("pre_made/thank_you.mp3")

    now = t.time()
    song = None
    rotary = 0
    init = t.time()

    while True:

        if t.time() - init > 60:
            close_audio(song)
            break

        touch = GPIO.input(touch_pin)
        button = GPIO.input(button_pin)

        if not rotary:
            tempo = rotary_sensor()

            if tempo:
                params['tempo'] = tempo
                client.send_params(params)
                rotary = 1

        if button:
            scale = list(np.random.randint(0, 3, 12))
            params['scale'] = scale
            client.send_params(params)
            sleep(0.5)

        if len(files) != len(os.listdir("magenta_audio")):

            rotary = 0
            now = t.time()
            close_audio(song)

            files = sorted(os.listdir("magenta_audio"))

            song = aplay_audio(os.path.join("magenta_audio", files[-1]))
            init = t.time()

        elif t.time() - now > 18:
            now = t.time()
            song = aplay_audio(os.path.join("magenta_audio", files[-1]))

        if touch:
            hat_counter += 1
            init = t.time()
            sleep(0.5)

            close_audio(song)

            if hat_counter < 2:
                play_audio("pre_made/hat.mp3")
                song = aplay_audio(os.path.join("magenta_audio",
                                                files[-1]))

            else:
                close_audio(song)
                play_audio("pre_made/hat2.mp3")
                break

    return hat_counter


def interact_mode():

    GPIO.output(red_led_pin, GPIO.HIGH)
    button = 0
    play_audio("pre_made/hello.mp3")
    audios = [1, 1, 1]
    hat_counter = 0

    att = None
    sir = None
    nose = None

    init = t.time()
    timeout = 0

    while not button:

        if t.time() - init > 59:
            timeout = 1
            break

        button = GPIO.input(button_pin)

        if audios[0]:
            nose = aplay_audio("pre_made/nose.mp3")
            audios[0] = 0
            now = t.time()

        if t.time() - now > 5 and audios[1]:
            sir = aplay_audio("pre_made/sir.mp3")
            audios[1] = 0
            now = t.time()

        if t.time() - now > 8 and audios[2]:
            att = aplay_audio("pre_made/attention.mp3")
            audios[2] = 0
            now = t.time()

        if not any(audios) and t.time() - now > 6:
            audios = [1, 1, 1]

    close_audio(nose)
    close_audio(sir)
    close_audio(att)

    if not timeout:
        hat_counter = generate_music(hat_counter)

    return hat_counter


def search_mode(camera, button, rotation_count):

    while not button:

        button = GPIO.input(button_pin)

        if button:
            button = 1
            break

        persons, rotation_count = scan("front.png", camera, rotation_count)

        if persons:
            break

        if not button:
            button = GPIO.input(button_pin)
        else:
            button = 1
            break

        # If no one is around reposition
        if rotation_count >= 3 and not button:

            play_audio("pre_made/hellox2.mp3")

            aplay_audio("pre_made/help.mp3")

            reposition()
            rotation_count = 0

        if not button:
            button = GPIO.input(button_pin)

        else:
            button = 1
            break

    camera.close()

    if not button:
        navigate()

    status = interact_mode()

    # Turn leds off just in case
    GPIO.output(red_led_pin, GPIO.LOW)
    GPIO.output(green_led_pin, GPIO.LOW)

    return status


if __name__ == "__main__":

    try:
        while True:

            setup()
            rotation_count = 0
            button = 0
            camera = PiCamera()

            status = search_mode(camera, button, rotation_count)

            if status == 2:
                reposition()

    except KeyboardInterrupt:
        camera.close()
        GPIO.output(red_led_pin, GPIO.LOW)
        GPIO.output(green_led_pin, GPIO.LOW)
        GPIO.cleanup()
        pwm_1.start(0)
        exit()
