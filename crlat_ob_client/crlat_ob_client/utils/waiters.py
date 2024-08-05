import inspect
import logging
from time import sleep
from time import time

from crlat_ob_client import LOGGER_NAME
from crlat_ob_client.utils.exceptions import OBException


def wait_for_result(
        func,
        fargs=(),
        fkwargs=None,
        name=None,
        poll_interval=0.5,
        expected_result=True,
        bypass_exceptions=(ValueError, KeyError),
        timeout=30
    ):
    if name is None:
        name = func.__name__
    logger = logging.getLogger(LOGGER_NAME)
    if not fkwargs:
        fkwargs = {}
    sleeping_time = 0
    if not isinstance(expected_result, bool):
        raise OBException(message='Expected result should be True or False, instead it is %s' % expected_result)
    result = None
    time_to_stop = time()+timeout
    try:
        caller_name = inspect.stack()[1].function
    except RuntimeError:
        caller_name = inspect.stack()[1].function

    logger.debug(caller_name)
    while time() < time_to_stop:
        try:
            result = func(*fargs, **fkwargs)
            if bool(result) is expected_result:
                logger.info(f'[{caller_name}] Condition "{name}" succeed with result "{bool(result)}" in {sleeping_time} sec')
                return result
        except bypass_exceptions as err:
            logger.debug(f'[{caller_name}] Overriding bypassed "{err.__class__.__name__}" exception in WAIT with message:\n"{err}"')
        logger.debug(f'Waiting {sleeping_time} sec for condition "{name}" to result "{expected_result}",'
                     f' current is "{bool(result)}"')
        sleeping_time += poll_interval
        sleep(poll_interval)
    else:
        logger.debug(f'[{caller_name}] Failed waiting for condition "{name}" to result "{expected_result}" in {sleeping_time} sec')
    return result
