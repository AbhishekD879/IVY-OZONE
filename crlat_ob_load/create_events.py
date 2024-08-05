import sys

from gevent import monkey, sleep
from gevent.pool import Pool

from ob_load_test_helpers.data import *
from ob_load_test_helpers.ob_client_wrapper import OBClientWrapper

num_of_events = int(sys.argv[1]) if sys.argv[1] else 1
is_all_market = eval(sys.argv[2]) if sys.argv[2] else False
num_of_parallel_process = int(sys.argv[3]) if sys.argv[3] else 1
perform_stream = eval(sys.argv[4]) if sys.argv[4] else False
img_stream = eval(sys.argv[5]) if sys.argv[5] else False
env = sys.argv[6] if sys.argv[6] else 'tst2'
brand = sys.argv[7] if sys.argv[7] else 'bma'
is_live = eval(sys.argv[8]) if sys.argv[8] else True
is_upcoming = eval(sys.argv[9]) if sys.argv[9] else False
add_extended_markets = eval(sys.argv[10]) if sys.argv[10] else False
event_prefix = sys.argv[11] if sys.argv[11] else 'MQA'
client = OBClientWrapper(env=env, brand=brand)

all_markets = markets if is_all_market else None

client.base.ob_config.login_to_backoffice()
monkey.patch_socket()

pool = Pool(num_of_parallel_process)
for i in range(num_of_parallel_process):
    pool.spawn(client.add_events,
               markets=all_markets,
               num_of_events=num_of_events,
               perform_stream=perform_stream,
               img_stream=img_stream,
               is_live=is_live,
               is_upcoming=is_upcoming,
               add_extended_markets=add_extended_markets,
               event_prefix=event_prefix)
    sleep(0.1)
pool.join()
pool.kill()
