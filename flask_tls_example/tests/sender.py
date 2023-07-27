import requests
import pickle
import base64

def add(a, b):
    return a + b

# Arguments for the function
arguments = (10, 20)

# Serialize the function and arguments using pickle
serialized_function = pickle.dumps(add)
serialized_arguments = pickle.dumps(arguments)

# Convert the pickled binary data to Base64-encoded strings
function_base64 = base64.b64encode(serialized_function).decode()
arguments_base64 = base64.b64encode(serialized_arguments).decode()

# Send the Base64-encoded function and arguments to the remote computer as plain text
url = "https://ec2-3-68-29-103.eu-central-1.compute.amazonaws.com:5000/api/remote_function"
payload = {
    'function': function_base64,
    'arguments': arguments_base64
}
response = requests.post(url, data=payload)  # Use data parameter for plain text
print(response)
# Get the result from the remote computer
result = pickle.loads(base64.b64decode(response.content))
print("Result from remote computer:", result)