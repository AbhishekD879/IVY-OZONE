"""
Script is used to update all Ladbrokes-adapted tests with "Autotest adapted for Ladbrokes" = Yes mark
Jira: VOL-3877
"""

import os
from time import sleep
from crlat_testrail_integration.testrail import TestRailAPIClient
from crlat_testrail_integration.utils.exceptions import TestRailAPIError

TR = TestRailAPIClient()


root = '../tests/'
ignored_path = 'pack_901_deprecated_tests'

number_of_tests = 0
number_of_ladbrokes_adapted_tests = 0


TR_ID = 'TR_ID'
pytest_mark = '@pytest.mark.'
LADBROKES_ADAPTED_MARKS = [
    '@pytest.mark.tst2',
    '@pytest.mark.lad_tst2',
    # '@pytest.mark.stg2',
    # '@pytest.mark.lad_stg2',
    '@pytest.mark.hl',
    '@pytest.mark.lad_hl',
    '@pytest.mark.prod',
    '@pytest.mark.lad_prod'
]

for path, subdirs, files in os.walk(root):
    for name in files:
        if ignored_path in path:
            continue
        if name.startswith('test_') and name.endswith('.py'):
            number_of_tests += 1
            ladbrokes_adapted = False
            pytest_marks_for_test = []
            tr_ids_for_test = []

            s = open(os.path.join(path, name))

            for line in s:
                if pytest_mark in line:
                    pytest_marks_for_test.append(line.rstrip())
                if TR_ID in line:
                    try:
                        case_id = TR.get_testcase_id(line)
                        tr_ids_for_test.append(case_id)
                    except IndexError as e:
                        print(f'*** Ex: {str(e)}, {name} - {line}')
                        pass
            ladbrokes_adapted = any(mark in LADBROKES_ADAPTED_MARKS for mark in pytest_marks_for_test)
            print(f'tc {tr_ids_for_test} - {ladbrokes_adapted} adapted | {name}')
            if ladbrokes_adapted:
                for tr_case_id in tr_ids_for_test:
                    try:
                        tr_case = TR.get_case(case_id=tr_case_id)
                    except TestRailAPIError:
                        print(f'#### Not valid id: {tr_case_id}')
                        continue
                    print(f'** updating {tr_case_id} {tr_case["title"]} ')
                    tr_ladbrokes_adapted = tr_case.get('custom_ladbrokes_adapted')
                    if not tr_ladbrokes_adapted:
                        TR.update_case(case_id=tr_case_id, data={'custom_ladbrokes_adapted': 1})
                        sleep(1.5)
                number_of_ladbrokes_adapted_tests += 1
            print('**')


print(f'\nall tests {number_of_tests} \nlads adapted {number_of_ladbrokes_adapted_tests}')
