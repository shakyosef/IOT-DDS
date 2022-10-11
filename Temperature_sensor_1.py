from sys import path as sysPath
import rticonnextdds_connector as rti
from os import path as osPath
from time import sleep
import random
filepath = osPath.dirname(osPath.realpath(__file__))
connector = rti.Connector("MyParticipantLibrary::Temperature1", filepath + "/DDS.xml")
outputDDS = connector.getOutput("Temp_Publisher1::Temp_Writer1")
input_DDS_Actuator = connector.getInput("Temp_Subscriber1::Temp_Reader1")
#Temperature_sensor_1
while True:
    randomNumb = random.randint(20, 30)  # temp between 20-30
    outputDDS.instance.setNumber("Sensor_Number", 1)  # the sensor ID is 1
    outputDDS.instance.setNumber("Actual_Temp", randomNumb)
    outputDDS.write()
    input_DDS_Actuator.read()
    num_stutus_actuator=input_DDS_Actuator.samples.getLength()
    if num_stutus_actuator>0:
       stutus_actuator = input_DDS_Actuator.samples.getNumber( num_stutus_actuator -1,"status")
       if stutus_actuator==1:  #print the sensor temperature only when the actuator is working
          print("The temperature for sensor 1 is ",randomNumb)
    sleep(0.1)            #every second
