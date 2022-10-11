from sys import path as sysPath
import rticonnextdds_connector as rti
from os import path as osPath
from time import sleep
import random
filepath = osPath.dirname(osPath.realpath(__file__))
connector = rti.Connector("MyParticipantLibrary::Temperature2", filepath + "/DDS.xml")
outputDDS = connector.getOutput("Temp_Publisher2::Temp_Writer2")
input_DDS_Actuator = connector.getInput("Temp_Subscriber2::Temp_Reader2")
while True:
    randomNumb = random.randint(20, 30)  # temp between 20-30
    outputDDS.instance.setNumber("Sensor_Number", 2)  # the sensor ID is 2
    outputDDS.instance.setNumber("Actual_Temp", randomNumb)
    outputDDS.write()
    input_DDS_Actuator.read()
    num_stutus_actuator = input_DDS_Actuator.samples.getLength()
    if num_stutus_actuator > 0:
        stutus_actuator = input_DDS_Actuator.samples.getNumber(num_stutus_actuator - 1, "status")
        if stutus_actuator==1: #print the sensor temperature only when the actuator is working
         print("The temperature for sensor 2 is ",randomNumb)
    sleep(0.1)            #every second


