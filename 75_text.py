#Libraries
import RPi.GPIO as GPIO
import time
import socket
import array
import struct
import os
import glob
import random
import threading
import smbus
from time import sleep

threadLock = threading.Lock()

#Set up tcp server for transmission
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM, proto=0)
port = 12346
s.settimeout(.2)
try:
    s.bind(("192.168.43.153", port))
except:
    print("Address already bound, moving on..")

#Prepare a .csv for saving data
#The line below has been disabled coz changing directory messes up with vibration sensor
# os.chdir("/home/pi/Desktop/Final Project/Data")
vers = str(random.random())[2:]
# client, addr = s.accept()
# client.send(vers)
name = "Data/project_data_"+vers+".csv"
file_content = open(name, "w")
TitleRow = "Distance1, Distance2, Temperature, X_Axis, Y_Axis, Z_Axis, Vibration_state\n"
file_content.write(TitleRow)

class mythread(threading.Thread):
    def __init__(self, sensorID, trigger, echo, data):
        threading.Thread.__init__(self)
        self.sensorID = sensorID
        self.trigger = trigger
        self.echo = echo
        self.data = data
    def run(self):
        # print (("\nStarting distance sensor %d ") %(self.sensorID))
        #Now get the lock to synchronize threads
        threadLock.acquire()
        distance(self.sensorID, self.trigger, self.echo, self.data)
        #Free lock to release next thread
        threadLock.release()

def distance(sensorID, GPIO_TRIGGER, GPIO_ECHO, data):
    # print(("Acquiring data from distance sensor %d") %(sensorID))
    #set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)

    #set Trigger after 1ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)

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
    print ("Measured Distance %s = %f cm" % (sensorID, distance))
    data.append(distance)


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
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        print("Temperature in celcius and fahr is:" ,temp_c, ", ", temp_f)
        return temp_c


#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BOARD)

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


#adxl345 stuff
# select the correct i2c bus for this revision of Raspberry Pi
revision = ([l[12:-1] for l in open('/proc/cpuinfo','r').readlines() if l[:8]=="Revision"]+['0000'])[0]
bus = smbus.SMBus(1 if int(revision, 16) >= 4 else 0)

# ADXL345 constants
EARTH_GRAVITY_MS2   = 9.80665
SCALE_MULTIPLIER    = 0.004

DATA_FORMAT         = 0x31
BW_RATE             = 0x2C
POWER_CTL           = 0x2D

BW_RATE_1600HZ      = 0x0F
BW_RATE_800HZ       = 0x0E
BW_RATE_400HZ       = 0x0D
BW_RATE_200HZ       = 0x0C
BW_RATE_100HZ       = 0x0B
BW_RATE_50HZ        = 0x0A
BW_RATE_25HZ        = 0x09

RANGE_2G            = 0x00
RANGE_4G            = 0x01
RANGE_8G            = 0x02
RANGE_16G           = 0x03

MEASURE             = 0x08
AXES_DATA           = 0x32

class ADXL345:

    address = None

    def __init__(self, address = 0x53):        
        self.address = address
        self.setBandwidthRate(BW_RATE_100HZ)
        self.setRange(RANGE_2G)
        self.enableMeasurement()

    def enableMeasurement(self):
        bus.write_byte_data(self.address, POWER_CTL, MEASURE)

    def setBandwidthRate(self, rate_flag):
        bus.write_byte_data(self.address, BW_RATE, rate_flag)

    # set the measurement range for 10-bit readings
    def setRange(self, range_flag):
        value = bus.read_byte_data(self.address, DATA_FORMAT)

        value &= ~0x0F;
        value |= range_flag;  
        value |= 0x08;

        bus.write_byte_data(self.address, DATA_FORMAT, value)
    
    # returns the current reading from the sensor for each axis
    #
    # parameter gforce:
    #    False (default): result is returned in m/s^2
    #    True           : result is returned in gs
    def getAxes(self, gforce = False):
        bytes = bus.read_i2c_block_data(self.address, AXES_DATA, 6)
        
        x = bytes[0] | (bytes[1] << 8)
        if(x & (1 << 16 - 1)):
            x = x - (1<<16)

        y = bytes[2] | (bytes[3] << 8)
        if(y & (1 << 16 - 1)):
            y = y - (1<<16)

        z = bytes[4] | (bytes[5] << 8)
        if(z & (1 << 16 - 1)):
            z = z - (1<<16)

        x = x * SCALE_MULTIPLIER 
        y = y * SCALE_MULTIPLIER
        z = z * SCALE_MULTIPLIER

        if gforce == False:
            x = x * EARTH_GRAVITY_MS2
            y = y * EARTH_GRAVITY_MS2
            z = z * EARTH_GRAVITY_MS2

        x = round(x, 4)
        y = round(y, 4)
        z = round(z, 4)

        return {"x": x, "y": y, "z": z}

 

if __name__ == '__main__':
    try:
        s.listen(5)
        while True:
            threads = []
            data = []

            #Create threads for measuring the two distances
            Thread1 = mythread(1, GPIO_TRIGGER, GPIO_ECHO, data)
            Thread2 = mythread(2, GPIO_TRIGGER2, GPIO_ECHO2, data)

            #Start the new threads
            Thread1.start()
            Thread2.start()

            #Add the threads to thread list
            threads.append(Thread1)
            threads.append(Thread2)

            #Wait for all threads to complete
            for t in threads:
                t.join()

            #Read temperature
            temp = read_temp()
            data.append(temp)

            adxl345 = ADXL345()
            axes = adxl345.getAxes(True)
            add = str(adxl345.address)
            x = float(axes['x'])
            y = float(axes['y'])
            z = float(axes['z'])
            # print (("ADXL345 on address 0x%s:") % (add))
            print (("   x = %.3f G") % ( axes['x'] ))
            print (("   y = %.3f G") % ( axes['y'] ))
            print (("   z = %.3f G") % ( axes['z'] ))
            data.append(x)
            data.append(y)
            data.append(z)

            vibration_state_read = open("Data/vibration_sensor_data.txt", 'r')
            vibration_state = int(vibration_state_read.read())
            vibration_state_read.close()
            print(("Vibration state is %d") %(vibration_state))
            data.append(vibration_state)

            dat = str(data)
            dat = dat.encode()
            try:
                client, addr = s.accept()
                client.send(dat)
                client.close()
            except:
                print("Remote client is currently unavailable!")
            row = str(data[0]) + "," + str(data[1]) + "," + str(data[2]) + "," + str(data[3]) + "," + str(data[4]) + "," + str(data[5])  + "\n"
            #print(row)
            file_content.write(row)
            time.sleep(.5)
            print("---End of reading---\n")
            

    #Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()
