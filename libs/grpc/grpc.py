import grpc

import user_pb2
import user_pb2_grpc


class GRPCClient:
    def __init__(self, server_address):
        self.server_address = server_address

    def get_user_by_id(self, user_id):
        with grpc.insecure_channel(self.server_address) as channel:
            stub = user_pb2_grpc.UserServiceStub(channel)
            request = user_pb2.UserRequest(user_id=user_id)
            response = stub.GetUserById(request)
            return response

    def create_user(self, name, email):
        with grpc.insecure_channel(self.server_address) as channel:
            stub = user_pb2_grpc.UserServiceStub(channel)
            request = user_pb2.CreateUserRequest(name=name, email=email)
            response = stub.CreateUser(request)
            return response


# Usage example:
if __name__ == "__main__":
    # Replace 'server_address' with the actual address of your gRPC server
    grpc_client = GRPCClient(server_address='192.168.1.1:5001')

    # Example: Get user by ID
    user_id = 1
    result = grpc_client.get_user_by_id(user_id)

    print(f"User {user_id} Details:")
    print(result)

    # Example: Create a new user
    new_user_name = "Alice"
    new_user_email = "alice@example.com"
    new_user_result = grpc_client.create_user(name=new_user_name, email=new_user_email)
    print("New User Created:")
    print(new_user_result)
