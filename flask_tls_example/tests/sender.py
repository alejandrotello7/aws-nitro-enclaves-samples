import requests
import pickle

def add(a, b):
    return a + b

# Arguments for the function
arguments = (10, 20)

# Serialize the function and arguments using pickle
serialized_function = pickle.dumps(add)
serialized_arguments = pickle.dumps(arguments)

# Send the serialized function and arguments to the remote computer
url = "https://ec2-3-68-29-103.eu-central-1.compute.amazonaws.com:5000/api/remote_function"
payload = {
    'function': serialized_function.decode(),  # Convert bytes to string for JSON
    'arguments': serialized_arguments.decode()  # Convert bytes to string for JSON
}
response = requests.post(url, json=payload)
print(response)
# Get the result from the remote computer
result = pickle.loads(response.content)
print("Result from remote computer:", result)