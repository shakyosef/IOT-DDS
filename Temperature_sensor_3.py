from sys import path as sysPath
import rticonnextdds_connector as rti
from os import path as osPath
from time import sleep
import random
filepath = osPath.dirname(osPath.realpath(__file__))

connector = rti.Connector("MyParticipantLibrary::Temperature_Pub3", filepath + "/DDS.xml")
outputDDS = connector.getOutput("Temp_Publisher3::Temp_Writer3")
while True:
    randomNumb = random.randint(24, 26)      #temp between 24-26
    outputDDS.instance.setNumber("Sensor_Number", 3)        #the sensor ID is 3
    outputDDS.instance.setNumber("Actual_Temp", randomNumb)
    outputDDS.write()
    print("The temperature for sensor 3 is ",randomNumb)
    sleep(1)      #ten times in a second