from gevent import monkey
monkey.patch_all()

from datetime import datetime
import logging
import os
import random

import gevent
import locust
from locust import runners
import requests
from locust.main import parse_options

from crlat_ws_clients.clients.vis_client_model.vis_client_app import VisApp
from crlat_ws_clients.utils.loggers import lt_logger, get_root_logger

import ujson as json

backoffice_hostname = os.getenv('BACKOFFICE_HOSTNAME', 'ss-aka-ori.coral.co.uk')


class_ids_packed_football = [133, 132, 131, 130, 149, 148, 147, 146, 145, 144, 143, 142, 141, 140,
                             119, 118, 117, 116, 115, 114, 113, 112, 111, 110, 129, 128, 127, 126,
                             125, 124, 123, 122, 121, 120, 179, 178, 177, 176, 175, 174, 173, 172,
                             171, 170, 183, 181, 180, 28039, 159, 158, 157, 156, 155, 154, 153, 152,
                             151, 150, 28046, 169, 168, 167, 166, 165, 164, 163, 162, 161, 160, 26511,
                             26517, 26518, 26520, 26521, 26646, 26406, 26648, 26618, 26617, 26622,
                             26506, 109, 108, 107, 106, 105, 104, 103, 466, 102, 101, 100]


def get_events(version='2.31', class_ids=None):
    class_ids = class_ids if class_ids else []

    headers = {'Accept': 'application/json'}

    str_class_id = ','.join(str(e) for e in class_ids)

    now_ts = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')

    url = f'https://{backoffice_hostname}/openbet-ssviewer/Drilldown/{version}/EventToOutcomeForClass/{str_class_id}'

    params = (
        ('simpleFilter', 'event.siteChannels:contains:M'),
        ('simpleFilter', 'market.siteChannels:contains:M'),
        ('simpleFilter', 'outcome.siteChannels:contains:M'),
        ('simpleFilter', 'event.drilldownTagNames:intersects:EVFLAG_BL'),
        ('simpleFilter', 'market.isMarketBetInRun'),
        ('simpleFilter', 'event.isStarted'),
        ('simpleFilter', 'event.isLiveNowEvent'),
        ('simpleFilter', f'event.suspendAtTime:greaterThan:{now_ts}Z'),
        ('limitTo', 'market.displayOrder:isLowest'),
        ('existsFilter', 'market:simpleFilter:outcome.outcomeMeaningMajorCode:in:HH,MR'),
        ('existsFilter', 'event:simpleFilter:market.isMarketBetInRun'),
        ('existsFilter', 'event:simpleFilter:market.isResulted:isFalse'),
        ('existsFilter', 'event:simpleFilter:market.isDisplayed'),
        ('translationLang', 'en'),
    )

    r = requests.get(
        url=url,
        params=params,
        headers=headers,
    )
    if r.status_code in range(200, 209):
        req_ss = json.loads(r.text)
        event_ids_data = [events for events in req_ss['SSResponse']['children'][:]]
        event_id_list = []
        for item in event_ids_data:
            single_event_data = item.get('event')
            if isinstance(single_event_data, dict):
                event_id_list.append(single_event_data.get('id'))
        print(event_id_list)
        return event_id_list

    else:
        raise Exception(f'"{r.status_code}" Error: {r.reason} for url: {url}, data:\n{r.text}')


class VisTaskSet(locust.TaskSet):

    parser, options, args = parse_options()
    host = options.host if options.host else 'wss://vis-stg2-coral.symphony-solutions.eu/generic'

    event_ids = get_events(version='2.31', class_ids=class_ids_packed_football)

    @locust.task(1)
    def subscribe_event(self):
        ob_event_id = random.choice(self.event_ids)
        get_root_logger().setLevel(logging.WARNING)

        vis_app = VisApp(
            success_hooks=[locust.events.request_success.fire],
            failure_hooks=[locust.events.request_failure.fire]
        )

        lt_logger.setLevel(logging.DEBUG)
        try:
            vis_app.connect_vis_srv(base_url=self.host)
            vis_app.unsubscribe_fb(ob_event_id)

            vis_app.subscribe_fb(ob_event_id)

            gevent.sleep(random.choice(range(30, 150)))
        except Exception as err:
            locust.events.request_failure.fire(
                request_type='Vis_FB',
                name='General Error',
                response_time=0,
                exception=err
            )
        finally:
            vis_app.disconnect_vis_srv()
            del vis_app

    def on_stop(self):
        runners.locust_runner.quit()


class VIS_MS(locust.Locust):
    task_set = VisTaskSet
    min_wait = 500
    max_wait = 1500


if __name__ == '__main__':
    get_events(class_ids=class_ids_packed_football)
