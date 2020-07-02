import datetime
import re
import pyodbc

def connection():
    conn = pyodbc.connect('Driver={SQL Server};'
                    'Server=scq;'
                    'Database=CASQ;'
                    'UID=webcon;'
                    'PWD=cosmos*123;'
                    'Trusted_Connection=no;')
    
    return conn

def getNullData():
    conn = connection()
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


print(getNullData())
