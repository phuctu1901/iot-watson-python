import time
import wiotp.sdk.device
import random
import psutil

def myCommandCallback(cmd):
    print("Command received: %s" % cmd.data)

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
for x in range(0, 1000):
    temp = random.uniform(18,37)
    cpu_percent= psutil.cpu_percent();
    memory= dict(psutil.virtual_memory()._asdict())
    battery = dict(psutil.sensors_battery()._asdict())

    computer_state = {"cpu": cpu_percent, "memory": memory, "battery":battery}
    # data = {"simpledev": "ok", "x": temp}

    def myOnPublishCallback():
        print("Confirmed event %s received by IoTF\n" % x)

    # success = client.publishEvent("test", "json", data, qos=0, onPublish=myOnPublishCallback)
    # if not success:
    #     print("Not connected to IoTF")
        
    success1 = client.publishEvent("compute_status", "json", computer_state, qos=0, onPublish=myOnPublishCallback)
    if not success1:
        print("Not connected to IoTF")
    # time.sleep(15)

# Disconnect

client.disconnect();