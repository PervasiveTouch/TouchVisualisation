import serial
import time
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import threading

#config
BAUDRATE = 115200
PORT = '/dev/cu.usbmodem1201'  #depends on system|'COM3' for Windows
GRID_ROWS = 4
GRID_COLS = 4
MAX_VALUE = 50
INTERVAL = 500  

def setup_serial_connection():
    ser = serial.Serial(PORT, BAUDRATE, timeout=1)
    time.sleep(2)  #delay
    return ser

#read data to grid
def read_serial_data(grid, ser):
    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').rstrip()
            print(line)  #print data in terminal
            try:
                values = list(map(int, line.split(',')))
                if len(values) == GRID_COLS + 1:
                    row = values[0]
                    grid[row] = values[1:GRID_COLS + 1][::-1] #reverse for correct visualization
            except ValueError:
                print(f"Invalid data received: {line}")

#update bars 
def update_bars(i, grid, bars):
    for row in range(GRID_ROWS):
        for col, bar in enumerate(bars[row]):
            bar.set_height(grid[row][col]) 
    return [bar for sublist in bars for bar in sublist]

#display
def main():
    grid = np.zeros((GRID_ROWS, GRID_COLS))
    ser = setup_serial_connection()
    fig, axs = plt.subplots(GRID_ROWS, 1, figsize=(6, 10)) 
    bars = []

    #create multiple barplots
    for i in range(GRID_ROWS):
        axs[i].set_ylim(0, MAX_VALUE) 
        axs[i].set_title(f"Row {i}")
        bars.append(axs[i].bar(range(GRID_COLS), grid[i], color='red'))

    serial_thread = threading.Thread(target=read_serial_data, args=(grid, ser), daemon=True)
    serial_thread.start()

    #animate bars
    ani = FuncAnimation(fig, update_bars, fargs=(grid, bars), interval=INTERVAL)

    #plot
    plt.tight_layout() 
    plt.show()
    ser.close()

#run visualization
if __name__ == "__main__":
    main()
