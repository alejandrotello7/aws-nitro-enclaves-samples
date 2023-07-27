import requests
import pickle
import base64

def add(a, b):
    return a + b

# Function name and its module
function_name = 'add'
module_name = __name__

# Arguments for the function
arguments = (10, 20)

# Serialize the function name and module using pickle
serialized_function_name = pickle.dumps(function_name)
serialized_module_name = pickle.dumps(module_name)
serialized_arguments = pickle.dumps(arguments)

# Convert the pickled binary data to Base64-encoded strings
function_name_base64 = base64.b64encode(serialized_function_name).decode()
module_name_base64 = base64.b64encode(serialized_module_name).decode()
arguments_base64 = base64.b64encode(serialized_arguments).decode()

# Send the function name, module, and arguments to the remote computer as plain text
url = "https://ec2-3-68-29-103.eu-central-1.compute.amazonaws.com:5000/api/remote_function"
payload = {
    'function_name': function_name_base64,
    'module_name': module_name_base64,
    'arguments': arguments_base64
}
response = requests.post(url, data=payload)  # Use data parameter for plain text
print(response)
# Get the result from the remote computer
result = pickle.loads(base64.b64decode(response.content))
print("Result from remote computer:", result)
