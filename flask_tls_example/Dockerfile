# Use the official Python slim image as the base image
FROM python:3.9-slim

# Install necessary packages (iproute2 for 'ip' command and socat)
RUN apt-get update && apt-get install -y iproute2 socat

# Install Flask and other required dependencies
RUN pip install Flask gunicorn

# Copy the app.py file into the container
COPY app.py /app.py

# Copy the run.sh and app.sh scripts into the container
COPY utils/run.sh /run.sh
COPY utils/app.sh /app.sh

# Set the working directory to / to run the Flask app
WORKDIR /

# Expose port 80 to allow communication with the Flask app
EXPOSE 80

# Set execution permission for the scripts
RUN chmod +x /run.sh /app.sh

# Run the run.sh script first and then start the Flask app using Gunicorn
CMD /run.sh && gunicorn --bind 0.0.0.0:80 app:app
