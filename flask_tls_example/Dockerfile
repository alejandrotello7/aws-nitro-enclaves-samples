# Use a Python slim image as the base image
FROM python:3.9-slim-buster

# Set the working directory to /app
WORKDIR /app

# Install necessary packages (iproute2 for 'ip' command and socat)
RUN apt-get update \
    && apt-get install -y iproute2 socat \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Flask and other required dependencies
RUN pip install Flask

# Copy the app.py file into the container
COPY app.py .

# Copy Rust binary and Amazon certificate
COPY utils/att_doc_retriever_sample utils/cert.der .

# Copy the run.sh script into the container
COPY utils/run.sh .

# Expose port 80 to allow communication with the Flask app
EXPOSE 80

# Set execution permission for the scripts
RUN chmod +x run.sh

# Run the Flask app using the run.sh script
CMD ["./run.sh"]
