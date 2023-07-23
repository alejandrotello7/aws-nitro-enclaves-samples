# Use the official Python image as the base image
FROM python:3.9-slim

# Install Flask and other required dependencies
RUN pip install Flask

# Copy the app.py file into the container
COPY app.py /app.py

# Copy the run.sh and app.sh scripts into the container
COPY utils/run.sh /run.sh
COPY utils/app.sh /app.sh

# Set the working directory to / to run the Flask app
WORKDIR /

# Expose port 80 to allow communication with the Flask app
EXPOSE 80

# Add script permissions
RUN chmod +x /run.sh /app.sh

# Run the Flask app and socat when the container starts
CMD /bin/sh /run.sh && /bin/sh /app.sh