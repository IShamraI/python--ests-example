from helpers.common import pytest_assume
from libs.api import ExampleApi
from models import User
from test_steps.base_steps import BaseSteps


class GRPCSteps(BaseSteps):
    """
    Here we should place specific functions to check something or to transform some data
    """

    # def check_user_exists(self, api: ExampleApi, user_id: int):
    #     users = [user for user in api.get_all_users() if user.id == user_id]
    #     pytest_assume(len(users) == 1, f"Received {len(users)} users instead of 1: {users}")
    #
    # def create_user(self, api: ExampleApi, name: str = "John Doe", email: str = "john.doe@example.com"):
    #     new_user_data = User(name=name, email=email)
    #     return api.post("users", data=new_user_data.json())
