# *****************************************************************************
# Copyright (c) 2014, 2019 IBM Corporation and other Contributors.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Eclipse Public License v1.0
# which accompanies this distribution, and is available at
# http://www.eclipse.org/legal/epl-v10.html
# *****************************************************************************

import getopt
import signal
import time
import sys
import json
import wiotp.sdk.application

tableRowTemplate = "%-33s%-30s%s"



def myEventCallback(event):
    print("%-33s%-30s%s" % (event.timestamp.isoformat(), event.device, event.event + ": " + json.dumps(event.data)))


myConfig = { 
        "auth" :{
            "key": "a-j4fntv-g1om4djfeu",
            "token": "6Rd(EgFF4aGTdf4R_5"
            }
}

client = wiotp.sdk.application.ApplicationClient(config=myConfig)


client.connect()

def myEventCallback(event):
    str = "%s event '%s' received from device [%s]: %s"
    print(str % (event.format, event.eventId, event.device, json.dumps(event.data)))

client.deviceEventCallback = myEventCallback
client.subscribeToDeviceEvents()
# client.deviceStatusCallback = myStatusCallback
# print(client.subscribeToDeviceStatus().action)

# print("(Press Ctrl+C to disconnect)")

# # client.deviceStatusCallback = myStatusCallback
# # client.subscriptionCallback = mySubscribeCallback 
# client.disconnect()

    

# print("=============================================================================")
# print(tableRowTemplate % ("Timestamp", "Device", "Event"))
# print("=============================================================================")    

# # while True:
#     # eventsMid = client.subscribeToDeviceEvents(typeId, deviceId, event)
# client.subscribeToDeviceStatus("Cambien", "cambien001")
# time.sleep(1)


