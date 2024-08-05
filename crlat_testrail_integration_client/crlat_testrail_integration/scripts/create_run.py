import os
from time import sleep
from crlat_testrail_integration.testrail import TestRailAPIClient


tr = TestRailAPIClient(user=os.environ.get('TESTRAIL_USER', None),
                       password=os.environ.get('TESTRAIL_PASSWD', None))
AUTOMATION_REGRESSION_SUITE_ID = 3779
AUTOMATION_SANITY_SUITE_ID = 43740
IOS_FULLY_NATIVE_REGRESSION_PACKAGE_SUITE_ID = 74883
LCG_UAT_AUTOMATION_SUITE_ID = 44818
AUTOMATION_GRID_SUITE_ID = 73189
AUTOMATION_CONNECT_SUITE_ID = 73190

def create_run():
    test_run_id = os.environ.get('TESTRAIL_ID', None)
    if not test_run_id:
        ci_run_name = os.environ.get('GO_PIPELINE_NAME', None)
        if not ci_run_name:
            ci_run_name = os.environ.get('JOB_NAME', None)
        ci_run_number = os.environ.get('GO_PIPELINE_COUNTER', None)
        if not ci_run_number:
            ci_run_number = os.environ.get('BUILD_NUMBER', None)
        git_branch = os.environ.get('GIT_BRANCH', None)

        hostname = os.environ.get('OX_HOSTNAME', None)
        build_url = os.environ.get('BUILD_URL', None)

        test_path = os.environ.get('TEST_PATH', None)
        if not test_path:
            suite_id = AUTOMATION_REGRESSION_SUITE_ID
        else:
            if 'tests_sanity' in test_path:
                suite_id = AUTOMATION_SANITY_SUITE_ID
            elif ('tests_ios_fully_native_regression' in test_path) or ('tests_android'in test_path):
                suite_id = IOS_FULLY_NATIVE_REGRESSION_PACKAGE_SUITE_ID
            elif 'tests_uat' in test_path:
                suite_id = LCG_UAT_AUTOMATION_SUITE_ID
            elif 'tests_grid' in test_path:
                suite_id = AUTOMATION_GRID_SUITE_ID
            elif 'tests_connect' in test_path:
                suite_id = AUTOMATION_CONNECT_SUITE_ID
            else:
                suite_id = AUTOMATION_REGRESSION_SUITE_ID

        test_run_name = f'Automation Run {ci_run_name} #{ci_run_number}{f" [{git_branch}]" if git_branch else ""} @ {hostname}'

        data_for_run = {
            'name': test_run_name,
            'suite_id': suite_id,
            'include_all': True,
            'milestone_id': tr.milestone_id,
            'refs': git_branch,
            'description': build_url
        }
        try:
            current_run = tr.add_run(data=data_for_run)
        except ConnectionError as e:
            print(f'Got error: {e}')
            sleep(10)
            current_run = tr.add_run(data=data_for_run)

        test_run_id = str(current_run['id'])
        print(f'*** Created run "{test_run_name}" with id: "{test_run_id}"')
    else:
        current_run = tr.get_run(run_id=test_run_id)

        description = current_run.get('description', '')
        build_url = os.environ.get('BUILD_URL', '')
        description = f'{description} \n{build_url}'

        current_run = tr.update_run(run_id=test_run_id, data={'include_all': True,
                                                              'description': description})
        test_run_name = current_run.get('name')
        print(f'*** Using existing run "{test_run_name}" with id: "{test_run_id}"')

    with open('test_run_id.txt', 'w') as test_run_id_file:
        test_run_id_file.write(test_run_id)
        test_run_id_file.close()


def main():
    create_run()

if __name__ == '__main__':
    main()
