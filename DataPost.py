from sensor_module.BME280 import *
from sensor_module.ADT7410 import *
from sensor_module.MAX31855 import *
from key import *
import base64
import json
import urllib.request
from time import sleep
from abc import ABCMeta
from abc import abstractmethod
import ast

class Sensor(metaclass = ABCMeta):
  def __init__(self, url, place):
    self.url = url
    self.place = place
    self.user = USER
    self.password = PASSWORD
    self.physics_list = []
    self.postdata = []
    self.RELATESS = {
          "physics":{ "温度":1, "湿度":2, "気圧":3 },
          "device": { "BME280":1, "ADT7410":2 },
          "place": { "部屋001":1,"部屋002":2 },
         }
    self.RELATE = self.get_init_data()

  @abstractmethod
  def getData(self):
    pass

  def setData(self,value):
    '''
    postdataにデータを入れる
    引数: valueは配列で与える
    ex value = {"気温":23, "湿度":60, "気圧":1000}
    　配列のキーはphysics_listと一致させること
    '''
    self.postdata=[]
    for physics in self.physics_list:    
      self.postdata.append({
        "value": value[physics],
        "physics": physics,
        "device": self.device,
        "place": self.place
      })
  def convertToKey(self,objs):
    for obj in objs:
      for key, value in obj.items():
        if key in self.RELATE:
          obj[key]=self.RELATE[key][value]
    return objs

  def post(self, objs=None, url='/api/logs/',idback=False):
    if objs==None:
      objs = self.postdata
    method = "POST"
    headers = {"Content-Type": "application/json", }

    for obj in objs:
      URL = self.url + url
      # PythonオブジェクトをJSONに変換する
      json_data = json.dumps(obj).encode("utf-8")

      credentials = ('%s:%s' % (self.user, self.password))
      encoded_credentials = base64.b64encode(credentials.encode('ascii'))

      # httpリクエストを準備してPOST
      request = urllib.request.Request(URL, data=json_data, method=method, headers=headers)
      request.add_header('Authorization', 'Basic %s' % encoded_credentials.decode("ascii"))

      with urllib.request.urlopen(request) as response:
          response_body = response.read().decode("utf-8")
          print(response_body)
          if idback==True:
            data = ast.literal_eval(response_body)
            return data['id']

  def get_init_data(self):
    URL = self.url + '/api/users/'

    credentials = ('%s:%s' % (self.user, self.password))
    encoded_credentials = base64.b64encode(credentials.encode('ascii'))
    headers = {"Content-Type": "application/json", }

    request = urllib.request.Request(URL, headers=headers)
    request.add_header('Authorization', 'Basic %s' % encoded_credentials.decode("ascii"))

    with urllib.request.urlopen(request) as response:
      response_body = response.read().decode("utf-8")
    data = ast.literal_eval(response_body)
    
    if self.place not in list(data['place'].keys()):
      id = self.post([{"place":self.place}], '/api/place/', idback=True)
      data['place']['{}'.format(self.place)]=id


      print(data)

 
    return data

class ADT7410(Sensor):
  def __init__(self, url, place):
    super().__init__(url, place)
    self.physics_list = ["温度"]
    self.device = 'ADT7410'

  def getData(self):
    rowdata = get_adt7410_data()
    key = self.physics_list[0]
    value = rowdata['temp']

    return {key: value}

class BME280(Sensor):
  def __init__(self, url, place):
    super().__init__(url, place)
    self.physics_list = ["温度", "気圧", "湿度"]
    self.device = 'BME280'

  def getData(self):
    rowdata = BME280readData()
    return {key: value for (key, value) in zip(self.physics_list, rowdata.values())}

class MAX31855(Sensor):
  def __init__(self, url, place):
    super().__init__(url, place)
    self.physics_list = ["温度"]
    self.device = 'MAX31855'

  def getData(self):
    rowdata = get_max31855_data()
    key = self.physics_list[0]
    value = rowdata

    return {key: value}

if __name__ == '__main__':
  URL = "http://172.22.1.37:3001"

  sensors = [
       BME280(URL,"部屋005"),
       ADT7410(URL,"部屋027"),
       MAX31855(URL,"部屋026"),
      ]
  while True:
    for sensor in sensors:
      data = sensor.getData()
      sensor.setData(data)
      sensor.convertToKey(sensor.postdata)
      sensor.post()

    sleep(10)

#URL = "http://172.22.1.37:3001"
#sensor = BME280(URL,"部屋005")

#data = sensor.getData()
#sensor.setData(data)
#print('部屋003' not in list(sensor.RELATE['place'].keys()))
#sensor.convertToKey(sensor.postdata)
#sensor.post()




