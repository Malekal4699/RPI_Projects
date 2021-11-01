#main.py
from machine import Pin
from Pico-LCD-1.14-V2 import LCD_1inch14
import time

pin = Pin(25, Pin.OUT)

while True:
    pin.toggle()
    time.sleep_ms(1000)

LCD = LCD_1inch14()
