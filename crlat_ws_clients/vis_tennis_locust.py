from gevent import monkey
monkey.patch_all()

import logging
import os
import random

import gevent
from locust import runners, events, task, Locust, TaskSet
from locust.main import parse_options
import ujson as json

from crlat_ws_clients.clients.vis_client_model.vis_client_app import VisApp
from crlat_ws_clients.utils.loggers import lt_logger, get_root_logger


EVENT_IDS = json.loads(os.getenv('EVENT_IDS', '[13438893]'))


class VisTaskSet(TaskSet):

    parser, options, args = parse_options()
    host = options.host if options.host else 'wss://coral-vis-tennis.symphony-solutions.eu/tennis'

    @task
    def subscribe_event(self):
        ob_event_id = random.choice(EVENT_IDS)
        get_root_logger().setLevel(logging.WARNING)
        lt_logger.setLevel(logging.DEBUG)
        vis_app = VisApp(
            success_hooks=[events.request_success.fire],
            failure_hooks=[events.request_failure.fire]
        )
        try:
            vis_app.connect_vis_srv(base_url=self.host)
            vis_app.unsubscribe_tennis(ob_event_id)

            vis_app.subscribe_tennis(ob_event_id)

            gevent.sleep(random.choice(range(30, 150)))
            vis_app.disconnect_vis_srv()
        except Exception as err:
            events.request_failure.fire(
                request_type='Vis_Tennis',
                name='General Error',
                response_time=0,
                exception=err
            )
        finally:
            del vis_app

    def on_stop(self):
        runners.locust_runner.quit()


class VIS_MS(Locust):
    task_set = VisTaskSet
    min_wait = 500
    max_wait = 1500


if __name__ == '__main__':
    vts = VisTaskSet(VIS_MS())
    vts.subscribe_event()
