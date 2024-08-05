import os

import shutil
from crlat_testrail_integration.testrail import TestRailAPIClient

TR = TestRailAPIClient()

root = './tests/'
skip_dir = 'pack901_deprecated_tests'

# generated from testrail_integration_tools
manual_qa_structure = '/Users/mykhailo/PycharmProjects/testrail_integration_tools/testrail_integration_tools/tmp/repo/S637_Oxygen_Web_Regression_Package/'

counter = 0
for path, subdirs, files in os.walk(root):
    subdirs.remove(skip_dir) if skip_dir in subdirs else None

    for name in files:
        if name.startswith('test_') and name.endswith('.py'):
            counter += 1
            file_path = os.path.join(path, name)
            print(counter)

            s = open(file_path)
            tr_id_present = False
            for line in s:
                if 'TR_ID' in line:
                    tr_id_present = True
                    try:
                        test_case_id = TR.get_testcase_id(string=line)
                        test_case_string_part = f'_C{test_case_id}_'
                        s.close()
                        # print(test_case_id)
                        #
                        for path_manual, subdirs_manual, files_manual in os.walk(manual_qa_structure):
                            for name_manual in files_manual:
                                if test_case_string_part in name_manual:
                                    new_path = path_manual.replace(manual_qa_structure, '')
                                    new_full_path = f'{root}{new_path}/'

                                    full_path_to_test = './'
                                    for path_to_test in new_full_path.split('/')[1:-1]:
                                        full_path_to_test += f'{path_to_test}/'
                                        try:
                                            os.stat(full_path_to_test)
                                        except:
                                            os.makedirs(full_path_to_test)
                                            open(os.path.join(full_path_to_test, '__init__.py'), 'w').close()
                                        import time
                                        time.sleep(0.01)

                                    try:
                                        os.stat(new_full_path)
                                    except:
                                        os.makedirs(new_full_path)
                                        open(os.path.join(new_full_path, '__init__.py'), 'w').close()
                                    # print(new_full_path)
                                    shutil.move(src=file_path,
                                                dst=f'{new_full_path}{name}')

                                    print('***')
                        file_path = path_manual = subdirs_manual = files_manual = name_manual = test_case_id = new_path = new_full_path = name = ''
                    except IndexError:
                        print('************************ IndexError ************************')
                        print(file_path)
                        print('************************ IndexError ************************')

                    break

            if not tr_id_present:
                print('************************ NO TR ************************')
                print(file_path)
                print('************************ NO TR ************************')
