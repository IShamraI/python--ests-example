from helpers import log_allure_step, pytest_assume
from models import User
from test_classes.base_api_test import BaseApiTest


class TestExampleApi(BaseApiTest):
    def test_user_creation(self, example_api):
        """Test User successfully created

        Requirement: SOME-REQ-EXAMPLE-API-0001

        Step: Create user
        Expected: User created
        """

        with log_allure_step("Create user"):
            response_create_user = self.steps.create_user(api=example_api)
            pytest_assume(response_create_user.status_code == 201,
                          f"Failed to create user. Status code: {response_create_user.status_code}")

    def test_new_user_accessible(self, example_api):
        """Test User successfully created and accessible

        Requirement: SOME-REQ-EXAMPLE-API-0001

        Step: Create user
        Expected: User created

        Step: Request user info
        Expected: User info available
        """

        with log_allure_step("Create user"):
            response_create_user = self.steps.create_user(api=example_api)
            pytest_assume(response_create_user.status_code == 201,
                          f"Failed to create user. Status code: {response_create_user.status_code}")

        with log_allure_step("User info accessible"):
            self.steps.check_user_exists(example_api, user_id=User(**response_create_user.json()).id)
