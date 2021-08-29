#
# ------- Imports

import os
from time import time_ns, sleep
from machine import I2C, Pin
from pico_i2c_lcd import I2cLcd


#
# --------- Consts


i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)
I2C_ADDR = i2c.scan()
print(I2C_ADDR)
#lcd = I2cLcd(i2c, I2C_ADDR, 2, 16)

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

base_dir = '/sys/bus/w1/devices/'

# --- Veryfing probes exist/Detected

try:
    probe1 = glob.glob(base_dir + '28*' )[0] + '/temperature'
except :
    print("Defective or missing probe 1.")
    probe1 = "ErrP1"
try:
    probe2 = glob.glob(base_dir + '28*')[1] + '/temperature'
except :
    print("Defective or missing probe 2.")
    probe2 = "ErrP2"
    
fileLocations = [probe1,probe2]

# -------- Notes
#
# Brightness level  ~630 omhs
# Contrast level    ~1k omhs

#
# -------- Functions

def readFile(data):
    f = open(data, 'r')
    lines = f.read(6)
    rcPos = str.index(lines,"\n" )
    rawTemp = lines[0:rcPos]
    f.close()
    return rawTemp

def convertTemperature(file, degreeType):
    rawValue = readFile(file)
    if degreeType == "c":
        cString = (int(rawValue) / 1000.0)
        return round(cString,1)
    if degreeType == "f" :
        fString = (int(rawValue) / 1000.0) * 9.0 / 5.0 + 32.0
        return round(fString,1)
    else :
        return 0;

def getTemperature():
    print("Temp Mode")
    tList = []
    if not "Err" in fileLocations[0]:
        tList.append(convertTemperature(fileLocations[0],"c"))
        tList.append(convertTemperature(fileLocations[0],"f"))
    else:
        tList.append(fileLocations[0])
        tList.append("Err")
        
    if not "Err" in fileLocations[1]:
        tList.append(convertTemperature(fileLocations[1],"c"))
        tList.append(convertTemperature(fileLocations[1],"f"))
    else:
        tList.append(fileLocations[1])
        tList.append("Err")
    return tList
  
def lcdPrint(tList):
    print("Print LCD")
    lcd.cursor_pos = (0, 1)
    lcd.write_string(str(tList[0]) +  "C")
    lcd.cursor_pos = (0, 7)
    lcd.write_string( "/ " + str(tList[1]) + "F")
    lcd.cursor_pos = (1, 1)
    lcd.write_string(str(tList[2]) +  "C")
    lcd.cursor_pos = (1, 7)
    lcd.write_string( "/ " + str(tList[3]) + "F")
    print('1cf - ' + str(tList[0]) + '/'+ str(tList[1]))
    print('2cf - ' + str(tList[2]) + '/'+ str(tList[3]))

    
def button_callback(channel):
    print("Button pressed")
    wakeUp(300)
    
def wakeUp(timeout):
    powerOn()
    lcd.clear()
    tilSleep = 0
    while tilSleep <= timeout:
        lcdPrint(getTemperature())
        ticker()
        tilSleep += 1
        sleep(1)
    lcd.clear()
    powerOff()

def powerOn():
    GPIO.output(36, GPIO.HIGH)
    
def powerOff():
    GPIO.output(36, GPIO.LOW)
   
def ticker():
    isEven = time_ns() % 2
    if isEven == 0:
        lcd.cursor_pos = (0,15)
        lcd.write_string(" ")
        lcd.cursor_pos = (1,15)
        lcd.write_string(".")
    else :
        lcd.cursor_pos = (0,15)
        lcd.write_string("\'")
        lcd.cursor_pos = (1,15)
        lcd.write_string(" ")
        
GPIO.add_event_detect(10,GPIO.RISING,callback=button_callback)

#
# -------------- Main Code

def main():
    sleep(1)
        
if __name__ == "__main__":
    while True:
        main()