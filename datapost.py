import base64
import json
import urllib.request
from time import sleep
from sensor_module.BME280 import *
from key import *

url = "http://172.22.1.37:3001/api/logs/"
method = "POST"
headers = {"Content-Type": "application/json", }

user = USER
password = PASSWORD

DIVICE = "BME280"
PLACE = "E305-1"

while True:
    #data = BME280readData()

    #temperature = data['temp']
    #humidity = data['Hum']
    #press = data['press']

    # PythonオブジェクトをJSONに変換する
    #obj = {"temperature": temperature, "humidity": humidity,"pressure": press, "device" : DIVICE, "place" : PLACE }
    obj = {"value": 25.63, "physics": '温度', "device": 'BME280', "place": 'E305'}
    json_data = json.dumps(obj).encode("utf-8")

    credentials = ('%s:%s' % (user, password))
    encoded_credentials = base64.b64encode(credentials.encode('ascii'))

    # httpリクエストを準備してPOST
    request = urllib.request.Request(url, data=json_data, method=method, headers=headers)
    request.add_header('Authorization', 'Basic %s' % encoded_credentials.decode("ascii"))

    with urllib.request.urlopen(request) as response:
        response_body = response.read().decode("utf-8")

    sleep(2)

