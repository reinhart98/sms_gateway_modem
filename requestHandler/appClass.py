import json
import datetime
import requests
import re
import pyodbc 



class Appclass:
    def __init__(self):
        pass

    def getctime(self): 
        now = datetime.datetime.now()
        now = now.strftime("%b %d %Y %I:%M%p")
        return now
    
    def connection(self):
        conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=scq;'
                      'Database=CASQ;'
                      'UID=webcon;'
                      'PWD=cosmos*123;'
                      'Trusted_Connection=no;')
        
        return conn
    
    def insertIntodB(self,number,msg):
        conn = self.connection()
        cursor = conn.cursor()
        with conn:
            cursor.execute('''
                    INSERT INTO CASQ.dbo.CASSMSInbox (PhoneNumber, Text, CreatedDate)
                    VALUES
                    ('{}','{}','{}')
                    '''.format(number,msg,self.getctime()))
            conn.commit()
        # return "success"

    def getReturnMsg(self,order,name,SN=""):
        conn = self.connection()
        msg = ""
        if(order == "ok"):
            with conn:
                cursor = conn.cursor()
                cursor.execute('SELECT Text FROM CASQ.dbo.CASSMSReturnMessage WHERE ID=1')
                for i in cursor:
                    i = str(i).replace("'","")
                    i = i.replace('(',"")
                    i = i.replace(')',"")
                    msg = str(i)
            msg = msg.replace("xxx",name)
            msg = msg.replace("000",SN)
        else:
            with conn:
                cursor = conn.cursor()
                cursor.execute('SELECT Text FROM CASQ.dbo.CASSMSReturnMessage WHERE ID=2')
                for i in cursor:
                  
                    i = str(i).replace("'","")
                    i = i.replace('(',"")
                    i = i.replace(')',"")
                    msg = str(i)
            msg = msg.replace("xxx",name)
        
        return msg

    # START MULTIPLE SMS
    def getNumber(self,datas):
        try:
            startNum = re.escape('"+62')
            endNum   = re.escape('",,"')
            # st = "dasdasdsafs[image : image name : image]vvfd gvdfvg dfvgd"
            number = re.search('%s(.*)%s' % (startNum, endNum), datas).group(1)

            return number
        except:
            return 0

    def getMsg(self,datas):
        startMsg = re.escape('+28"')
        endMsg = re.escape("")
        
        # st = "dasdasdsafs[image : image name : image]vvfd gvdfvg dfvgd"
        msg = re.search('%s(.*)%s' % (startMsg, endMsg), datas).group(1)

        return msg

    def expressData(self,listdata):
        datas = []
        for i in listdata:
            i = i.replace("OK","")
            if(len(i) > 25):
                number = self.getNumber(i)
                if(number != 0):
                    dictdata = {
                        "number" : number,
                        "msg": self.getMsg(i)
                    }
                    datas.append(dictdata)
        return datas
    
    

    # END MULTIPLE SMS

    # START SINGLE SMS
    def checkformat1(self,listsplit):
        if(len(listsplit) >= 5):
            return True
        else:
            return False
    
    def checkformat2(self,listsplit):
        splitzeroidx = listsplit[0].split(" ")
        if(len(splitzeroidx) > 1):
            return True
        else:
            return False
    
    def checkformat3(self,listsplit):
        if "KG" in listsplit[0]:
            return True
        else:
            return False
    
    def smscheckformatdata(self, no, msg):
        newlistOK = []
        newlistNOT = []
        splitmsg = msg.split("/")
        SN = splitmsg[0].split(" ")
        con_a = self.checkformat1(splitmsg)
        con_b = self.checkformat2(splitmsg)
        con_c = self.checkformat3(splitmsg)

        if(con_a and con_b and con_c):
            print("ALL OK INSERT TO TABLE AND FLAG")
            self.insertIntodB(no,msg)
            msg = self.getReturnMsg("ok",splitmsg[1],SN[1])
            dict_ok = {
                    "number":no,
                    "msg": msg
                }
            newlistOK.append(dict_ok)
            # return "Selamat {} Kartu garansi anda dengan serial number {} sudah di daftarkan".format(splitmsg[1],SN[1])
        else:
            print("data format not match")
            self.insertIntodB(no,msg)
            dict_not = {
                    "number":no,
                    "msg": self.getReturnMsg("no",no)
                }
            newlistNOT.append(dict_not)
    
        datas = {
            "formatOK":newlistOK,
            "formatNOT":newlistNOT
        }

        return datas
    # END SINGLe SMS

    def smscheckformatdata2(self,listdata):
        newlistOK = []
        newlistNOT = []
        for i in listdata:
            splitmsg = i['msg'].split('/')
            SN = splitmsg[0].split(" ")
            con_a = self.checkformat1(splitmsg)
            con_b = self.checkformat2(splitmsg)
            con_c = self.checkformat3(splitmsg)

            if(con_a and con_b and con_c):
                print("ALL OK INSERT TO TABLE AND FLAG")
                self.insertIntodB(i['number'],i['msg'])
                # here read from db for return msg
                dict_ok = {
                    "number":i['number'],
                    "msg": self.getReturnMsg("ok",splitmsg[1],SN[1])
                }
                newlistOK.append(dict_ok)
            else:
                print("data format not match")
                self.insertIntodB(i['number'],i['msg'])
                dict_not = {
                    "number":i['number'],
                    "msg": self.getReturnMsg("no",i['number'])
                }
                newlistNOT.append(dict_not)
        
        datas = {
            "formatOK":newlistOK,
            "formatNOT":newlistNOT
        }

        return datas

    
    def procesSMS(self,datas,tipe):
        print(tipe)
        if (tipe == "multiple"):
            formatteddata = self.expressData(datas)
            return self.smscheckformatdata2(formatteddata)
        else:
            splitdatas = datas.split(",")
            # tulis table dulu baru check format
            print("str")
            return self.smscheckformatdata(splitdatas[0],splitdatas[1])
            
        
        

    
    
    

    
    
        
    
