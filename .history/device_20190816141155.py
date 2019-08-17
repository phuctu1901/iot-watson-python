import wiotp.sdk.device

def myCommandCallback(cmd):
    print("Command received: %s" % cmd.data)

# Configure

myConfig = wiotp.sdk.device.parseConfigFile("device.yaml")
client = wiotp.sdk.device.DeviceClient(config=myConfig, logHandlers=None)
client.commandCallback = myCommandCallback

# Connect
client.connect()

# Send Data
myData={'name' : 'foo', 'cpu' : 60, 'mem' : 50}
client.publishEvent(eventId="status", msgFormat="json", data=myData, qos=0, onPublish=None)

# Disconnect
client.disconnect()