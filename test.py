from sensor_module.BME280 import *

data = readData()

print(data["temp"])