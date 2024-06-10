import RPi.GPIO as GPIO
import time
from gpiozero import DistanceSensor
import json
import random

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

LED = 21

Motor1_PWM = 18
Motor1_IN1 = 17
Motor1_IN2 = 22

Motor2_PWM = 19
Motor2_IN1 = 24
Motor2_IN2 = 4

Button = 5  # Assuming the pushbutton is connected to GPIO pin 5
Right_Speed_Sensor = 23  # GPIO pin connected to the speed sensor of the right wheel
Left_Speed_Sensor = 16   # GPIO pin connected to the speed sensor of the left wheel

GPIO.setup(Motor1_PWM, GPIO.OUT)
GPIO.setup(Motor1_IN1, GPIO.OUT)
GPIO.setup(Motor1_IN2, GPIO.OUT)

GPIO.setup(Motor2_PWM, GPIO.OUT)
GPIO.setup(Motor2_IN1, GPIO.OUT)
GPIO.setup(Motor2_IN2, GPIO.OUT)

GPIO.setup(LED, GPIO.OUT)
GPIO.setup(Button, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(Right_Speed_Sensor, GPIO.IN)
GPIO.setup(Left_Speed_Sensor, GPIO.IN)

motor1_pwm = GPIO.PWM(Motor1_PWM, 100)  # Initialize PWM instance for Motor 1
motor2_pwm = GPIO.PWM(Motor2_PWM, 100)  # Initialize PWM instance for Motor 2

motor1_pwm.start(0)  # Start PWM for Motor 1 with 0% duty cycle (stopped)
motor2_pwm.start(0)  # Start PWM for Motor 2 with 0% duty cycle (stopped)

sensor = DistanceSensor(echo=27, trigger=25)

def drive_backward(speed):
    GPIO.output(LED, GPIO.HIGH)
    GPIO.output(Motor1_IN1, GPIO.LOW)
    GPIO.output(Motor1_IN2, GPIO.HIGH)
    GPIO.output(Motor2_IN1, GPIO.LOW)
    GPIO.output(Motor2_IN2, GPIO.HIGH)
    motor1_pwm.ChangeDutyCycle(speed)
    motor2_pwm.ChangeDutyCycle(speed)

def stop_motors():
    GPIO.output(Motor1_IN1, GPIO.LOW)
    GPIO.output(Motor1_IN2, GPIO.LOW)
    GPIO.output(Motor2_IN1, GPIO.LOW)
    GPIO.output(Motor2_IN2, GPIO.LOW)
    motor1_pwm.ChangeDutyCycle(0)
    motor2_pwm.ChangeDutyCycle(0)
    GPIO.output(LED, GPIO.LOW)

def turn_random_angle():
    angle = random.randint(0, 360)
    duration = angle / 360  # Assume it takes 1 second to turn 360 degrees
    GPIO.output(Motor1_IN1, GPIO.HIGH)
    GPIO.output(Motor1_IN2, GPIO.LOW)
    GPIO.output(Motor2_IN1, GPIO.LOW)
    GPIO.output(Motor2_IN2, GPIO.HIGH)
    motor1_pwm.ChangeDutyCycle(50)
    motor2_pwm.ChangeDutyCycle(50)
    time.sleep(duration)
    stop_motors()

try:
    # Move backward for a certain distance (20 cm)
    drive_backward(30)  # Set your initial speed
    time.sleep(1)  # Adjust the duration based on your robot's speed to travel 20 cm
    stop_motors()
    
    # Turn a random angle
    turn_random_angle()
    motor1_pwm.stop()
    motor2_pwm.stop()
    sensor.close()
    
    time.sleep(1)
    
    # Call the first script
    exec(open('./python/script_1.py').read())

except KeyboardInterrupt:
    pass
except Exception as e:
    print(f"An error occured: {e}")
finally:
    motor1_pwm.stop()
    motor2_pwm.stop()
    sensor.close()

