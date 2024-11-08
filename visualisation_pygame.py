import pygame
import serial 
import time
import numpy as np
import threading

#config
BAUDRATE = 115200
PORT = '/dev/cu.usbmodem1201'  #depends on system|'COM3' on Windows
GRID_ROWS = 4
GRID_COLS = 4
CELL_SIZE = 100
MARGIN = 5
SCREEN_WIDTH = GRID_COLS * CELL_SIZE + (GRID_COLS + 1) * MARGIN
SCREEN_HEIGHT = GRID_ROWS * CELL_SIZE + (GRID_ROWS + 1) * MARGIN
BACKGROUND_COLOR = (0, 0, 0) 
ser = None

#serial connection
def setup_serial_connection():
    global ser
    ser = serial.Serial(PORT, BAUDRATE, timeout=1)
    time.sleep(2)  #small delay

#initialize pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Real-Time Visualization')

#fill grid with zeros
grid = np.zeros((GRID_ROWS, GRID_COLS))

#set color
def value_to_color(value):
    if value > 0:
        return (0, 255, 0)  #green
    else:
        return (255, 0, 0)  #red

#draw grid
def draw_grid():
    for row in range(GRID_ROWS):
        for col in range(GRID_COLS):
            color = value_to_color(grid[row][col])
            x = col * CELL_SIZE + (col + 1) * MARGIN
            y = row * CELL_SIZE + (row + 1) * MARGIN
            pygame.draw.rect(screen, color, (x, y, CELL_SIZE, CELL_SIZE))

#read data to grid
def read_serial_data():
    global grid
    while True:
        if ser and ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').rstrip()
            print(line)
            try:
                values = list(map(int, line.split(',')))
                if len(values) == GRID_COLS + 1:
                    row = values[0]
                    grid[row] = values[1:GRID_COLS + 1][::-1] #reverse for correct visualization
            except ValueError:
                print(f"Invalid data received: {line}")

def start_serial_thread():
    serial_thread = threading.Thread(target=read_serial_data, daemon=True)
    serial_thread.start()

#display
def main():
    global ser
    setup_serial_connection()  
    start_serial_thread() 

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill(BACKGROUND_COLOR)
        draw_grid()
        pygame.display.flip()
        pygame.time.delay(100) #update rate

    if ser:
        ser.close()
    pygame.quit()

#run visualization
if __name__ == "__main__":
    main()
