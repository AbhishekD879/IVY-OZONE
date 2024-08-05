"""
Script is used to generate list of all unique pytest marks
Jira: VOL-2110
Used for: https://confluence.egalacoral.com/display/SPI/Existing+pytest+marks
"""

import os
from collections import Counter
import re

root = '../tests/'


all_marks = []

number_of_tests = 0

for path, subdirs, files in os.walk(root):
    for name in files:
        if name.startswith('test_') and name.endswith('.py'):
            number_of_tests += 1
            path_ = os.path.join(path, name)
            # print(path_)
            s = open(os.path.join(path, name))

            for line in s:
                if '@pytest.mark' in line:
                    mark = re.match('(@pytest.mark.)(\w+)', line)
                    if mark:
                        all_marks.append(mark.group(2))


print(f'Number of tests: {number_of_tests}')
print(f'Unique marks: {set(all_marks)}')
print(f'Number of unique marks: {len(set(all_marks))}')
print(f'Marks usage: {Counter(all_marks)}')
