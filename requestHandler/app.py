# api to Add_data to dynamo :
# 2. ..../api/add_data?woid=..&target=...&createdby=..&workitem=..&wocenter=..
# 3. ..../api/add_data/simple_form
# 4. .../api/add_data/jsonformat    -> POST
# jsonformat {
# "woid":...,
# "target":....,
# "createdby":....,
# "workitem":...,
# "workitemid":....,
# "shoot_cavity":...,
# "wocenter":....
# }

# api to get_data from dynamo:
# 1. .../api/get_data/woid/<woid>/<num>
# 2. .../api/get_data       
# 3. ..../api/get_data/woid?wo={woid}
# 4. ..../api/get_data/woitem?woitem={woitem}
# 5....../api/get_data/wocenter?wocenter={wocenter}
# 6. ......../api/get_dataPrint
# 7. ......./api/get_dataLog

# deleteData:
# 1. ..../api/deleteData?wo={woid}
# 2. .../api/deleteData/jsonformat                -> POST
# jsonformat = {
# "woId":...,
# "number":....
# }

# updateData:
# 1. ..../api/updateData/jsonformat                -> POST
# jsonformat for Updatedate 
# {
#  "woid":woid, 
#  "name": "smiley33",
#  "shoot_cavity":1,
#  "target":100,
#  "wocenter":"005",
#  "workitem":"knop"       
# }

# 2. ..../api/updateData/simple_form

# PublishData:
# 1. ...../api/publish <-- POST
# {
# "topic":....,
# "payload": payload
# }

from flask import Flask
from flask import jsonify
from flask import request
import json
import datetime
import appClass as p
from flask import render_template
import socket
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

appdata = p.Appclass()

hostname = socket.gethostname()    
IPAddr = socket.gethostbyname(hostname)

@app.route('/', methods=['GET'])
def hello_world():
    # return jsonify({'message' : 'CONNECTED'})
    return jsonify({"API":"connected"})

@app.route('/api/sms', methods=['POST'])
def sms():
    json = request.get_json()
    tipe = json['type']
    datas = json['content']
    print(datas)
    proc = appdata.procesSMS(datas,tipe)
    return proc

@app.route('/api/getDataInbox')
def getdataibx():
    proc = appdata.getDataAll()
    return str(proc)

@app.route('/api/getnulldata')
def getdatanull():
    proc = appdata.getFixNullData()
    return jsonify(proc)


if __name__ == "__main__":
    try:
        app.run(debug=True, host=IPAddr, port=20002)
    except:
        app.run(debug=True, host="localhost", port=20002)
        
