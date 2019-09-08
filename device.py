import wiotp.sdk.device
import random
import psutil
import datetime
import time    
import json
import dht11
import RPi.GPIO as GPIO

#config for GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()

instance = dht11.DHT11(pin=23)

RELAIS_1_GPIO = 12
GPIO.setup(RELAIS_1_GPIO, GPIO.OUT) # GPIO Assign mode
GPIO.output(RELAIS_1_GPIO, GPIO.HIGH) # off


RELAIS_2_GPIO = 16
GPIO.setup(RELAIS_2_GPIO, GPIO.OUT) # GPIO Assign mode
GPIO.output(RELAIS_2_GPIO, GPIO.HIGH) # off



isPublishEvent = 1

def myCommandCallback(cmd):
    print("Command received: %s" % cmd.data)
    print(cmd.data)
    event = cmd.data.get("event")
    value =int (cmd.data.get("value"))

    if(event == "isPublishEvent" and value == 0):
        print("Stop push info to server")
        isPublishEvent = 0
    elif(event == "isPublishEvent" and value ==1):
        print("Continue push info to server")
        isPublishEvent = 1


    if(event == "button1"):
        if (GPIO.input(12)):
             GPIO.output(RELAIS_1_GPIO, GPIO.LOW) # off
        else:
             GPIO.output(RELAIS_1_GPIO, GPIO.HIGH) # on
    if(event == "button2"):
        if (GPIO.input(16)):
             GPIO.output(RELAIS_2_GPIO, GPIO.LOW)
        else:
             GPIO.output(RELAIS_2_GPIO, GPIO.HIGH)

	
# Configure

myConfig = { 
    "identity": {
        "orgId": "j4fntv",
        "typeId": "Cambien",
        "deviceId": "cambien001"
    },
    "auth": {
        "token": "12345678"
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



# Connect
client.connect()

# # Send Data
# for x in range(2, 30, 3):
#     myData={'name' : 'foo', 'cpu' : x, 'mem' : 50}
#     client.publishEvent(eventId="status", msgFormat="json", data=myData, qos=2, onPublish=None)


# Connect and send datapoint(s) into the cloud
# deviceCli.connect()
# for x in range(0, 1000):


def button_callback_relay1(channel):
    print("Button was pushed!")
    print(channel)
    if (GPIO.input(12)):
        GPIO.output(RELAIS_1_GPIO, GPIO.LOW) # off
    else:
        GPIO.output(RELAIS_1_GPIO, GPIO.HIGH) # on
        
def button_callback_relay2(channel):
    print("Button was pushed!")
    print(channel)
    if (GPIO.input(16)):
        GPIO.output(RELAIS_2_GPIO, GPIO.LOW) # off
    else:
        GPIO.output(RELAIS_2_GPIO, GPIO.HIGH) # on
      
GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(25, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

GPIO.add_event_detect(24,GPIO.RISING,callback=button_callback_relay1,  bouncetime=200)

GPIO.add_event_detect(25,GPIO.RISING,callback=button_callback_relay2,  bouncetime=200)
# Disconnect

while True:
    while isPublishEvent==1:
        result = instance.read()
        while result.is_valid():
            print("Temperature: %-3.1f C" % result.temperature)
            print("Humidity: %-3.1f %%" % result.humidity)
            break
        current_time = datetime.datetime.now()
        env_sensor = {"temp": result.temperature, "hum": result.humidity}
    # data = {"simpledev": "ok", "x": temp}

        def myOnPublishCallback():
            print("Confirmed event %s received by IoTF\n" % current_time)

    # success = client.publishEvent("test", "json", data, qos=0, onPublish=myOnPublishCallback)
    # if not success:
    #     print("Not connected to IoTF")
        
        success1 = client.publishEvent("env_sensor", "json", env_sensor, qos=0, onPublish=myOnPublishCallback)
        if not success1:
            print("Not connected to IoTF")
        time.sleep(30)

client.disconnect();
