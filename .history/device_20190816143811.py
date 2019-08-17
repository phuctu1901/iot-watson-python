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
    data = {"simpledev": "ok", "x": x}

    def myOnPublishCallback():
        print("Confirmed event %s received by IoTF\n" % x)

    success = client.publishEvent("test", "json", data, qos=0, onPublish=myOnPublishCallback)
    if not success:
        print("Not connected to IoTF")

    time.sleep(500)

# Disconnect

client.disconnect();