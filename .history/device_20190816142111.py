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
            "transport": "tcp|websockets",
            "cleanStart": True|False,
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

# Send Data
myData={'name' : 'foo', 'cpu' : 610, 'mem' : 50}
client.publishEvent(eventId="status", msgFormat="json", data=myData, qos=0, onPublish=None)

# Disconnect