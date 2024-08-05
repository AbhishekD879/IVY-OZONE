import sys
from ob_load_test_helpers.ob_client_wrapper import OBClientWrapper
from ob_load_test_helpers.s3_files_loader import merge_events_files
import os

env = sys.argv[1] if sys.argv[1] else 'tst2'
brand = sys.argv[2] if sys.argv[2] else 'bma'
if os.getenv('HOST', 'LOCAL') == 'AWS_SLAVE':
    file_with_events = merge_events_files()
else:
    file_with_events = sys.argv[3] if sys.argv[3] else 'target/file_with_events_ids.json'

client = OBClientWrapper(env=env, brand=brand)

client.undisplay_all_events(file_with_events)
