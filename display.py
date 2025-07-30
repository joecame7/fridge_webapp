import time
import sys

import grovepi  # ensure grovepi is installed

# I2C Setup for Grove LCD
DISPLAY_RGB_ADDR = 0x30
DISPLAY_TEXT_ADDR = 0x3e

# Determine I2C Bus
if sys.platform == 'uwp':
    import winrt_smbus as smbus
    bus = smbus.SMBus(1)
else:
    import smbus
    import RPi.GPIO as GPIO
    rev = GPIO.RPI_REVISION
    if rev == 2 or rev == 3:
        bus = smbus.SMBus(1)
    else:
        bus = smbus.SMBus(0)

# Global variable to track the last update time
last_update_time = 0
debounce_duration = 5  # seconds

def setRGB(r, g, b):
    bus.write_byte_data(DISPLAY_RGB_ADDR, 0x04, 0x15)
    bus.write_byte_data(DISPLAY_RGB_ADDR, 0x06, r)
    bus.write_byte_data(DISPLAY_RGB_ADDR, 0x07, g)
    bus.write_byte_data(DISPLAY_RGB_ADDR, 0x08, b)

def textCommand(cmd):
    bus.write_byte_data(DISPLAY_TEXT_ADDR, 0x80, cmd)

def setText(text, priority=False):
    """
    Update the LCD display with the provided text.
    If priority=True, the update always happens (ignoring debounce).
    If priority=False, updates are skipped if debounce_duration seconds haven't elapsed.
    """
    global last_update_time
    current_time = time.time()

    if not priority:
        if current_time - last_update_time < debounce_duration:
            return  

    last_update_time = current_time

    textCommand(0x01)
    time.sleep(0.05)
    textCommand(0x08 | 0x04)
    textCommand(0x28) 
    time.sleep(0.05)

    count = 0
    row = 0
    for c in text:
        if c == '\n' or count == 16:
            count = 0
            row += 1
            if row == 2: 
                break
            textCommand(0xc0) 
            if c == '\n':
                continue
        count += 1
        bus.write_byte_data(DISPLAY_TEXT_ADDR, 0x40, ord(c))
        


if __name__ == '__main__':
    setText('hola', priority=True)
    setText('hola1', priority=True)
    setText('hola2', priority=True)
    setText('hola3', priority=True)
    time.sleep(5.5)
    setText('hola4')