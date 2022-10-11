from sys import path as sysPath
import rticonnextdds_connector as rti
from os import path as osPath
from time import sleep
import random
filepath = osPath.dirname(osPath.realpath(__file__))

connector = rti.Connector("MyParticipantLibrary::Start_Stop_pub", filepath + "/DDS.xml")
outputDDS = connector.getOutput("On_Off_Publisher::Start_Stop_Writer")
outputDDS.instance.set_boolean("On_Off", 1)     #Initialize the first value
print("The button state is on")
sleep(5)        #wait for the first loop iteration
while True:
    sleep(15)
    outputDDS.instance.set_boolean("On_Off", 0)     #turn off singal sends
    outputDDS.write()
    print("The button state is off")
    sleep(5)
    outputDDS.instance.set_boolean("On_Off", 1)     #turn on singal sends
    outputDDS.write()
    print("The button state is on")