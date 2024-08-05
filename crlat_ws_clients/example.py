import time

import gevent
import logging

from crlat_ws_clients.clients.vis_client_model.vis_client_app import VisApp
from crlat_ws_clients.utils.loggers import  lt_logger
logger = lt_logger


def report_passed(request_type='', name='', response_time=0, response_length=0):
    logger.warning('%s "%s" passed in %s ms content size = %s' % (request_type, name, response_time, response_length))


def report_failure(request_type='', name='', response_time=0, exception=None):
    logger.warning('%s "%s" failed in %s ms with error: %s' % (request_type, name, response_time, exception))


def vizz_tennis(ob_event_id=11486246):
    vis_app = VisApp(success_hooks=[report_passed], failure_hooks=[report_failure])

    lt_logger.setLevel(logging.DEBUG)
    vis_app.connect_vis_srv(base_url='wss://coral-vis-tennis-tst2.symphony-solutions.eu/tennis')

    vis_app.unsubscribe_tennis(ob_event_id)
    vis_app.subscribe_tennis(ob_event_id)
    gevent.sleep(2)
    vis_app.disconnect_vis_srv()


def vizz_fb(ob_event_id=13022430):
    vis_app = VisApp(success_hooks=[report_passed], failure_hooks=[report_failure])

    lt_logger.setLevel(logging.DEBUG)
    vis_app.connect_vis_srv(base_url='wss://vis-coral.symphony-solutions.eu/generic')

    vis_app.unsubscribe_fb(ob_event_id)
    vis_app.subscribe_fb(ob_event_id)
    gevent.sleep(150)
    vis_app.disconnect_vis_srv()


vizz_fb(ob_event_id=13022430)
