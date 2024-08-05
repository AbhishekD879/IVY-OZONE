import json
import os

from crlat_testrail_integration.testrail import TestRailAPIClient


tr = TestRailAPIClient(user=os.environ.get('TESTRAIL_USER', None),
                       password=os.environ.get('TESTRAIL_PASSWD', None))


def create_results_file():

    test_run_id = os.environ.get('TESTRAIL_ID', None)
    if not test_run_id:
        with open('test_run_id.txt', 'r') as test_run_id_file:
            test_run_id = test_run_id_file.read()
            test_run_id_file.close()

    tests = tr.get_tests(run_id=test_run_id)
    results = {test.get('case_id'): test for test in tests}
    print(f'Found "{len(results)}" results')

    json_file_name = os.getenv('RESULTS_JSON')
    print(f'JSON file name: "{json_file_name}"')
    if json_file_name:
        with open(json_file_name, 'w') as f:
            json.dump(results, f, indent=2)


def main():
    create_results_file()

if __name__ == '__main__':
    main()
