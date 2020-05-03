import base64
import json
import urllib.request
from time import sleep
from sensor_module.BME280 import *
from key import *

url = "http://192.168.1.27:3000/api/logs/"
method = "POST"
headers = {"Content-Type": "application/json", }

user = USER
password = PASSWORD

while True:
    data = readData()

    temperature = data['temp']
    humidity = data['Hum']

    # PythonオブジェクトをJSONに変換する
    obj = {"temperature": temperature, "humidity": humidity, }
    json_data = json.dumps(obj).encode("utf-8")

    credentials = ('%s:%s' % (user, password))
    encoded_credentials = base64.b64encode(credentials.encode('ascii'))

    # httpリクエストを準備してPOST
    request = urllib.request.Request(url, data=json_data, method=method, headers=headers)
    request.add_header('Authorization', 'Basic %s' % encoded_credentials.decode("ascii"))

    with urllib.request.urlopen(request) as response:
        response_body = response.read().decode("utf-8")

    sleep(2)

