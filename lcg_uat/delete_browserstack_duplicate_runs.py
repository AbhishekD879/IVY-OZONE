import argparse
import base64
import logging
import os
import re
import sys
from time import sleep
from typing import List, Set
from crlat_testrail_integration.testrail import TestRailAPIClient

from voltron.utils.helpers import do_request

sys.path.append(os.getcwd())
logger = logging.getLogger('user_info_logger')

bs_api_host = "https://api.browserstack.com/automate"
testrail_api_host = "https://ladbrokescoral.testrail.com/index.php?/api/v2"


def parse_arguments():
    # Parse command-line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--browsestack_username', '-browsestack_username', help='BrowserStack username',
                        default='avinashmayur_d4Ul2M'.strip(), type=str)
    parser.add_argument('--browserstack_access_key', '-browserstack_access_key',
                        help='BrowserStack access key',
                        default='wGrAm4TUqDsyWARVx9ac'.strip(), type=str)
    parser.add_argument('--build_name', '-build_name',
                        help='build name',
                        default=None)
    return parser.parse_args()


def _get_browserstack_build(build_name: str):
    _url = f"{bs_api_host}/builds.json?limit=100"
    auth = parse_arguments()
    builds = do_request(_url, auth=(auth.browsestack_username, auth.browserstack_access_key), method='GET')
    for build in builds:
        if build_name in build.get('automation_build').get('name'):
            return build.get('automation_build')


def _get_all_browserstack_sessions_ids(build_id: str) -> Set[str]:
    all_records = set()
    offset = 0
    limit = 100
    auth = parse_arguments()
    while True:
        _url = f"{bs_api_host}/builds/{build_id}/sessions.json?limit={limit}&offset={offset}"
        data = do_request(_url, auth=(auth.browsestack_username, auth.browserstack_access_key), method="GET")

        # Extract records and store them in the set
        records = data
        for record in records:
            record_id = record.get("automation_session", {}).get("hashed_id")
            if record_id:
                all_records.add(record_id)

        # Check if there are more records to fetch
        if len(records) < limit:
            break  # All records fetched
        else:
            offset += limit  # Move to the next set of records

    return all_records


def _identify_browserstack_build_name():
    ci_build = os.environ.get('BUILD_NUMBER', 82)
    return f"BUILD_NUMBER:{ci_build}"


def _get_bs_sessions_from_testrail():
    tr = TestRailAPIClient(user=os.environ.get('TESTRAIL_USER', 'pradhan.amitkumar@ivycomptech.com'),
                           password=os.environ.get('TESTRAIL_PASSWD', 'Amit@1234'))
    test_run_id = os.environ.get('TESTRAIL_ID', 221215)
    test_runs_case_ids = []
    islink_present = True
    count = 0
    pattern = r"BS:(\w+)$"
    while islink_present:
        tests = tr.get_tests(run_id=test_run_id, offset=count)
        test_runs_case_ids.extend([test.get('case_id') for test in tests['tests']])
        next_link = tests['_links']['next'] if tests['_links']['next'] != None else None
        if next_link is None:
            break
        count += 250
        sleep(2)
    unique_case_ids = set(test_runs_case_ids)
    return _get_bs_id_from_case_ids(unique_case_ids)


def _get_bs_id_from_case_ids(test_runs_case_ids):
    creds = '%s:%s' % (os.environ.get('TESTRAIL_USER', 'pradhan.amitkumar@ivycomptech.com'),
                       os.environ.get('TESTRAIL_PASSWD', 'Amit@1234'))
    creds = creds.encode()
    auth = base64.b64encode(creds).decode()
    headers = {
        'Authorization': 'Basic %s' % auth,
        'Content-Type': 'application/json'
    }
    test_run_id = os.environ.get('TESTRAIL_ID', 221215)
    bs_id_to_delete = []
    for case_id in test_runs_case_ids:
        _url = f"{testrail_api_host}/get_results_for_case/{test_run_id}/{case_id}"
        try:
            data = do_request(_url, headers=headers, method="GET")
        except Exception:
            sleep(120)
            data = do_request(_url, headers=headers, method="GET")
        sorted_results = sort_data_by_created_on_and_custom(data.get('results'))
        index = 1
        pattern = r"BS:(\w+)"
        for result in sorted_results:
            comment = result.get("comment")
            if comment is not None and isinstance(comment, str):
                match = re.search(pattern, comment)
                if match and match.group(1):  # Check if match is not None and group(1) exists
                    bs_id = match.group(1)
                    if index == 1:
                        index += 1
                    else:
                        bs_id_to_delete.append(bs_id)
                        break
    return set(bs_id_to_delete)


def sort_data_by_created_on_and_custom(data):
    """
    Sorts a list of dictionaries based on the 'created_on' field in descending order,
    and prioritizes elements where 'custom_manual_or_auto' is None.

    Args:
        data (list): List of dictionaries containing the data to be sorted.

    Returns:
        list: Sorted list of dictionaries.
    """
    sorted_data = sorted(data, key=lambda x: (-x['created_on'], x['custom_manual_or_auto'] is None))
    return sorted_data


def _delete_session_from_browserstack(sessions: Set[str]):
    query_string = "?"
    auth = parse_arguments()

    # Convert the set to a list to enable slicing
    session_list = list(sessions)

    # Chunk the sessions into sets of 100 elements each
    chunk_size = 100
    session_chunks = [session_list[i:i + chunk_size] for i in range(0, len(session_list), chunk_size)]

    # Iterate over each chunk and delete sessions
    for session_chunk in session_chunks:
        query_string = "&".join([f'sessionId={session}' for session in session_chunk])
        url = f"{bs_api_host}/sessions/{query_string}"
        do_request(url, auth=(auth.browsestack_username, auth.browserstack_access_key), method="DELETE")


if __name__ == "__main__":
    pass
    # expected_build_name = _identify_browserstack_build_name()
    # build = _get_browserstack_build(expected_build_name)
    # build_status = build.get('status')
    # if build_status == 'done':
    #     print(f"Build Name: {expected_build_name} Completed")
    #     build_id = build.get('hashed_id')
    #     if not build_id:
    #         print(f"Build ID: {build_id} not found")
    #         exit(1)
    #     session_ids = _get_all_browserstack_sessions_ids(build_id)
    # testrail_bs_ids = _get_bs_sessions_from_testrail()
    # _delete_session_from_browserstack(testrail_bs_ids)
