import logging
from time import sleep, time

from crlat_siteserve_client.utils.exceptions import SiteServeException


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
    logger = logging.getLogger()
    if not fkwargs:
        fkwargs = {}
    sleeping_time = 0
    if not isinstance(expected_result, bool):
        raise SiteServeException(message='Expected result should be True or False, instead it is %s' % expected_result)
    result = None
    time_to_stop = time()+timeout
    while time() < time_to_stop:
        try:
            result = func(*fargs, **fkwargs)
            if bool(result) is expected_result:
                logger.info(
                    'Condition "%s" succeed with result "%s" in %s sec' % (
                        name,
                        result,
                        sleeping_time
                    )
                )
                return result
        except bypass_exceptions as err:
            logger.debug('Overriding bypassed "%s" exception in WAIT' % err.__class__.__name__)
        logger.debug('Waiting {0} sec for condition "{1}" to result "{2}", current is "{3}"'.format(
            sleeping_time,
            name,
            expected_result,
            result is expected_result)
        )
        sleeping_time += poll_interval
        sleep(poll_interval)
    else:
        logger.debug(
            'Failed waiting for condition "%s" to result "%s" in %s sec' % (
                name,
                expected_result,
                sleeping_time
            )
        )
    return result
