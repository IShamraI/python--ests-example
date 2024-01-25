from concurrent import futures

import grpc

import user_pb2
import user_pb2_grpc


class UserService(user_pb2_grpc.UserServiceServicer):
    def __init__(self, user_data=None):
        self.user_data = {}
        # Assume a simple user database
        if user_data is None:
            self.user_data = {
                1: {"user_id": 1, "name": "John Doe", "email": "john.doe@example.com"}
            }
        else:
            self.user_data = user_data

    def GetUserById(self, request, context):
        user_id = request.user_id
        user_info = self.user_data.get(user_id, {})
        return user_pb2.UserResponse(**user_info)

    def CreateUser(self, request, context):
        # Assume a simple user creation
        new_user_id = max(self.user_data.keys()) + 1
        self.user_data[new_user_id] = {"user_id": new_user_id, "name": request.name, "email": request.email}
        return user_pb2.UserResponse(user_id=new_user_id, name=request.name, email=request.email)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    user_service = UserService()
    user_pb2_grpc.add_UserServiceServicer_to_server(user_service, server)
    server.add_insecure_port(':5001')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
