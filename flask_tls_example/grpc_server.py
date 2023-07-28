import logging
import sys
from concurrent import futures
import pickle
import grpc
import myservice_pb2
import myservice_pb2_grpc


class GreetService(myservice_pb2_grpc.MyServiceServicer):
    def Execute(self, request, context):
        # Deserialize the function and arguments using pickle
        function_to_execute = pickle.loads(request.function)
        arguments = pickle.loads(request.arguments)

        # Execute the function with provided arguments
        result = function_to_execute(*arguments)

        # Serialize the result using pickle
        serialized_result = pickle.dumps(result)

        # Create the response and return it
        return myservice_pb2.ExecuteResponse(result=serialized_result)


def run_grpc_server():
    # Load your certificate and key files (replace 'certificate.pem' and 'key.pem' with the actual file paths)
    with open('/etc/ssl/certs/enclaves.pem', 'rb') as f:
        certificate = f.read()
    with open('/etc/ssl/private/enclaves.key', 'rb') as f:
        private_key = f.read()

    # Create TLS credentials from the certificate and key
    server_credentials = grpc.ssl_server_credentials(((private_key, certificate,),))

    # Create the gRPC server with the TLS credentials
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    myservice_pb2_grpc.add_MyServiceServicer_to_server(GreetService(), server)
    server.add_secure_port('[::]:50051', server_credentials)

    # Log a message indicating that the server is running
    logger = logging.getLogger('grpc_server')
    logger.setLevel(logging.INFO)

    # Log to console
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.INFO)
    logger.addHandler(ch)

    server.start()
    logger.info("gRPC server is running on port 50051...")

    server.wait_for_termination()

if __name__ == '__main__':
    run_grpc_server()
