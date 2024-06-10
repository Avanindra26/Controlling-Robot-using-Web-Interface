import RPi.GPIO as GPIO
import time
from gpiozero import DistanceSensor
import json

global left_wheel_distance 
global right_wheel_distance 
global distance_to_obstacle 

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

left_wheel_rotation_count = 0
right_wheel_rotation_count = 0

sensor = DistanceSensor(echo=27, trigger=25)

def drive_forward(speed):
    GPIO.output(LED, GPIO.HIGH)
    GPIO.output(Motor1_IN1, GPIO.HIGH)
    GPIO.output(Motor1_IN2, GPIO.LOW)
    GPIO.output(Motor2_IN1, GPIO.HIGH)
    GPIO.output(Motor2_IN2, GPIO.LOW)
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

def count_left_wheel(channel):
    global left_wheel_rotation_count
    left_wheel_rotation_count += 1

def count_right_wheel(channel):
    global right_wheel_rotation_count
    right_wheel_rotation_count += 1

GPIO.add_event_detect(Left_Speed_Sensor, GPIO.RISING, callback=count_left_wheel)
GPIO.add_event_detect(Right_Speed_Sensor, GPIO.RISING, callback=count_right_wheel)

try:
    # Reset wheel rotation counts
    left_wheel_rotation_count = 0
    right_wheel_rotation_count = 0
    left_wheel_distance = 0
    right_wheel_distance = 0
    distance_to_obstacle = 0

    while True:
        # Measure distance to obstacle
        distance_to_obstacle = sensor.distance * 100  # Convert to centimeters

        # Stop motors if obstacle is too close
        if distance_to_obstacle < 10:  # Adjust the threshold as needed
            stop_motors()
            result = {
                'distance_from_obstacle': distance_to_obstacle,
                'left_wheel_distance': left_wheel_distance,
                'right_wheel_distance': right_wheel_distance
            }
            print(json.dumps(result))
            break

        drive_forward(50)  # Set your initial speed

        # Calculate distance traveled by each wheel (assuming 20 cm per rotation)
        if left_wheel_rotation_count > 20:
            left_wheel_distance += 20  # in centimeters
            left_wheel_rotation_count = 0
        if right_wheel_rotation_count > 20:
            right_wheel_distance += 20  # in centimeters
            right_wheel_rotation_count = 0

        time.sleep(0.1)  # Small delay to avoid busy-waiting

    

except KeyboardInterrupt:
    pass
except Exception as e:
    print(f"An error occured: {e}")

finally:
    motor1_pwm.stop()
    motor2_pwm.stop()
    sensor.close()
    

