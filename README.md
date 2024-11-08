# TouchVisualisation
A set of Python 3 scripts for visualizing sensor data. Modular and adaptable for different grid layouts, making it easy to customize visualizations for various sensor types.

## datagetter.py
This Python script prints the sensor data in the terminal. 
The values ​​do not match the real grid, they are mirrored vertically.
This script allows you to test whether the sensor is connected correctly and the data can be read.

## barplot.py
Each row is represented by a bar plot, and each column corresponds to a bar. A filled bar indicates "untouched" status, while an empty bar represents "touched." This grid layout visualizes the sensor's status, with data displayed in the terminal.
