import logging
import time
from datetime import datetime
from functools import wraps
from typing import Union

import allure
import pytest


def timeit(func):
    @wraps(func)
    def timeit_wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        total_time = end_time - start_time
        # first item in the args, ie `args[0]` is `self`
        logging.debug(f'Function {func.__name__}{args} {kwargs} Took {total_time:.4f} seconds')
        return result

    return timeit_wrapper


def pytest_assume(condition: bool, text: str = None) -> None:
    """
    Args:
        condition: condition to log error
        text: text of the error to raise

    Returns:
        None
    """
    if not condition:
        logging.error(text)
    pytest.assume(condition, text)


def get_current_time(*args, **kwargs) -> str:
    return datetime.now().astimezone().replace(microsecond=0, *args, **kwargs).isoformat()


def wait_until(predicate, timeout: Union[int, float] = 10, period: Union[int, float] = 0.25, *args, **kwargs):
    """
    This function will wait 'predicate' lambda function result for 'timeout' seconds
    Args:
        predicate: lambda function (True|False)
        timeout: wait for specified seconds
        period: how long we will sleep between conditions
        *args: any additional args fot predicate func
        **kwargs: any additional kwargs fot predicate func

    Returns:
        return_value will be return if specified or lambda result(True|False)

    Examples:
        >>> filename = 'C:\test.txt'
        >>> wait_until(lambda **kwargs: os.path.isfile(kwargs.get('filename')), 10, filename=filename,
        >>>            )

    """
    result = None
    _timeout = time.time() + timeout
    while time.time() < _timeout:
        result = predicate(*args, **kwargs)
        if result:
            break
        time.sleep(period)
    else:
        logging.warning(f"Condition was not meet in {timeout} seconds.")
    return result


def log_allure_step(text):
    logging.info(f"#### {text}")
    return allure.step(text)
