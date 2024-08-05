import os
from random import randint

import locust
from gevent import sleep
from locust import events

from ob_load_test_helpers.ob_client_wrapper import OBClientWrapper
from ob_load_test_helpers.s3_files_loader import merge_events_files

FILE_WITH_IDS = ''


class MyTaskSet(locust.TaskSet):
    env = os.getenv('BACKEND_ENV', 'tst2')
    brand = os.getenv('BRAND', 'bma')
    events_to_update = os.getenv('TO_UPDATE', 'live')
    update_selections_limit = eval(os.getenv('UPDATE_SELECTIONS_LIMIT', 'None'))
    ob = OBClientWrapper(env=env, brand=brand)
    file_with_events = merge_events_files() if os.getenv('HOST', 'LOCAL') == 'AWS_SLAVE' else f'target/{FILE_WITH_IDS}'

    @locust.task(10)
    def update_selection(self):
        try:
            self.ob.update_random_event(self.file_with_events, events_key=self.events_to_update,
                                        limit=self.update_selections_limit)
            events.request_success.fire(
                request_type='POST',
                name='LiveUpdate',
                response_time=0,
                response_length=0
            )
        except Exception as error:
            events.request_failure.fire(
                request_type='POST',
                name='LiveUpdate',
                response_time=0,
                exception=error
            )

    @locust.task(1)
    def suspend_unsuspend(self):
        selection_id = self.ob.get_random_selection(self.file_with_events, events_key=self.events_to_update,
                                                    limit=self.update_selections_limit)
        try:
            self.ob.change_random_selection_state(selection_id=selection_id, active=False)
            events.request_success.fire(
                request_type='POST',
                name='LiveUpdate',
                response_time=0,
                response_length=0
            )
        except Exception as error:
            events.request_failure.fire(
                request_type='POST',
                name='LiveUpdate',
                response_time=0,
                exception=error
            )
        sleep(randint(5, 15))
        try:
            self.ob.change_random_selection_state(selection_id=selection_id, active=True)
            events.request_success.fire(
                request_type='POST',
                name='LiveUpdate',
                response_time=0,
                response_length=0
            )
        except Exception as error:
            events.request_failure.fire(
                request_type='POST',
                name='LiveUpdate',
                response_time=0,
                exception=error
            )


class LiveUpdates(locust.Locust):
    task_set = MyTaskSet
    min_wait = 5000
    max_wait = 15000
