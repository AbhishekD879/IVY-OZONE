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
oxygen_hostname = os.getenv('OX_HOSTNAME', 'invictus.coral.co.uk')
test_path = os.getenv('TEST_PATH', './tests_ios_fully_native_regression')
mark = os.getenv('MARK', 'tst2')
custom_marks = os.getenv('CUSTOM_MARKS', '')

args = ignore_args + ['--collect-only', '-m ios and (%s)' % custom_marks if custom_marks else '-m ios', '%s' % test_path, '-s', '-qqq']

devices_args = {
    'native_ios': {
        'arguments': args,
        'number_of_tests': 0,
        'run_tests': 'True'}
}


def collect_tests():
    print('* RUNNING COLLECT TESTS FOR: py.test %s' % (' '.join(devices_args['native_ios']['arguments'])))
    output = StringIO()
    backup = sys.stdout
    sys.stdout = output
    tests = []

    pytest.cmdline.main(devices_args['native_ios']['arguments'])

    contents = output.getvalue()

    sys.stdout = backup

    for line in contents.split('\n'):
        match = re.match(r'^([a-zA-Z0-9/\.\-_]+): [0-9]+$', line)
        if match is not None:
            tests.append(match.group(1))

    output.close()
    num_tests = len(tests)
    print(f'Found {num_tests} tests for given marks:')
    print(json.dumps(tests, indent=2))
    random.shuffle(tests)

    if num_tests <= 0:
        print('* ERROR: "%s" tests were found' % num_tests)
        print(contents)
        sys.exit(1)

    with open(os.path.join(discovery_dir, 'native_ios.txt'), mode='w') as tests_file:
        tests_file.writelines('\n'.join(tests))
    return num_tests


if not os.path.isdir(discovery_dir):
    os.mkdir(discovery_dir)
devices_args['native_ios']['number_of_tests'] = collect_tests()
