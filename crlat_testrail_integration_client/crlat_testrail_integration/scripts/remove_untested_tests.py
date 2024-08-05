import os

from crlat_testrail_integration.testrail import TestRailAPIClient
tr = TestRailAPIClient(user=os.environ.get('TESTRAIL_USER', None),
                       password=os.environ.get('TESTRAIL_PASSWD', None))


def remove_untested_tests():
    test_run_id = os.environ.get('TESTRAIL_ID', None)
    if not test_run_id:
        with open('test_run_id.txt', 'r') as test_run_id_file:
            test_run_id = test_run_id_file.read()
            test_run_id_file.close()

    # tests = tr.get_tests(run_id=test_run_id)
    # not_untested_cases = [test.get('case_id') for test in tests if test.get('status_id') != tr.STATUSES.get('untested')]

    # Date-21/09/2021- Below are the changes with respect to new api change (from line 19-28) -version TestRail 7.2.1
    not_untested_cases = []
    islink_present = True
    count = 0
    while islink_present:
        tests = tr.get_tests(run_id=test_run_id, offset=count)
        not_untested_cases.extend([test.get('case_id') for test in tests['tests']])
        next_link = tests['_links']['next'] if tests['_links']['next'] != None else None
        if next_link is None:
            break
        count += 250

    print(f'*** Found {len(not_untested_cases)} tests for run {test_run_id}')
    tr.update_run(run_id=test_run_id,
                  data={
                      'include_all': False,
                      'case_ids': not_untested_cases
                  })


def main():
    remove_untested_tests()

if __name__ == '__main__':
    main()
