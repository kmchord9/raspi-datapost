from sensor_module.BME280 import *
from sensor_module.ADT7410 import *
from key import *
import base64
import json
import urllib.request
from time import sleep
from abc import ABCMeta
from abc import abstractmethod

class Sensor(metaclass = ABCMeta):
  def __init__(self, url, device, place):
    self.url = url
    self.device = device
    self.place = place
    self.user = USER
    self.password = PASSWORD
    self.physics_list = []
    self.postdata = []
    self.RELATE = {
          "physics":{ "温度":1, "湿度":2, "気圧":3 },
          "device": { "BME280":1, "ADT7410":2 },
          "place": { "E305":1 },
         }

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
    for physics in self.physics_list:    
      self.postdata.append({
        "value": value[physics],
        "physics": physics,
        "device": self.device,
        "place": self.place
      })
  def convertToKey(obj):
    for key, value in zip(obj.items(),self.RELATE.keys()):
      if key 



  def post(self, objs=None):
    if objs==None:
      objs = self.postdata
    print(objs)
    method = "POST"
    headers = {"Content-Type": "application/json", }

    for obj in objs:
      print(obj)
      # PythonオブジェクトをJSONに変換する
      json_data = json.dumps(obj).encode("utf-8")

      credentials = ('%s:%s' % (self.user, self.password))
      encoded_credentials = base64.b64encode(credentials.encode('ascii'))

      # httpリクエストを準備してPOST
      request = urllib.request.Request(self.url, data=json_data, method=method, headers=headers)
      request.add_header('Authorization', 'Basic %s' % encoded_credentials.decode("ascii"))

      with urllib.request.urlopen(request) as response:
          response_body = response.read().decode("utf-8")
      sleep(2)


class ADT7410(Sensor):
  def __init__(self, url, device, place):
    super().__init__(url, device, place)
    self.physics_list = ["温度"]

  def getData(self):
    rowdata = get_adt7410_data()
    key = self.physics_list[0]
    value = rowdata['temp']

    return {key: value}

class BME280(Sensor):
  def __init__(self, url, device, place):
    super().__init__(url, device, place)
    self.physics_list = ["温度", "気圧", "湿度"]

  def getData(self):
    rowdata = BME280readData()
    return {key: value for (key, value) in zip(self.physics_list, rowdata.values())}


if __name__ == '__main__':
  a = BME280("http://172.22.1.37:3001/api/logs/", "BME280","E305")
  d = a.getData()
  a.setData(d)
  a.post()


