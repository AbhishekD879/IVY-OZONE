import json
import os
import requests
from requests.auth import HTTPBasicAuth
from io import StringIO

import re
import random

import pytest
import sys
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

headers = {'Accept': 'application/vnd.go.cd.v4+json', 'Content-Type': 'application/json'}
ignore_paths = os.getenv('IGNORE_TEST_PATHS', '')
ignore_args = ['--ignore=%s' % x for x in ignore_paths.strip(';').split(';')] if ignore_paths else []
user = os.getenv('GO_USER', 'gobot')
passwd = os.getenv('GO_PASSWD', 'Secret#1')
auth = HTTPBasicAuth(username=user, password=passwd)
pipe_line_name = os.getenv('GO_PIPELINE_NAME', 'OX_UI_CRLATVPC_mobile_desktop')
num_instances = os.getenv('GO_PIPELINE_COUNTER', '0')
# environment = os.getenv('ENV', '')
oxygen_hostname = os.getenv('OX_HOSTNAME', 'invictus.coral.co.uk')
test_path = os.getenv('TEST_PATH', './tests')
devices_to_run = os.getenv('RUN_ON', 'mobile and desktop')
mark = os.getenv('MARK', 'tst2')
custom_marks = os.getenv('CUSTOM_MARKS', '')
custom_mobile_marks = 'not desktop_only and (%s)' % custom_marks if custom_marks else 'not desktop_only'
mobile_custom_marks_args = '(%s) and %s' % (mark, custom_mobile_marks)
goserver_address = os.getenv('GO_SERVER_ADDRESS', 'https://goserver.crlat.net:8154')


args_default = ignore_args + ['--collect-only', '-m %s' % mobile_custom_marks_args, '%s' % test_path, '-s', '-qqq', ]
args_desktop = ''
if 'desktop' in devices_to_run:
    desktop_custom_marks_arg = '(%s) and desktop and (%s)' % (mark, custom_marks) if custom_marks else '(%s) and desktop' % mark
    args_desktop = ignore_args + ['--collect-only', '-m %s' % desktop_custom_marks_arg, '%s' % test_path, '-s', '-qqq', ]

devices_args = {
    'mobile': {
        'arguments': args_default,
        'number_of_tests': 0,
        'run_tests': 'True'},  # run_tests value has to be string because GOCD does not support boolean values for environment variables
    'desktop': {
        'arguments': args_desktop,
        'number_of_tests': 0,
        'run_tests': 'True'
    }
}


def collect_tests(device_name):
    print('* RUNNING COLLECT TESTS FOR %s: py.test %s' % (device_name.upper(), ' '.join(devices_args[device_name]['arguments'])))
    output = StringIO()
    backup = sys.stdout
    sys.stdout = output
    tests = []

    pytest.cmdline.main(devices_args[device_name]['arguments'])

    contents = output.getvalue()

    sys.stdout = backup

    for line in contents.split('\n'):
        match = re.match(r'^([a-zA-Z0-9/\.\-_]+): [0-9]+$', line)
        if match is not None:
            tests.append(match.group(1))

    output.close()
    num_tests = len(tests)
    print('Found %s tests for given marks' % num_tests)
    print(json.dumps(tests, indent=2))
    random.shuffle(tests)

    if num_tests <= 0:
        print('* ERROR: "%s" tests were found' % num_tests)
        print(contents)
        sys.exit(1)

    with open('discovered-tests-%s.txt' % device_name, mode='w') as tests_file:
        tests_file.writelines('\n'.join(tests))
    return num_tests


def get_pipeline():
    resp = requests.get(
        '%s/go/api/admin/pipelines/%s' % (goserver_address, pipe_line_name),
        auth=auth,
        headers=headers,
        verify=False
    )
    if resp.status_code != 200:
        raise Exception('Something goes wrong with request. Status code: %s: %s' % (resp.status_code, resp.reason))
    if resp.content == '':
        raise Exception('Empty response')
    job = json.loads(resp.content)
    # print('existing job "%s"' % json.dumps(job, indent=2))
    headers.update({'If-Match': resp.headers['ETag']})
    return job


def update_job_stages(job, **kwargs):
    stages_to_update = devices_args.keys()
    updated = job
    # print(updated)
    for stage_to_update in stages_to_update:
        for stage_i in range(0, len(updated['stages'])):
            if updated['stages'][stage_i]['name'] == '%s_dynamic_jobs_stage' % stage_to_update:
                for job_i in range(0, len(updated['stages'][stage_i]['jobs'])):
                    if updated['stages'][stage_i]['jobs'][job_i]['name'] == 'dynamic_job':
                        updated['stages'][stage_i]['jobs'][job_i]['run_instance_count'] = devices_args[stage_to_update]['number_of_tests']
                        for variable_i in updated['stages'][stage_i]['jobs'][job_i]['environment_variables']:
                            if variable_i['name'] == 'RUN_TESTS':
                                variable_i['value'] = devices_args[stage_to_update]['run_tests']

    print('* UPDATING PIPELINE "%s": content: "%s"' % (pipe_line_name, json.dumps(updated, indent=2)))
    r = requests.put('%s/go/api/admin/pipelines/%s' % (goserver_address, pipe_line_name),
                     auth=auth,
                     headers=headers,
                     data=json.dumps(updated),
                     verify=False
                     )

    if r.status_code != 200:
        raise Exception('Something goes wrong with request. Status code: %s: %s' % (r.status_code, r.reason))
    if r.content == '':
        raise Exception('Empty response')
    print('* UPDATED PIPELINE "%s" content: \n"%s"' % (pipe_line_name, r.content))


if 'mobile' in devices_to_run:
    devices_args['mobile']['number_of_tests'] = collect_tests(device_name='mobile')
else:
    with open('discovered-tests-mobile.txt', mode='w') as tests_file:
        tests_file.writelines('')
    devices_args['mobile']['number_of_tests'] = 1  # has to be 1 as GO CD do not support 0 as number of instances for triggered job
    devices_args['mobile']['run_tests'] = 'False'

if 'desktop' in devices_to_run:
    devices_args['desktop']['number_of_tests'] = collect_tests(device_name='desktop')
    devices_args['desktop']['run_tests'] = 'True'
else:
    with open('discovered-tests-desktop.txt', mode='w') as tests_file:
        tests_file.writelines('')
    devices_args['desktop']['number_of_tests'] = 1  # has to be 1 as GO CD do not support 0 as number of instances for triggered job
    devices_args['desktop']['run_tests'] = 'False'

job = get_pipeline()
update_job_stages(job=job)
