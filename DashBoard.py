import rticonnextdds_connector as rti
from os import path as osPath
from time import sleep
filepath = osPath.dirname(osPath.realpath(__file__))
connector = rti.Connector("MyParticipantLibrary::DashBoard_sub",  filepath + "/DDS.xml")
input_DDS_Microphone = connector.getInput("Dash_Sub_Microphone::Dash_Reader_Microphone")
input_DDS_Actuator = connector.getInput("Dash_Sub_Actuator::Dash_Reader_Actuator")
input_DDS_Actuator_Temp1 = connector.getInput("Dash_Sub_Actuator_temp1::Dash_Reader_Actuator_temp1")
input_DDS_Actuator_Temp2 = connector.getInput("Dash_Sub_Actuator_temp2::Dash_Reader_Actuator_temp2")
input_DDS_Actuator_time = connector.getInput("Dash_Sub_Actuator_time::Dash_Reader_Actuator_time")


while True:
    allTemp1 = []  # save the last 10 extreme measurements
    allTemp2 = []
    allActuator = []
    sleep(5)  # print every 5 sec
    input_DDS_Microphone.take()
    input_DDS_Actuator.read()
    input_DDS_Actuator_Temp1.read()
    input_DDS_Actuator_Temp2.read()
    input_DDS_Actuator_time.read()
    numOfSamplesActuator = input_DDS_Actuator.samples.getLength()
    numOfSamplesActuatorTemp1 = input_DDS_Actuator_Temp1.samples.getLength()
    numOfSamplesActuatorTemp2 = input_DDS_Actuator_Temp2.samples.getLength()
    numOfSamplesActuatorTime = input_DDS_Actuator_time.samples.getLength()
    numOfSamplesMicrophone= input_DDS_Microphone.samples.getLength()
    size_1=min(10, numOfSamplesActuatorTemp1)
    size_3=min(10, numOfSamplesActuatorTemp2)
    size_2=min(10, numOfSamplesActuator)
    for i in range(0,size_1,1):
       if  input_DDS_Actuator_Temp1.infos.isValid(i):
           x= input_DDS_Actuator_Temp1.samples.getNumber(i, "extreme temp 1")
           allTemp1.append(x)
    for i in range(0, size_3, 1):
        if input_DDS_Actuator_Temp2.infos.isValid(i):
            x = input_DDS_Actuator_Temp2.samples.getNumber(i, "extreme temp 2")
            allTemp2.append(x)

    index2=numOfSamplesActuator-1
    mona2=0
    while index2>=0 and mona2<size_2:
        allActuator.append(input_DDS_Actuator.samples.getNumber(index2, "status"))
        index2-=1
        mona2+=1

    if  numOfSamplesMicrophone>0:
        Real_Time = input_DDS_Microphone.samples.getString( numOfSamplesMicrophone-1, "Real_Time")
    else:
        Real_Time=""
    if numOfSamplesActuatorTime>0:
        calibrations_Time=  input_DDS_Actuator_time.samples.getString(numOfSamplesActuatorTime-1, "calibration's_Time")
    else:
        calibrations_Time=""
    print(" Microphone:  <", Real_Time, ">")
    print("Actuator:",  allActuator)
    print("Extreme Thermometer 1:",allTemp1)
    print("Extreme Thermometer 2:",allTemp2)
    print("The last calibration's time:",  calibrations_Time)



