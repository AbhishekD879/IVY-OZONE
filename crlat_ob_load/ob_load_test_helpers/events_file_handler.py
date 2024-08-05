import json
import time

FILE_WITH_EVENTS = 'target/file_with_events_ids_' + f'{time.time()}' + '.json'


def read_events_ids_from_file(file_with_events):
    with open(file_with_events, 'r') as data:
        events_to_outcomes = json.load(data)
    return events_to_outcomes


def write_events_ids_to_file(data):
    with open(FILE_WITH_EVENTS, mode='w+') as file:
        json.dump(data, file, indent=2)
