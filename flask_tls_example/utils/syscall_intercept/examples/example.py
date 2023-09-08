import subprocess
import os

# # Set the LD_LIBRARY_PATH and LD_PRELOAD environment variables
# os.environ['LD_LIBRARY_PATH'] = '.'
# os.environ['LD_PRELOAD'] = 'example.so'

# Get the current directory
current_directory = os.getcwd()

try:
    # Run the 'ls' command on the current directory
    result = subprocess.run(['ls', current_directory], stdout=subprocess.PIPE, text=True, check=True)

    # Print the output of the 'ls' command
    print(result.stdout)

except subprocess.CalledProcessError as e:
    # Handle any errors, such as the directory not existing
    print(f"Error: {e}")
