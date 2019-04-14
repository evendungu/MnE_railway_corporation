#Vibrator stuff;)
import RPi.GPIO as GPIO
import os
from time import sleep

#GPIO SETUP
channel = 11
GPIO.setmode(GPIO.BOARD)
GPIO.setup(channel, GPIO.IN)
vibration_state = 0

#Set up for file to write state to
os.chdir("/home/pi/Desktop/Final Project/Data")
name = "vibration_sensor_data.txt"     
def callback(channel):
    global vibration_state
    if GPIO.input(channel):
        print("Movement Detected!")
        vibration_state = 1
        vibration_state_write = open(name, 'w')
        vibration_state_write.write(str(vibration_state))
        vibration_state_write.close()
        sleep(2)
    else:
        print("Movement Not Detected!")
    vibration_state = 0
    vibration_state_write = open(name, 'w')
    vibration_state_write.write(str(vibration_state))
    vibration_state_write.close()
     
GPIO.add_event_detect(channel, GPIO.BOTH, bouncetime=300)  # let us know when the pin goes HIGH or LOW
GPIO.add_event_callback(channel, callback)  # assign function to GPIO PIN, Run function on change

while True:
    sleep(0.1)
  
