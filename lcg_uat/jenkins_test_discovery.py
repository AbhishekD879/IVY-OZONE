import json
import os
import random
import re
import sys
from io import StringIO

import pytest


discovery_dir = os.getenv('DISCOVERY_DIR', 'discovered-tests')
ignore_paths = os.getenv('IGNORE_TEST_PATHS', '')
ignore_args = ['--ignore=%s' % x for x in ignore_paths.strip(';').split(';')] if ignore_paths else []
oxygen_hostname = os.getenv('OX_HOSTNAME', 'https://sports.ladbrokes.com/')
test_path = os.getenv('TEST_PATH', './tests_sanity')
devices_to_run = os.getenv('RUN_ON', 'mobile, desktop')
mark = os.getenv('MARK', 'prod or lad_prod')
custom_marks = os.getenv('CUSTOM_MARKS', 'sanity and not slow and not lotto')

args_mobile_slow = ''
args_mobile_normal = ''
args_desktop_slow = ''
args_desktop_normal = ''


if 'mobile' in devices_to_run:
    if custom_marks:
        mobile_custom_marks_slow = f'not desktop_only and (slow and {custom_marks})'
        mobile_custom_marks_normal = f'not desktop_only and (not slow and {custom_marks})'
    else:
        mobile_custom_marks_slow = 'not desktop_only and slow'
        mobile_custom_marks_normal = 'not desktop_only and not slow'

    mobile_custom_marks_args_slow = f'({mark}) and {mobile_custom_marks_slow}'
    mobile_custom_marks_args_normal = f'({mark}) and {mobile_custom_marks_normal}'

    args_mobile_slow = ignore_args + ['--collect-only', f'-m {mobile_custom_marks_args_slow}', test_path, '-s', '-qqq']
    args_mobile_normal = ignore_args + ['--collect-only', f'-m {mobile_custom_marks_args_normal}', test_path, '-s', '-qqq']

if 'desktop' in devices_to_run:
    if custom_marks:
        desktop_custom_marks_slow = f'not mobile_only and (slow and {custom_marks})'
        desktop_custom_marks_normal = f'not mobile_only and (not slow and {custom_marks})'
    else:
        desktop_custom_marks_slow = 'not mobile_only and slow'
        desktop_custom_marks_normal = 'not mobile_only and not slow'

    desktop_custom_marks_args_slow = f'({mark}) and desktop and {desktop_custom_marks_slow}'
    desktop_custom_marks_args_normal = f'({mark}) and desktop and {desktop_custom_marks_normal}'

    args_desktop_slow = ignore_args + ['--collect-only', f'-m {desktop_custom_marks_args_slow}', test_path, '-s', '-qqq']
    args_desktop_normal = ignore_args + ['--collect-only', f'-m {desktop_custom_marks_args_normal}', test_path, '-s', '-qqq']

devices_args = {
    'mobile': {
        'arguments': {
            'slow': args_mobile_slow,
            'normal': args_mobile_normal
        },
        'number_of_tests': 0,
        'run_tests': 'True'
    },  # run_tests value has to be string because Jenkins does not support boolean values for environment variables
    'desktop': {
        'arguments': {
            'slow': args_desktop_slow,
            'normal': args_desktop_normal
        },
        'number_of_tests': 0,
        'run_tests': 'True'
    }
}


def collect_tests(device_name):
    tests = []

    for tests_type, arguments in devices_args[device_name]['arguments'].items():
        print(f'* RUNNING COLLECT TESTS FOR %s: py.test %s' % (device_name.upper(), ' '.join(arguments)))
        output = StringIO()
        backup = sys.stdout
        sys.stdout = output
        tests_ = []
        pytest.cmdline.main(arguments)

        contents = output.getvalue()

        sys.stdout = backup

        for line in contents.split('\n'):
            match = re.match(r'^([a-zA-Z0-9/\.\-_]+): [0-9]+$', line)
            if match is not None:
                tests_.append(match.group(1))

        output.close()
        random.shuffle(tests_)
        print(f'Found {len(tests_)} {tests_type} {device_name} tests for given marks: \n {json.dumps(tests_, indent=2)}')
        tests += tests_

    num_tests = len(tests)
    print(f'*** Found total {num_tests} {device_name} tests for given marks: \n {json.dumps(tests, indent=2)}')

    if num_tests <= 0:
        print('* ERROR: "0" tests were found')
        sys.exit(1)

    with open(os.path.join(discovery_dir, f'{device_name}.txt'), mode='w') as tests_file_:
        tests_file_.writelines('\n'.join(tests))
    return num_tests


if not os.path.isdir(discovery_dir):
    os.mkdir(discovery_dir)
if 'mobile' in devices_to_run:
    devices_args['mobile']['number_of_tests'] = collect_tests(device_name='mobile')
    devices_args['mobile']['run_tests'] = 'True'
else:
    with open(os.path.join(discovery_dir, 'mobile.txt'), mode='w') as tests_file:
        tests_file.writelines('')
    devices_args['mobile']['number_of_tests'] = 1
    devices_args['mobile']['run_tests'] = 'False'

if 'desktop' in devices_to_run:
    devices_args['desktop']['number_of_tests'] = collect_tests(device_name='desktop')
    devices_args['desktop']['run_tests'] = 'True'
else:
    with open(os.path.join(discovery_dir, 'desktop.txt'), mode='w') as tests_file:
        tests_file.writelines('')
    devices_args['desktop']['number_of_tests'] = 1
    devices_args['desktop']['run_tests'] = 'False'
