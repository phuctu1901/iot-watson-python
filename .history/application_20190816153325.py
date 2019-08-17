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
import ibmiotf.application

tableRowTemplate = "%-33s%-30s%s"


def mySubscribeCallback(mid, qos):
    if mid == statusMid:
        print("<< Subscription established for status messages at qos %s >> " % qos[0])
    elif mid == eventsMid:
        print("<< Subscription established for event messages at qos %s >> " % qos[0])


def myEventCallback(event):
    print("%-33s%-30s%s" % (event.timestamp.isoformat(), event.device, event.event + ": " + json.dumps(event.data)))


def myStatusCallback(status):
    if status.action == "Disconnect":
        summaryText = "%s %s (%s)" % (status.action, status.clientAddr, status.reason)
    else:
        summaryText = "%s %s" % (status.action, status.clientAddr)
    print(tableRowTemplate % (status.time.isoformat(), status.device, summaryText))



myConfig = { 
        "auth" :{
            "key": "a-j4fntv-g1om4djfeu",
            "token": "6Rd(EgFF4aGTdf4R_5"
            }
}

client = wiotp.sdk.application.ApplicationClient(config=myConfig)

print("(Press Ctrl+C to disconnect)")

client.deviceEventCallback = myEventCallback
client.deviceStatusCallback = myStatusCallback
client.subscriptionCallback = mySubscribeCallback 

    

print("=============================================================================")
print(tableRowTemplate % ("Timestamp", "Device", "Event"))
print("=============================================================================")    

while True:
    eventsMid = client.subscribeToDeviceEvents(typeId, deviceId, event)
    statusMid = client.subscribeToDeviceStatus(typeId, deviceId)
    time.sleep(1)


