# Import necessary modules
import argparse
import base64
import os
import logging
import datetime
from crlat_testrail_integration.utils.request_wrappers import do_request
from crlat_testrail_integration.testrail import TestRailAPIError
from requests import request


# Set up logging with INFO level
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('voltron_logger')


# Define constants for TestRail
class TestrailConstants:
    def __init__(self):
        self.BASE_URL = 'https://ladbrokescoral.testrail.com/'
        self.PROJECT_ID = 36
        self.SUITE_ID = 3779
        self.MILESTONE_ID = 1026
        self.TESTRAIL_USERNAME = 'pradhan.amitkumar@ivycomptech.com' if not \
            os.environ.get('TESTRAIL_USER', None) else os.environ.get('TESTRAIL_USER', None)
        self.TESTRAIL_PASSWORD = 'Amit@1234' if not os.environ.get('TESTRAIL_PASSWD', None) else os.environ.get(
            'TESTRAIL_PASSWD', None)
        self.REQUEST_URL = None
        self.AUTH_TOKEN = None
        self.REQUEST_HEADERS = None


# Function to parse command-line arguments
def parse_arguments():
    parser = argparse.ArgumentParser()
    # Note This Will Include All The Runs for Below specified date example if created_after is 29/07/2022 then
    # This will include all the runs for 29/07/2022
    parser.add_argument('--created_after', help='Only return test runs created after this date (as UNIX timestamp)',
                        type=str, default='1/06/2020')

    # Note This Will Exclude All The Runs for Below specified date example if created_before is 30/07/2022 then
    # This will Exclude all the runs for 30/07/2022
    parser.add_argument('--created_before', help='Only return test runs created before this date (as UNIX timestamp)',
                        type=str, default='2/06/2020')

    parser.add_argument('--created_by', help='A comma-separated list of creators (user IDs) to filter by', type=str,
                        default='191')

    parser.add_argument('--is_completed',
                        help='1 to return completed test runs only. 0 to return active test runs only', type=bool,
                        default=1)

    parser.add_argument('--limit', help='Limit the result to limit test runs.', type=int, default=None)

    parser.add_argument('--offset', help='Use offset to skip records', type=int, default=None)

    parser.add_argument('--milestone_id', help='A comma-separated list of milestone IDs to filter by', type=str,
                        default=None)

    parser.add_argument('--refs_filter', help='A single Reference ID (e.g. TR-a, 4291, etc.)', type=str, default=None)

    parser.add_argument('--suite_id', help='A comma-separated list of test suite IDs to filter by', type=str,
                        default=None)

    parser.add_argument('--delete_all_runs', help='Delete All Runs', type=str,
                        default=True)
    return parser.parse_args()


# Function to check if a test run falls within the given date range
def is_run_within_date_range(run, created_after, created_before):
    # Convert date strings to Unix timestamp
    created_after_unix = date_string_to_unix_timestamp(created_after)
    created_before_unix = date_string_to_unix_timestamp(created_before)

    # Check if the run creation date is within the date range
    return created_after_unix <= run['created_on'] <= created_before_unix


# Function to set up TestRail constants
def setup_testrail_constants():
    testrail_constant = TestrailConstants()
    if not (testrail_constant.TESTRAIL_USERNAME or testrail_constant.TESTRAIL_PASSWORD):
        raise TestRailAPIError('Please set your TestRail username/password')
    if not testrail_constant.BASE_URL.endswith('/'):
        testrail_constant.BASE_URL += '/'

    testrail_constant.REQUEST_URL = testrail_constant.BASE_URL + 'index.php?/api/v2'
    creds = '%s:%s' % (testrail_constant.TESTRAIL_USERNAME, testrail_constant.TESTRAIL_PASSWORD)
    creds = creds.encode()
    testrail_constant.AUTH_TOKEN = base64.b64encode(creds).decode()
    testrail_constant.REQUEST_HEADERS = {
        'Authorization': 'Basic %s' % testrail_constant.AUTH_TOKEN,
        'Content-Type': 'application/json'
    }
    return testrail_constant


# Function to delete a test run
def delete_run(run_id, testrail_constants, soft=0):
    # Define the URL for deleting a test run
    url = f"{testrail_constants.REQUEST_URL}/delete_run/{run_id}/soft={soft}"
    logger.info(f"Deleting run with id: {run_id}")
    # Send a POST request to delete the test run and handle possible responses
    response = request(url=url, method='POST', headers=testrail_constants.REQUEST_HEADERS, timeout=60)

    if response.status_code == 200:
        logger.info(f"Successfully deleted the test run with id: {run_id}")
    elif response.status_code == 400:
        logger.error("Invalid or unknown test run.")
    elif response.status_code == 403:
        logger.error("No permissions to delete test runs or no access to the project.")
    elif response.status_code == 429:
        logger.error("Too many requests. Please wait and try again.")
    else:
        logger.error(f"An error occurred: {response.text}")

    return response


