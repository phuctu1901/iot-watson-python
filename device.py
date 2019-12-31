import wiotp.sdk.device
import random
import psutil
import datetime
import time    
import json
import dht11
import RPi.GPIO as GPIO
import logging
import uuid
import threading

logging.basicConfig(filename='device.log',level=logging.DEBUG)

import smbus
import time

# Define some constants from the datasheet

#DEVICE     = 0x23 # Default device I2C address

#POWER_DOWN = 0x00 # No active state
#POWER_ON   = 0x01 # Power on
#RESET      = 0x07 # Reset data register value

# Start measurement at 4lx resolution. Time typically 16ms.
#CONTINUOUS_LOW_RES_MODE = 0x13
# Start measurement at 1lx resolution. Time typically 120ms
#CONTINUOUS_HIGH_RES_MODE_1 = 0x10
# Start measurement at 0.5lx resolution. Time typically 120ms
#CONTINUOUS_HIGH_RES_MODE_2 = 0x11
# Start measurement at 1lx resolution. Time typically 120ms
# Device is automatically set to Power Down after measurement.
#ONE_TIME_HIGH_RES_MODE_1 = 0x20
# Start measurement at 0.5lx resolution. Time typically 120ms
# Device is automatically set to Power Down after measurement.
#ONE_TIME_HIGH_RES_MODE_2 = 0x21
# Start measurement at 1lx resolution. Time typically 120ms
# Device is automatically set to Power Down after measurement.
#ONE_TIME_LOW_RES_MODE = 0x23

#bus = smbus.SMBus(1)  # Rev 2 Pi uses 1

#def convertToNumber(data):
  # Simple function to convert 2 bytes of data
  # into a decimal number
#  return ((data[1] + (256 * data[0])) / 1.2)

#def readLight(addr=DEVICE):
 # data = bus.read_i2c_block_data(addr,ONE_TIME_HIGH_RES_MODE_1)
 # return convertToNumber(data)

# Khai báo các biến liên quan đến chân GPIO


GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()


RELAIS_1_GPIO = 12 #Relay 1 tương ứng với chân GPIO 12
RELAIS_2_GPIO = 16 #Relay 2 tương ứng với chân GPIO 16
instance = dht11.DHT11(pin=23) #Cảm biến DHT11 tương ứng với chân GPIO 23

BUTTON_1_GPIO = 16
BUTTON_2_GPIO = 12
        
def button_callback_relay2(channel):
    print("Button was pushed!")
    print(channel)
    if (GPIO.input(BUTTON_1_GPIO)):
        GPIO.output(RELAIS_2_GPIO, GPIO.LOW) # off
    else:
        GPIO.output(RELAIS_2_GPIO, GPIO.HIGH) # on
    send_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
    print(send_time)
    button_data = {"button": 2, "value": GPIO.input(RELAIS_2_GPIO),"time": send_time}
    success1 = client.publishEvent("buttonSwitch", "json", button_data, qos=0, onPublish=myOnPublishCallback)
    if not success1:
        print("Not connected to IoTF")

def button_callback_relay1(channel):
    print("Button was pushed!")
    print(channel)
    if (GPIO.input(BUTTON_2_GPIO)):
        GPIO.output(RELAIS_1_GPIO, GPIO.LOW) # off
    else:
        GPIO.output(RELAIS_1_GPIO, GPIO.HIGH) # on
    send_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
    print(send_time)
    button_data = {"button": 1, "value": GPIO.input(RELAIS_1_GPIO),"time": send_time}
    success1 = client.publishEvent("buttonSwitch", "json", button_data, qos=0, onPublish=myOnPublishCallback)
    if not success1:
        print("Not connected to IoTF")


def getLightState():
    send_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
    light_data = {"relay1": GPIO.input(RELAIS_1_GPIO), "relay2": GPIO.input(RELAIS_2_GPIO),"time": send_time}
    success1 = client.publishEvent("lightStatus", "json", light_data, qos=0, onPublish=myOnPublishCallback)
    if not success1:
        print("Not connected to IoTF")

def configButton():
    GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(25, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    GPIO.add_event_detect(24,GPIO.RISING,callback=button_callback_relay1,  bouncetime=200)

    GPIO.add_event_detect(25,GPIO.RISING,callback=button_callback_relay2,  bouncetime=200)


def configRelay():
    GPIO.setup(RELAIS_1_GPIO, GPIO.OUT) # GPIO Assign mode
    GPIO.output(RELAIS_1_GPIO, GPIO.HIGH) # off


    GPIO.setup(RELAIS_2_GPIO, GPIO.OUT) # GPIO Assign mode
    GPIO.output(RELAIS_2_GPIO, GPIO.HIGH) # off

    

def configDevice():
    configButton()
    configRelay()
    


#config for GPIO







configDevice()

isPublishEvent = 1

def myCommandCallback(cmd):
    print("Command received: %s" % cmd.data)
    print(cmd.data)
    event = cmd.data.get("event")
#    value =int (cmd.data.get("value"))
#
#    if(event == "isPublishEvent" and value == 0):
#        print("Stop push info to server")
#        isPublishEvent = 0
#    elif(event == "isPublishEvent" and value ==1):
#        print("Continue push info to server")
#        isPublishEvent = 1


    if(event == "button1"):
        button_callback_relay1(0)
        print(cmd.data)
    if(event == "button2"):
        button_callback_relay2(0)
        
    if(event == "getLightState"):
        getLightState()
        
def myOnPublishCallback():
                current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
                print("Confirmed event %s received by IoTF\n" % current_time)
# Configure

myConfig = { 
    "identity": {
        "orgId": "ru269o",
        "typeId": "RaspberryPiGateway",
        "deviceId": "rasp_gateway_demo"
    },
    "auth": {
        "token": "wvo2RxmcVz0AZTrg!h"
    },
    "options": {
        "domain": "internetofthings.ibmcloud.com",
        # "logLevel": "error|warning|info|debug",
        "mqtt": {
            "port": 8883,
            "transport": "websockets",
            "cleanStart": True,
            "sessionExpiry": 3600,
            "keepAlive": 60,
        #     "caFile": "/path/to/certificateAuthorityFile.pem"
        }
    }
}
client = wiotp.sdk.device.DeviceClient(config=myConfig, logHandlers=None)
client.commandCallback = myCommandCallback

client.connect()

while True:
#    attach ="Coongj hoa xa hoi chu nhgia viet nam, doc lap tu do hanh phuc"
    while isPublishEvent==1:
        
        result = instance.read()
#        print(result)
#        while result.is_valid():
        while True:
            temps = psutil.sensors_temperatures()
            send_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
#            print(send_time)
#            print("Light Level : " + str(readLight()))
            id = str(uuid.uuid4())
            logging.info(id+" ---- "+send_time)
            dht11_data = {"id": id, "time": send_time,"hum": 10, "temp": temps.get('cpu-thermal')[0].current, "cpu_percent":psutil.cpu_percent(percpu=True)}
            
            success1 = client.publishEvent("psutil_data", "json", dht11_data, qos=0, onPublish=myOnPublishCallback)
            if not success1:
                print("Not connected to IoTF")
            break
        time.sleep(5)

client.disconnect();

# def main():
#    print("hello world")
# main()
