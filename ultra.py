#Libraries
import RPi.GPIO as GPIO
import time
import socket
import array
import struct
import os
import glob
import random


#Set up tcp server for transmission
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM, proto=0)
port = 12346
s.bind(("192.168.43.153", port))

#Stuff for thermometer
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'
def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines

def read_temp():
    print("Temperature in celcius and fahr is..")
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        return temp_c


#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)

#set GPIO Pins
GPIO_TRIGGER = 18
GPIO_ECHO = 24
GPIO_TRIGGER2 = 12
GPIO_ECHO2 = 16

#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)
GPIO.setup(GPIO_TRIGGER2, GPIO.OUT)
GPIO.setup(GPIO_ECHO2, GPIO.IN)

GPIO.output(GPIO_TRIGGER, False)
GPIO.output(GPIO_TRIGGER2, False)
print("Waiting for sensor to settle..")
time.sleep(10)

def distance():
    print("Attempting..")
    #set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)
    GPIO.output(GPIO_TRIGGER2, True)

    #set Trigger after 1ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
    GPIO.output(GPIO_TRIGGER2, False)

    StartTime = time.time()
    StopTime = time.time()

    #save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()

    #save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()

    #time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    #multiply with the sonic speed (34300 cm/s)
    #and divide by 2, because it's to and from
    distance = (TimeElapsed * 34300) / 2
    return distance

if __name__ == '__main__':
    try:
        s.listen(5)
        while True:
            dist1 = distance()
            temp = read_temp()
            print ("Temperature is %.2f ", % temp)
            print ("Measured Distance_1 = %.1f cm" % dist1)
            data = (dist1, temp)
            client, addr = s.accept()
            data = str(data)
            data = dist.encode()
            client.send(data)
            client.close()
            time.sleep(1)
            

    #Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()
