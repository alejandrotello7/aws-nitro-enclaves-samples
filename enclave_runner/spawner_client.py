import requests

def call_flask_api():
    url = "http://ec2-3-69-47-66.eu-central-1.compute.amazonaws.com:50052/start_enclave"  # Replace with the actual IP and port of your Flask API
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            enclave_id = data['EnclaveID']
            pcr0 = data['PCR0']
            print(f"EnclaveID: {enclave_id}")
            print(f"PCR0: {pcr0}")
        else:
            print(f"Error from server: {response.status_code} - {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"HTTP Request failed: {e}")

if __name__ == "__main__":
    call_flask_api()
