import wiotp.sdk.device

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
            "sessionExpiry": 360000,
            "keepAlive": 6000,
        #     "caFile": "/path/to/certificateAuthorityFile.pem"
        }
    }
}
client = wiotp.sdk.device.DeviceClient(config=myConfig, logHandlers=None)
client.commandCallback = myCommandCallback

# Connect
client.connect()

# Send Data
for x in range(2, 30, 3):
    myData={'name' : 'foo', 'cpu' : x, 'mem' : 50}
    client.publishEvent(eventId="status", msgFormat="json", data=myData, qos=1, onPublish=None)

# Disconnect

client.disconnect();