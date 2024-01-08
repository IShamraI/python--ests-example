from test_steps.base_steps import BaseSteps


class BaseTest:
    """
    In this class and in child classes we should place specific fixtures, required for specific test class in
    test/ folder
    """
    steps = BaseSteps()
