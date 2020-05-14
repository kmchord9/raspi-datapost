# -*- coding: utf-8 -*-

import board
import busio
import digitalio
import adafruit_max31855


def get_max31855_data():
  spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
  cs = digitalio.DigitalInOut(board.D5)
  max31855 = adafruit_max31855.MAX31855(spi, cs)

  return max31855.temperature