from google.protobuf.json_format import MessageToDict

from helpers import pytest_assume, wait_until
from libs.grpc.grpc import GRPCClient
from models import User
from test_classes.base_grpc_test import BaseGRPCTest


class TestGRPCService(BaseGRPCTest):
    user = User(user_id=1, name="John Doe", email="john.doe@example.com")

    def test_get_user_by_id(self, example_grpc_service):
        grpc_client = GRPCClient(server_address='127.0.0.1:5001')
        resp_user = User(**MessageToDict(grpc_client.get_user_by_id(self.user.user_id)))
        pytest_assume(resp_user.name == self.user.name, f"Unexpected name == {resp_user.name}")
        pytest_assume(resp_user.email == self.user.email, f"Unexpected email == {resp_user.email}")

    # def test_mock_get_user_by_id(self, example_grpc_service):
    #     # Mock the gRPC client call
    #     with patch("grpc._channel._UnaryUnaryMultiCallable") as mock_call:
    #         user = User(user_id=1, name="John Doe", email="john.doe@example.com")
    #         mock_call.return_value = user_pb2.UserResponse(**user.dict())
    #         grpc_client = GRPCClient(server_address='127.0.0.1:5001')
    #         result = grpc_client.get_user_by_id(user_id=user.user_id)
    #         print(result)
    #         # print(result.return_value)
    #         print(example_grpc_service.user_data)
    #         # assert False
    #         pytest_assume(example_grpc_service.user_data[1] == 1, 1)
    # wait_until(lambda: self.subs[topic] == True)
    
    