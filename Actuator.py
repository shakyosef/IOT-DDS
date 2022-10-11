from datetime import datetime
from sys import path as sysPath
import rticonnextdds_connector as rti
from os import path as osPath
from time import sleep
import random
filepath = osPath.dirname(osPath.realpath(__file__))
connector = rti.Connector("MyParticipantLibrary::Actuator", filepath + "/DDS.xml")
outputDDS = connector.getOutput("Actuator_Publisher::Actuator_Writer")
outputDDSTemp1 = connector.getOutput("Actuator_Publisher_temp1::Actuator_Writer_temp1")
outputDDSTemp2 = connector.getOutput("Actuator_Publisher_temp2::Actuator_Writer_temp2")
outputDDSTime = connector.getOutput("Actuator_Publisher_time::Actuator_Writer_time")
input_DDS_Temp1 = connector.getInput("Actuator_Subscriber1::Actuator_Reader1")
input_DDS_Temp2 = connector.getInput("Actuator_Subscriber2::Actuator_Reader2")
input_DDS_Temp3 = connector.getInput("Actuator_Subscriber3::Actuator_Reader3")
input_DDS_StartStop = connector.getInput("Actuator_StartStop_Subscriber::Actuator_StartStop_Reader")
status = 1                  #initialize the first status for th actuator
outputDDS.instance.setNumber("status", status)
outputDDS.write()

Start_Stop = 1      #1 if the button in on else 0
Last_status = -1        #start value for first condition
while True:
    input_DDS_Temp1.take()  #get temp from sensor 1
    input_DDS_Temp2.take()      #get temp from sensor 2
    input_DDS_Temp3.read()         #get temp from sensor 3
    input_DDS_StartStop.read()  #get state from start stop button
    numOfSamples_Temp1 = input_DDS_Temp1.samples.getLength()
    numOfSamples_Temp2 = input_DDS_Temp2.samples.getLength()
    numOfSamples_Temp3 =  input_DDS_Temp3.samples.getLength()
    numOfSamples_StartStop= input_DDS_StartStop.samples.getLength()
    if numOfSamples_StartStop>0:        #we got a message from start stop
        Start_Stop =input_DDS_StartStop.samples.getBoolean(numOfSamples_StartStop-1,"On_Off")   #get the newest message
        if Start_Stop==0: # if we receive stop command
            status = 0
            sleep(0.5)
            if status != Last_status:       #send message only if value changed
                outputDDS.instance.setNumber("status", status)
                outputDDS.write()
                Last_status = status
            print('The machine state is ', status)
            print("received stop command")
        else:
            status=1
    size=numOfSamples_Temp2
    if Start_Stop==1:
        if  numOfSamples_Temp1 > numOfSamples_Temp2:  # checking the temp
            size= numOfSamples_Temp2
        else:
            size = numOfSamples_Temp1
        if size>0:
            Current_temp1 = input_DDS_Temp1.samples.getNumber( size -1,"Actual_Temp")
            Current_temp2 = input_DDS_Temp2.samples.getNumber( size -1, "Actual_Temp")
            temperature_difference =abs(Current_temp1-Current_temp2)
            if temperature_difference >=7 : # if we get extreme temp
                status = 2
                outputDDS.instance.setNumber("status", status)
                outputDDS.write()
                Last_status = status
                print('The machine state is ', status)
                now = datetime.now()  # current date and time
                time = now.strftime("%H:%M:%S.%f")  # get the hours to miliseconds
                outputDDSTime.instance.setString("calibration's_Time", time)
                outputDDSTime.write()
                outputDDSTemp1.instance.setNumber("extreme temp 1", Current_temp1)
                outputDDSTemp1.write()
                outputDDSTemp2.instance.setNumber("extreme temp 2",  Current_temp2 )
                outputDDSTemp2.write()
                print("calibration is needed")
                if numOfSamples_Temp3>0:
                  Temperature_sensor_3 = input_DDS_Temp3.samples.getNumber( numOfSamples_Temp3 - 1, "Actual_Temp")
                  print("Difference measured:",  temperature_difference,"calibration thermometer measurement:",  Temperature_sensor_3)

            else:
                status = 1
                if status != Last_status:   #send message only if value changed
                  outputDDS.instance.setNumber("status", status)
                  outputDDS.write()
                  Last_status = status
                  print('The machine state is ',status)


    sleep(1)