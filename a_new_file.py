# Not exactly sure what goes in this file.

# In any case the code below was loaded and tested on my
# NodeMCU as main.py which is also in the NodeMCU directory.



import time
from machine import Pin

led = Pin(2, Pin.OUT)

on = 0
off = 1
interval = .5

led.value(on)

for i in range(10):
    time.sleep(interval)
    led.value(off)
    time.sleep(interval)
    led.value(on)
    
time.sleep(interval)
led.value(off)
