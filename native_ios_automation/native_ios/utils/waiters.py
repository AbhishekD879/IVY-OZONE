import logging
import inspect
from time import sleep
from time import time

from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from native_ios.pages.shared import actions
from native_ios.utils.exceptions.voltron_exception import VoltronException


def wait_for_result(
        func,
        fargs=(),
        fkwargs=None,
        name=None,
        poll_interval=0.5,
        expected_result=True,
        bypass_exceptions=(NoSuchElementException, StaleElementReferenceException),
        timeout=30
):
    if name is None:
        name = func.__name__
    logger = logging.getLogger('native_ios_logger')
    if not fkwargs:
        fkwargs = {}
    sleeping_time = 0
    if not isinstance(expected_result, bool):
        raise VoltronException(message=f'Expected result should be True or False, instead it is {expected_result}')
    result = None
    waiting_time = time()
    period = poll_interval / 2
    time_to_stop = time() + (timeout if timeout > period else period)
    try:
        caller_name = inspect.stack()[1].function
    except RuntimeError:
        caller_name = inspect.stack()[1].function
    while waiting_time < time_to_stop:
        try:
            actions.perform_actions()
            result = func(*fargs, **fkwargs)
            if bool(result) is expected_result:
                logger.info(
                    f'[{caller_name}] Condition "{name}" succeed with result "{bool(result)}" in {sleeping_time} sec')
                return result

        except bypass_exceptions as err:
            logger.debug(f'[{caller_name}] Overriding bypassed "{err.__class__.__name__}" exception in WAIT with message:\n"{err}"')
        logger.debug(f'Waiting {sleeping_time} sec for condition "{name}" to result "{expected_result}",'
                     f' current is "{bool(result)}"')

        sleeping_time += poll_interval
        waiting_time += poll_interval
        sleep(poll_interval)

    else:
        logger.debug(
            f'[{caller_name}] Failed waiting for condition "{name}" to result "{expected_result}" in {sleeping_time} sec')
    return result
