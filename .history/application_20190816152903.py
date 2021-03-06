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

try:
    import ibmiotf.application
except ImportError:
    # This part is only required to run the sample from within the samples
    # directory when the module itself is not installed.
    #
    # If you have the module installed, just use "import ibmiotf"
    import os
    import inspect

    cmd_subfolder = os.path.realpath(
        os.path.abspath(os.path.join(os.path.split(inspect.getfile(inspect.currentframe()))[0], "../../src"))
    )
    if cmd_subfolder not in sys.path:
        sys.path.insert(0, cmd_subfolder)
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


def interruptHandler(signal, frame):
    client.disconnect()
    sys.exit(0)


    myConfig = { 
    "auth" {
        "key": "a-j4fntv-g1om4djfeu"
        "token": "6Rd(EgFF4aGTdf4R_5"
    }
}
    client = wiotp.sdk.application.ApplicationClient(config=myConfig)

    print("(Press Ctrl+C to disconnect)")

    client.deviceEventCallback = myEventCallback
    client.deviceStatusCallback = myStatusCallback
    client.subscriptionCallback = mySubscribeCallback

    eventsMid = client.subscribeToDeviceEvents(typeId, deviceId, event)
    statusMid = client.subscribeToDeviceStatus(typeId, deviceId)

    print("=============================================================================")
    print(tableRowTemplate % ("Timestamp", "Device", "Event"))
    print("=============================================================================")

    while True:
        time.sleep(1)


