# Use an official Python runtime as a parent image
FROM python:3.8

# Install Rust
RUN curl https://sh.rustup.rs -sSf | sh -s -- -y
ENV PATH="/root/.cargo/bin:${PATH}"

# Install jq
RUN apt-get update && apt-get install -y jq

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the current directory contents into the container at /usr/src/app
COPY . .
COPY /home/ec2-user/dev/aws-nitro-enclaves-samples/att_doc_verifier /usr/src/app/att_doc_verifier/

# Copy the certificate
COPY enclaves.pem /etc/ssl/certs/enclavees.pem

# Copy the private key
COPY enclaves.key /etc/ssl/private/enclaves.key

# Set appropriate permissions for the private key
RUN chmod 600 /etc/ssl/private/enclaves.key
# Install any needed packages specified in requirements.txt
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 50051

# Define environment variable
ENV NAME World

# Run script.sh when the container launches
CMD ["./docker_verifier_script.sh"]
