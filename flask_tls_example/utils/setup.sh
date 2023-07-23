# Pull the alpine/socat:latest Docker image
docker pull alpine/socat:latest

# Replace these values with the desired port number you want to use
PORT_NUMBER=5000

# Run the Docker container with socat
docker run -d -p $PORT_NUMBER:$PORT_NUMBER --name socat_container_$(date +%Y%m%d%H%M%S) alpine/socat tcp-listen:$PORT_NUMBER,fork,keepalive,reuseaddr vsock-connect:16:80,keepalive