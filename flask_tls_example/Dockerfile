# Use the official Python slim image with Debian Buster as the base image
FROM ubuntu:latest

# Set the working directory to / to run the Flask app
WORKDIR /

# Install necessary packages (iproute2 for 'ip' command and socat)
RUN apt-get update && apt-get install -y iproute2 socat
RUN apt-get update && apt-get install -y python3 python3-pip socat

# Install Flask and other required dependencies
RUN pip3 install Flask

# Copy the app.py file into the container
COPY app.py .

# Copy Rust binary
COPY utils/att_doc_retriever_sample .

# Copy the run.sh script into the container
COPY utils/run.sh .

# Expose port 80 to allow communication with the Flask app
EXPOSE 80

# Set execution permission for the scripts
RUN chmod +x run.sh


CMD ["./run.sh"]


# Run the Flask app using the built-in development server
#CMD ["python3", "app.py"]
