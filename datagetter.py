import serial
import time

#baudrate and port
bauderate = 115200
port = '/dev/cu.usbmodem1201' #depending on system | Window 'COM3'
#serial connection
ser = serial.Serial(port, bauderate, timeout=1)


time.sleep(2)  #time to ensure data is send to

try:
    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').rstrip()  
            #values dont align with the position on the mouse
            print(line)
            
except KeyboardInterrupt:
    print("Programm beendet")
finally:
    ser.close() 