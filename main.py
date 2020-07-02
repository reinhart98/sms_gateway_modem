import serial
import time
import dataHandler as DH
import smsHandler as H
import json
import gc
import sys

RecMsg = H.Receive()
Dats = DH.dataHandler()
SQL = DH.SQLHandler()
counter = 0

def deleteDatas(index):
    for i in range(1,index+1):
        RecMsg.DeleteSMS(i)
        time.sleep(1)

def sendData(no, sms):
    while 1:
        datas = RecMsg.SendSMS(no,sms)
        datas = datas.replace("\r\n","")

        if "ERROR" in datas:
            print("MESSAGE FAILED SEND RESEND")
            # here keep sent with delay 1 second
            time.sleep(.5)
            continue
        else:
            print("Message Sent Successfully")
            break

    return True

def processUnreadMSG():
    sms = []
    while 1:
        datas = RecMsg.GetAllUnReadSMS()
        if "ERROR" in datas:
            time.sleep(1)
            continue
        else:
            datas.replace("OK","")
            break
    if(len(datas) > 40):
        chkcount = Dats.checknumunread(datas)
        number = Dats.getNumber(datas)
        print(number)
        if(chkcount > 1):
            splitsms = datas.split("+CMGL")
            datas = datas.replace("OK","',")
            dict_data = {
                "type":"multiple",
                "content":splitsms
            }
            res = Dats.sendtoAPI(dict_data)
        else:
            if(number != 0):
                msg = Dats.getMsg(datas,"OK")
                dict_data = {
                    "type":"single",
                    "content": number+","+msg
                }
                res = Dats.sendtoAPI(dict_data)
                # print("response:"+res)
        
        try:
            responseData = json.loads(res)
            if (len(responseData['formatNOT']) > 0):
                for i in responseData['formatNOT']:
                    sendData("+62"+i['number'],i['msg'])
            if (len(responseData['formatOK']) > 0):
                for i in responseData['formatOK']:
                    sendData("+62"+i['number'],i['msg'])

        except Exception as e:
            print(e)
            # print("sending....")
            # splitstr = res.split(",")
            # num = "+62"+splitstr[0]
            # msg = splitstr[1]
            # sendData(num,msg)

        deleteDatas(chkcount)
    else:
        print(datas)
    

def jobnull():
    listnull = SQL.getFixNullData()
    print(listnull)
    if(len(listnull) > 0):
        for i in listnull:
            splitmsg = i.split(",")
            number = splitmsg[1].replace(" ","")
            msg = splitmsg[2].replace(" ","")
            res = sendData(number,msg)
            if(res):
                SQL.flagDatas(int(splitmsg[0]))
            time.sleep(2)



# sendData("+6282187460814","Kode OTP Anda Adaah 00040")
# RecMsg.GetAllSMS()
# deleteDatas(10)
# while 1:
#     processUnreadMSG()
#     time.sleep(5)



if __name__ == "__main__":
    # RecMsg.GetAllSMS()
    # deleteDatas(10)
    while 1:
        counter += 1
        processUnreadMSG()
        if(counter % 6 == 0):
            jobnull()
        elif(counter == 60):
            gc.collect()
            os.execv(sys.executable, ['python'] + sys.argv)
        time.sleep(1)
    