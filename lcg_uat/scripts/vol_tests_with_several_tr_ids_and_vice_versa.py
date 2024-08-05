"""
Script is used to get number of test cases needed to split/combine
Jira: VOL-2756
"""

import os
from collections import Counter
from crlat_testrail_integration.testrail import TestRailAPIClient
TR = TestRailAPIClient()


root = '../tests/'

number_of_tests = 0
tests_t = {}
paths = []

all_TRS = []
tests_v = {}

for path, subdirs, files in os.walk(root):
    for name in files:
        if name.startswith('test_') and name.endswith('.py'):
            tr_items = 0
            path_ = os.path.join(path, name)
            s = open(os.path.join(path, name))

            for line in s:

                if 'TR_ID' in line:
                    try:
                        all_TRS.append(TR.get_testcase_id(line))
                    except IndexError:
                        pass
                    tr_items += 1
            if tr_items > 1:
                paths.append(path_)
                number_of_tests += 1
                tests_t[name] = tr_items

dups = [item for item, count in Counter(all_TRS).items() if count > 1]

print(f'Number of tests with several TR ids: {number_of_tests}')
for i, n in tests_t.items():
    print(f'{i, n}')

print(f'Number of VOL tests that cover same TR: {len(dups)}')
for i_ in dups:
    print(f'C{i_}')


print(f'Path for tests with several TR ids:')
for i, item in enumerate(sorted(paths)):
    print(i, item)
