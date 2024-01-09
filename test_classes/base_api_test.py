import pytest

from libs.api import ExampleApi
from test_classes.base_test import BaseTest
from test_steps.api_steps import ApiSteps


class BaseApiTest(BaseTest):
    """
    In this class and in child classes we should place specific fixtures, required for specific test class in
    test/ folder
    """
    steps = ApiSteps()

    @pytest.fixture(scope="function")
    def example_api(self):
        return ExampleApi()
