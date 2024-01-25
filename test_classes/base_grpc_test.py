from concurrent import futures
from unittest.mock import patch

import grpc
import pytest

import user_pb2_grpc
from libs.api import ExampleApi
from src.grpc.grpc_service import serve, UserService
from test_classes.base_test import BaseTest
from test_steps.grpc_steps import GRPCSteps
from user_pb2_grpc import UserServiceStub


class BaseGRPCTest(BaseTest):
    """
    In this class and in child classes we should place specific fixtures, required for specific test class in
    test/ folder
    """
    steps = GRPCSteps()
    server = None
    user_service = None

    @pytest.fixture(scope="function")
    def example_grpc_service(self):
        self.server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        self.user_service = UserService()
        user_pb2_grpc.add_UserServiceServicer_to_server(self.user_service, self.server)
        self.server.add_insecure_port('[::]:5001')
        self.server.start()
        yield self.user_service
        self.server.stop(1)

    # @pytest.fixture(scope="function")
    # def example_grpc_client(self):
    #     # Start the gRPC server in a separate thread
    #     self.server_thread = patch("grpc._server._start_unary_server").start()
    #     self.server_thread.side_effect = serve
    #     yield
    #     self.server_thread.stopall()
