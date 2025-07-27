from gpiozero import Servo, LED
import RPi.GPIO as GPIO
import time

# Pins
TRIG = 10
ECHO = 11
LED_PIN = 5

# Servo setup
left_servo = Servo(9)
right_servo = Servo(6)
led = LED(LED_PIN)

# GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

def get_distance():
    GPIO.output(TRIG, False)
    time.sleep(0.0002)

    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    pulse_start = time.time()
    timeout = pulse_start + 0.04

    while GPIO.input(ECHO) == 0 and time.time() < timeout:
        pulse_start = time.time()

    while GPIO.input(ECHO) == 1 and time.time() < timeout:
        pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150  # Speed of sound
    return distance

def move_servo_smoothly(servo, start, end, step_delay=0.05):
    step = 0.01 if end > start else -0.01
    pos = start
    while (step > 0 and pos < end) or (step < 0 and pos > end):
        servo.value = pos
        pos += step
        time.sleep(step_delay)

try:
    left_servo.value = 0  # 90 degrees neutral (approx.)
    right_servo.value = 0
    led.off()

    while True:
        dist = get_distance()
        print(f"Distance: {dist:.2f} cm")

        if dist <= 5:
            move_servo_smoothly(left_servo, left_servo.value or 0, -1)
            move_servo_smoothly(right_servo, right_servo.value or 0, 1)
            led.on()
        else:
            move_servo_smoothly(left_servo, left_servo.value or 0, 0)
            move_servo_smoothly(right_servo, right_servo.value or 0, 0)
            led.off()

        time.sleep(0.05)

except KeyboardInterrupt:
    print("Program stopped")
    GPIO.cleanup()
