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

isPublishEvent = 1

def myCommandCallback(cmd):
    print("Command received: %s" % cmd.data)
    global isPublishEvent
    isPublishEvent = cmd.data.get("publishEvent")
    if(isPublishEvent==0):
        print("Stop push info to server")
    else:
        print("Continue push info to server")

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



# Disconnect

while True:
    while isPublishEvent==1:
        result = instance.read()
        if result.is_valid():
            print("Temperature: %-3.1f C" % result.temperature)
            print("Humidity: %-3.1f %%" % result.humidity)
        else:
            print("Error: %d" % result.error_code)
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
        time.sleep(3)

client.disconnect();
