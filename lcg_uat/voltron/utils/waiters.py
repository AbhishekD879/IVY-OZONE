import logging
import inspect
import re
from time import sleep
from time import time

from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from voltron.pages.shared import actions
from voltron.utils.exceptions.voltron_exception import VoltronException


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
    logger = logging.getLogger('voltron_logger')
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
            # Remove the session info and documentation URL
            err = str(err)
            # Remove the session info and documentation URL
            cleaned_error = re.sub(r'\(Session info:.*errors#no-such-element-exception', '', err, flags=re.DOTALL)

            # Remove the Stacktrace and everything after it
            cleaned_error = re.sub(r'Stacktrace:.*$', '', cleaned_error, flags=re.DOTALL)

            logger.debug(
                f'[{caller_name}] Overriding bypassed exception in WAIT with message:\n"{cleaned_error}"')
        logger.debug(f'Waiting {sleeping_time} sec for condition "{name}" to result "{expected_result}",'
                     f' current is "{bool(result)}"')

        sleeping_time += poll_interval
        waiting_time += poll_interval
        sleep(poll_interval)

    else:
        logger.debug(
            f'[{caller_name}] Failed waiting for condition "{name}" to result "{expected_result}" in {sleeping_time} sec')
    return result


def wait_for_haul(time_interval=1):
    sleep(time_interval)


def wait_for_cms_reflection(func, timeout=1, expected_result=True, refresh_count=3, ref=None, haul=0, fargs=()):
    if haul is not None:
        wait_for_haul(haul)
    if ref is None:
        raise VoltronException("Ref is needed to access driver please pass self as ref")
    for i in range(refresh_count):
        ref.device.driver.refresh()
        ref.site.wait_splash_to_hide(timeout=timeout)
        result = wait_for_result(func,
                                 fargs=fargs,
                                 expected_result=expected_result,
                                 timeout=timeout,
                                 bypass_exceptions=(AttributeError,
                                                    NoSuchElementException,
                                                    StaleElementReferenceException,
                                                    VoltronException))

        if bool(result) == expected_result:
            return result
