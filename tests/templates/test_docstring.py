"""Test Module to setup TestCases doc"""
from helpers.common import log_allure_step, pytest_assume
from test_classes.base_test import BaseTest


class TestNewFeature1(BaseTest):

    def do_some_staff(self) -> str:
        """
        Dummy function

        Returns:
            str: empty string
        """
        return ""

    def test_feature_setup1(self):
        """Test case 1 to test our super new and cool feature

        Requirement: SOME-REQ-0001

        Step: Start solution
        Expected: solution started

        Step: Test Feature1 with setup1
        Expected: Feature1 works as expected
        """

        expected_result = "some result"

        with log_allure_step("Solution up and running"):
            pass

        with log_allure_step("Test Feature1 with setup1"):
            result = self.do_some_staff()
            pytest_assume(result == expected_result)
        return ""

    def test_feature_setup2(self):
        """Test case 2 to test our super new and cool feature

        Requirement: SOME-REQ-0001

        Step: Start solution
        Expected: solution started

        Step: Test Feature1 with setup2
        Expected: Feature1 works as expected

        Step: Test Feature1 with setup2 and additional conditions
        Expected: Feature1 works as expected
        """

        self.steps.check_dummy()
