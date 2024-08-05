import os
import fileinput

from crlat_testrail_integration.testrail import TestRailAPIClient

root = './tests/'


# for adding vol_id into test

if __name__ == '__main__':

    tr = TestRailAPIClient()

    for path, subdirs, files in os.walk(root):
        for name in files:
            if name.startswith('test_') and name.endswith('.py'):
                path_ = os.path.join(path, name)
                print(path_)
                # s = open(os.path.join(path, name)).read()
                # print(s)
                for line in fileinput.FileInput(path_, inplace=True):
                    if 'NAME:' in line:
                        line2 = line.rstrip().replace('\n', '').replace('\r', '').strip()
                        name = tr.get_testcase_name(string=line2)
                        current_section = tr.get_current_section_for_case(path=path_)
                        current_test = tr.get_current_case_from_section(current_section=current_section, test_name=name)
                        vol_id = current_test['id']
                        print('    VOL_ID: C%s\n' % vol_id + line.replace('\n', ''))
                    else:
                        print(line.replace('\n', ''))

