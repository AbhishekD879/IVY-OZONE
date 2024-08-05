import os

from crlat_testrail_integration.testrail import TestRailAPIClient, TestRailAPIError

root = './tests/'


#  For "renewing" actual Automation statuses

if __name__ == '__main__':
    tr_manual = TestRailAPIClient(suite_id=637)  # oxygen manual regression suite

    all_manual_cases = tr_manual.get_cases()
    print('** Found %s manual cases' % len(all_manual_cases))

    # set default 'manual' value
    for iteration, test_case in enumerate(all_manual_cases):
        # print(test_case)
        tr_id = test_case['id']
        print('** Check for test #%s, id: %s' % (iteration, tr_id))
        tr_id = test_case['id']
        is_automated = test_case['custom_automatedd']
        if is_automated != 1:
            # 0 - none, 1 - manual, 2 - automated
            try:
                tr_manual.update_case(case_id=tr_id, data={'custom_automatedd': 1})
            except Exception as e:
                print('Exception on test "%s", msg: "%s"' % (test_case, e))

    # get automated testcases
    all_cases = []
    automated_files_without_id = []
    for path, subdirs, files in os.walk(root):
        for name in files:
            if name.startswith('test_') and name.endswith('.py'):
                file_path = os.path.join(path, name)
                # print(filepath)
                F = open(file_path)
                manual_tc_id = None
                for line in F:
                    strip_line = line.strip()
                    if strip_line.startswith('TR_ID'):
                        try:
                            manual_tc_id = tr_manual.get_testcase_id(string=strip_line)
                            # print(strip_line)
                            # print(manual_tc_id)
                            all_cases.append(manual_tc_id)
                        except IndexError:
                            print('** IndexError file without tr_id:')
                            print(file_path)
                            print('**')
                if manual_tc_id is None:
                    print('** file without tr_id:')
                    print(file_path)
                    print('**')
                    automated_files_without_id.append(file_path)

    print('*** Total num automated without tr_id %s, %s' % (len(automated_files_without_id), automated_files_without_id))

    print('*** Total num tr_id mentions: %s' % len(all_cases))

    unique_all_cases = set(all_cases)
    print('*** Total unique tr_id %s' % len(unique_all_cases))

    deleted_manual_cases = []
    for iteration, automated_manual_case_id in enumerate(unique_all_cases):
        print('** Update for test #%s, id: %s' % (iteration, automated_manual_case_id))
        try:
            tr_manual.update_case(case_id=automated_manual_case_id, data={'custom_automatedd': 2})
        except TestRailAPIError:
            print('*** deleted manual testcase %s' % automated_manual_case_id)
            deleted_manual_cases.append(automated_manual_case_id)

    print('*** Num of deleted tc\'s: %s, %s' % (len(deleted_manual_cases), deleted_manual_cases))
