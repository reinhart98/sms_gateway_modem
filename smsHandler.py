
import serial
import time
import sys

class Receive(object):

    def __init__(self):
        self.open()

    def open(self):
        self.ser = serial.Serial('COM17', 115200, timeout=5)
        self.SendCommand(str.encode('ATZ\r'))
        self.SendCommand(str.encode('AT+CMGF=1\r'))


    def SendCommand(self,command, getline=True):
        self.ser.write(command)
        data = ''
        if (getline):
            data=self.ReadLine()
        return data 

    def ReadLine(self):
        data = self.ser.readline()
        print(data)
        return data 



    def GetAllUnReadSMS(self):
        self.ser.flushInput()
        self.ser.flushOutput()


        command = 'AT+CMGL="REC UNREAD"\r\n'#gets incoming sms that has not been read
        print(self.SendCommand(str.encode(command),getline=True))
        data = self.ser.readall()
        # print(data.decode("utf-8"))
        datas = data.decode("utf-8")

        datas = datas.replace("\r\n","")
        
    
        return datas

    def GetAllSMS(self):
        self.ser.flushInput()
        self.ser.flushOutput()


        command = 'AT+CMGL="ALL"\r\n'#gets incoming sms that has not been read
        print(self.SendCommand(str.encode(command),getline=True))
        data = self.ser.readall()
        datas = data.decode("utf-8")
        try:
            datas = datas.replace("\r\n","")
        except:
            print("err when replace r n")
    
        print("DATAS: "+datas)

    def DeleteSMS(self,index):
        self.ser.flushInput()
        self.ser.flushOutput()


        command = 'AT+CMGD="{}"\r\n'.format(index)#gets incoming sms that has not been read
        print(self.SendCommand(str.encode(command),getline=True))
        data = self.ser.readall()
        datas = data.decode("utf-8")
        try:
            datas = datas.replace("\r\n","")
        except:
            print("err when replace r n")
    
        print("DATAS: "+datas)
    
    
    def SendSMS(self,no,msg):
        self.ser.flushInput()
        self.ser.flushOutput()
        command = '''AT+CMGS="''' + no + '''"\r'''
        print(self.SendCommand(str.encode(command),getline=True))
        time.sleep(2)
        self.ser.write(str.encode(msg + "\r"))
        time.sleep(1)
        self.ser.write(str.encode(chr(26)))
        time.sleep(2)
        data = self.ser.readall()
        datas = data.decode("utf-8")
        
        return datas


