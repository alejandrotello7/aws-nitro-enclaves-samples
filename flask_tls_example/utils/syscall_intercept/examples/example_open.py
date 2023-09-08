import os
import subprocess

# Set the LD_LIBRARY_PATH and LD_PRELOAD environment variables
os.environ['LD_LIBRARY_PATH'] = '.'
os.environ['LD_PRELOAD'] = 'example_open.so'

# Try to open the file 'CMakeLists.txt'
try:
    with open('CMakeLists.txt', 'r') as file:
        print(file.read())
except OSError as e:
    print(f"Error: {e}")
