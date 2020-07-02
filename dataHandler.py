import sys
import re
import requests
import json
import pyodbc

class SQLHandler:
    def __init__(self):
        pass

    def connection(self):
        conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=scq;'
                      'Database=CASQ;'
                      'UID=webcon;'
                      'PWD=cosmos*123;'
                      'Trusted_Connection=no;')
        
        return conn

    def getNullData(self):
        conn = self.connection()
        datas = []
        newdatas = []
        with conn:
            cursor = conn.cursor()
            cursor.execute('SELECT ID,PhoneNumber,Text FROM CASQ.dbo.CASSMSSentItem WHERE SentFlag IS NULL')
            for i in cursor:
                i = str(i).replace("'","")
                i = i.replace('(',"")
                i = i.replace(')',"")
                datas.append(i)
        return datas
    
    def getFixNullData(self):
        lstdatas = self.getNullData()
        newdatas = []
        if(len(lstdatas) > 0):
            for i in lstdatas:
                splitstr = i.split(",")
                if "+62" in splitstr[1]:
                    print(i)
                    newdatas.append(i)
                
        return newdatas
    
    def flagDatas(self,id):
        conn = self.connection()
        with conn:
            cursor = conn.cursor()
            cursor.execute('UPDATE CASQ.dbo.CASSMSSentItem SET SentFlag=? WHERE ID=?','X',id)

class dataHandler:
    def __init__(self):
        pass

    def checknumunread(self,datas):
        substring = "+CMGL"
        count = datas.count(substring)
        return count

    def getNumber(self,datas):
        try:
            startNum = re.escape('"+62')
            endNum   = re.escape('",,"')
            # st = "dasdasdsafs[image : image name : image]vvfd gvdfvg dfvgd"
            number = re.search('%s(.*)%s' % (startNum, endNum), datas).group(1)

            return number
        except:
            return 0

    def getMsg(self,datas,endstring):
        startMsg = re.escape('+28"')
        endMsg = re.escape(endstring)
        
        # st = "dasdasdsafs[image : image name : image]vvfd gvdfvg dfvgd"
        msg = re.search('%s(.*)%s' % (startMsg, endMsg), datas).group(1)

        return msg
    
    def sendtoAPI(self,dict_data):
        url = "http://10.0.27.43:20002/api/sms"
        r = requests.post(url,json=dict_data)
        print(r.status_code)
        return r.text