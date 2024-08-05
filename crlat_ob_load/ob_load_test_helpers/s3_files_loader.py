import boto3
from ob_load_test_helpers.events_file_handler import *
import jsonmerge
import os

s3 = boto3.resource('s3', region_name='eu-west-2')

client_s3 = boto3.client('s3', region_name='eu-west-2')

files = client_s3.list_objects_v2(Bucket='crlat-ob-load-file-with-events-ids')

schema = {
    'properties': {
        'live': {
            'properties': {
                'mergeStrategy': 'append'}
        }
    }
}


def merge_events_files():
    merged = {}
    if not os.path.exists('target'):
        os.makedirs('target')
    for file in files['Contents']:
        s3.meta.client.download_file('crlat-ob-load-file-with-events-ids',
                                     file['Key'], f'target/{file["Key"]}')
    for file in os.listdir('target/'):
        if os.path.isfile(f'target/{file}'):
            parsed_file = read_events_ids_from_file(f'target/{file}')
            merged = jsonmerge.merge(merged, parsed_file, schema)
    write_events_ids_to_file(merged)
    return FILE_WITH_EVENTS
