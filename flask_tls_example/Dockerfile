# Use the official Python slim image with Debian Buster as the base image
FROM python:3.9-slim-buster

# Set the working directory to / to run the Flask app
WORKDIR /

# Install necessary packages (iproute2 for 'ip' command and socat)
RUN apt-get update && apt-get install -y iproute2 socat

# Install Flask and other required dependencies
RUN pip install Flask gunicorn

# Copy the app.py file into the container
COPY app.py .

# Copy the run.sh scripts into the container
COPY utils/run.sh .

# Expose port 80 to allow communication with the Flask app
EXPOSE 80

# Set execution permission for the scripts
RUN chmod +x run.sh

# Execute the run.sh script before starting the Flask app
#ENTRYPOINT ["/run.sh"]

# Run the Flask app using Gunicorn
#CMD ["gunicorn", "--bind", "0.0.0.0:80", "app:app"]
CMD ["bash"]

