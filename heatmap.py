import serial
import time
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
from matplotlib.animation import FuncAnimation
import threading

#config
BAUDRATE = 115200
PORT = '/dev/cu.usbmodem1201'  # depends on system\'COM3' for Windows
GRID_ROWS = 4
GRID_COLS = 4
VMIN = 1
VMAX_DEFAULT = 50  
ZERO_COLOR = 0     
INTERVAL = 500    

def setup_serial_connection():
    ser = serial.Serial(PORT, BAUDRATE, timeout=1)
    time.sleep(2)  #delay
    return ser

#normalization by chatgpt
def zero_fixed_normalize(value, vmin=VMIN, vmax=VMAX_DEFAULT):
    norm = Normalize(vmin, vmax)
    normalized_values = norm(value)
    normalized_values[value == 0] = ZERO_COLOR
    return normalized_values

#read data to grid
def read_serial_data(grid, ser):
    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').rstrip()
            print(line)
            try:
                values = list(map(int, line.split(',')))
                if len(values) == GRID_COLS + 1:
                    row = values[0]
                    grid[row] = values[1:GRID_COLS+1][::-1] #reverse for correct visualization
            except ValueError:
                print(f"Invalid data received: {line}")

#update heatmap
def update_heatmap(i, grid, heatmap):
    vmax_value = np.max(grid[np.nonzero(grid)]) if np.any(grid) else VMAX_DEFAULT
    heatmap.set_norm(Normalize(vmin=VMIN, vmax=vmax_value))
    heatmap.set_array(grid)
    return [heatmap]

#display
def main():
    grid = np.zeros((GRID_ROWS, GRID_COLS))
    ser = setup_serial_connection()
    fig, ax = plt.subplots()
    heatmap = ax.imshow(grid, cmap='afmhot', norm=Normalize(vmin=VMIN, vmax=VMAX_DEFAULT))
    plt.colorbar(heatmap)

    serial_thread = threading.Thread(target=read_serial_data, args=(grid, ser), daemon=True)
    serial_thread.start()

    #animation for squares
    ani = FuncAnimation(fig, update_heatmap, fargs=(grid, heatmap), interval=INTERVAL)
    
    plt.show()
    ser.close()

#run visualization
if __name__ == "__main__":
    main()
