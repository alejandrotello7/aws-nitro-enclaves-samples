def check_certificate_contents(certificate_data):
    encodings = ["utf-8", "latin-1", "ascii"]  # Add additional encodings if needed
    for encoding in encodings:
        try:
            certificate_contents = certificate_data.decode(encoding)
            print("Contents of the certificate:")
            print(certificate_contents)
            break  # Stop trying encodings if successful
        except UnicodeDecodeError:
            continue
    else:
        print("Unable to decode certificate contents.")

# Example usage
with open("ca.crt", "rb") as file:
    certificate_data = file.read()

check_certificate_contents(certificate_data)