def date_string_to_unix_timestamp(date_string):
    # Define the date format
    date_format = "%d/%m/%Y"
    datetime.datetime.strptime(date_string, date_format).replace(tzinfo=datetime.timezone.utc).timestamp()
    # Try to convert the date string to a datetime object
    try:
        return int(datetime.datetime.strptime(date_string, date_format).replace(tzinfo=datetime.timezone.utc).timestamp())
    except ValueError:
        raise ValueError(
            "The input date string is not in the correct format. Please provide a date in 'dd/mm/yyyy' format.")

    # Convert the datetime object to a UNIX timestamp and return it
    # return int(time.mktime(date_object.timetuple()))


def delete_automation_runs(runs, testrail_constants, args):
    # Log the start of deletion process
    # Open a file to write the runs information
    logger.info(f"Deleting automation runs: {runs}")
    # Parse the date
    date = datetime.datetime.strptime(args.created_after, '%d/%m/%Y')
    path = 'C:\\Automation_Logs\\'
    new_path = f"{path}Runs_info_{date.year}.txt"
    # Format the date
    formatted_date = date.strftime('%b %Y')
    # open the file in append mode
    with open(new_path, "a", encoding='utf-8') as file:
        file.write(f"Start Date: {args.created_after}, Month: {formatted_date}\n")
        for run in runs:
            logger.info(f"Current run: {run}")
            # write the run id and name to the file
            file.write(f"Run ID: {run['id']}, Name: {run['name']}\n")
            delete_run(run['id'], testrail_constants)
        file.write(f"End Date: {formatted_date}\n")
    logger.info("Finished deleting runs.")


# Function to get test runs with certain filters
def get_test_runs_with_filter(filter_args, testrail_constants):
    # Initialize an empty list to store the results
    results = []
    # Define the URL for getting test runs
    url = f"{testrail_constants.REQUEST_URL}/get_runs/{testrail_constants.PROJECT_ID}"
    # Define the filters based on the arguments provided
    filters = {}
    # int(date_string_to_unix_timestamp(filter_args.created_after))
    # int(date_string_to_unix_timestamp(filter_args.created_before))
    if filter_args.created_after:
        filters['created_after'] = int(date_string_to_unix_timestamp(filter_args.created_after))
    if filter_args.created_before:
        filters['created_before'] = int(date_string_to_unix_timestamp(filter_args.created_before))
    if filter_args.created_by:
        filters['created_by'] = filter_args.created_by
    if filter_args.is_completed is not None:
        filters['is_completed'] = filter_args.is_completed
    if filter_args.limit:
        filters['limit'] = filter_args.limit
    if filter_args.offset:
        filters['offset'] = filter_args.offset
    if filter_args.milestone_id:
        filters['milestone_id'] = [int(x) for x in filter_args.milestone_id.split(",")]
    if filter_args.refs_filter:
        filters['refs'] = filter_args.refs_filter
    if filter_args.suite_id:
        filters['suite_id'] = [int(x) for x in filter_args.suite_id.split(",")]
    if filters:
        url += "/" + "&".join(f"{key}={value}" for key, value in filters.items())
    try:
        response = do_request(url, 'GET', testrail_constants.REQUEST_HEADERS)
        if response['runs']:
            # runs_within_date = list(filter(
            #     lambda c_run: is_run_within_date_range(c_run, created_after=filter_args.created_after,
            #                                            created_before=filter_args.created_before), response['runs']))
            if not filter_args.delete_all_runs:
                runs = response['runs']
                for run in runs:
                    if 'Automation Run CRLAT-LCG-UAT-BMA-UI-TESTING-onprem' in run.get('name', '') and \
                            'https://jenkins-vie.coral.co.uk/job/CRLAT-LCG-UAT-BMA-UI-TESTING-onprem/' \
                            in run.get('description', ''):
                        results.append(run)
            else:
                results.extend(response['runs'])
        else:
            raise TestRailAPIError(f"An error occurred: {response}")
    except TestRailAPIError as error:
        logger.error(f"Error occurred while getting test runs: {str(error)}")
    return results


if __name__ == "__main__":
    logger.info("Starting process.")
    args = parse_arguments()
    TESTRAIL_CONSTANTS = setup_testrail_constants()
    all_filtered_runs = get_test_runs_with_filter(filter_args=args, testrail_constants=TESTRAIL_CONSTANTS)
    logger.info(f"All filtered runs: {all_filtered_runs}")
    delete_automation_runs(runs=all_filtered_runs, testrail_constants=TESTRAIL_CONSTANTS, args=args)
    logger.info("Finished process.")
