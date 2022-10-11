from datetime import datetime
from sys import path as sysPath

import now as now
import rticonnextdds_connector as rti
from os import path as osPath
from time import sleep, time
import random

filepath = osPath.dirname(osPath.realpath(__file__))
connector = rti.Connector("MyParticipantLibrary::Microphone_pub", filepath + "/DDS.xml")
outputDDS = connector.getOutput("Microphone_Publisher::Microphone_Writer")
while True:
       now = datetime.now()  # current date and time
       time = now.strftime("%H:%M:%S.%f")  # get the hours to miliseconds
       outputDDS.instance.setString("Real_Time", time)
       outputDDS.write()
       print(" The time: ", time)
       sleep(0.1)            #every 0.1 second
