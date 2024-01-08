from helpers.common import log_allure_step, pytest_assume


class BaseSteps:
    """
    Here we should place specific functions to check something or to transform some data
    """
    def check_dummy(self):
        with log_allure_step("Dummy check"):
            pytest_assume(True, "Not expected here at all")
