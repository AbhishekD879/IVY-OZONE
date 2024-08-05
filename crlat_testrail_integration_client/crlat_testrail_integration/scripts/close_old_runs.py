import os
from datetime import datetime
from datetime import timedelta

from crlat_testrail_integration.testrail import TestRailAPIClient
from crlat_testrail_integration.utils.exceptions import TestRailAPIError

tr = TestRailAPIClient(user=os.environ.get('TESTRAIL_USER', None),
                       password=os.environ.get('TESTRAIL_PASSWD', None))

NON_RELEASE_RUNS_DELTA_DAYS = 3
RELEASE_RUNS_DELTA_DAYS = 31
AUTOMATION_RUN_TEMPLATE_NAME = 'Automation Run'


def close_old_runs():
    active_runs = tr.get_runs(is_completed=0)
    automation_runs = [run for run in active_runs['runs'] if AUTOMATION_RUN_TEMPLATE_NAME in run.get('name')]

    print(f'*** Found "{len(automation_runs)}" active Automation Runs')

    for run in automation_runs:
        run_name = run.get('name')
        timedelta_days = RELEASE_RUNS_DELTA_DAYS if 'OX' in run_name else NON_RELEASE_RUNS_DELTA_DAYS
        if datetime.utcfromtimestamp(run.get('created_on')) < (datetime.utcnow() - timedelta(days=timedelta_days)):
            test_run_id = run.get('id')
            print(f'*** Closing run \'{run_name}\' with id \'{test_run_id}\'')
            try:
                # tests = tr.get_tests(run_id=test_run_id)
                # not_untested_cases = [test.get('case_id') for test in tests if
                #                       test.get('status_id') != tr.STATUSES.get('untested')]
                # Date-21/09/2021- Below are the changes with respect to new api change (from line 33-42) -version TestRail 7.2.1
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
                tr.update_run(run_id=test_run_id,
                              data={
                                  'include_all': False,
                                  'case_ids': not_untested_cases
                              })
                tr.close_run(run_id=test_run_id)
            except (Exception, TestRailAPIError):
                pass


def main():
    close_old_runs()

if __name__ == '__main__':
    main()
