#
# TestRail API binding for Python 2.x and 3.x (API v2, available since
# TestRail 3.0)
#
# Learn more:
#
# http://docs.gurock.com/testrail-api2/start
# http://docs.gurock.com/testrail-api2/accessing
#
# Copyright Gurock Software GmbH. See license.md for details.
#
import base64
import getpass
import re

import keyring

from crlat_testrail_integration.utils.exceptions import TestRailAPIError
from crlat_testrail_integration.utils.log_mngr import setup_custom_logger
from crlat_testrail_integration.utils.request_wrappers import do_request


# User/pass for testrail account: Coral.Calendar.Invites@symphony-solutions.eu / Secret#1

all_cases_data = []
all_section_data = []

class TestRailAPIClient(object):
    _logger = setup_custom_logger()

    def __init__(self,
                 base_url='https://ladbrokescoral.testrail.com/',
                 project_id=36,
                 suite_id=3779,
                 milestone_id=1026,
                 user=None,
                 password=None):
        self.project_id = project_id
        self.suite_id = suite_id
        self.milestone_id = milestone_id
        (self.user, self.password) = (user, password) if (user and password) else self.get_testrail_username_password()
        # (self.user, self.password) = 'Coral.Calendar.Invites@symphony-solutions.eu', 'Secret#1' # for debugging
        if not (self.user or self.password):
            raise TestRailAPIError('Please set your TestRail username/password')
        if not base_url.endswith('/'):
            base_url += '/'
        self.url = base_url + 'index.php?/api/v2'
        creds = '%s:%s' % (self.user, self.password)
        creds = creds.encode()
        self.auth = base64.b64encode(creds).decode()
        self.headers = {
            'Authorization': 'Basic %s' % self.auth,
            'Content-Type': 'application/json'
        }

    # # # # # V O L T R O N # # # #
    # Custom testrail API methods #
    # # # # # V O L T R O N # # # #

    STATUSES = {
        'passed': 1,
        'canceled': 2,
        'blocked': 2,
        'broken': 2,
        'untested': 3,
        'retest': 4,
        'failed': 5,
    }

    @staticmethod
    def get_testrail_username_password():
        username = keyring.get_password('testrail_username', 'username')
        if not username:
            username = getpass.getpass('Please set your Testrail username')
            keyring.set_password('testrail_username', 'username', username)

        password = keyring.get_password('testrail_password', 'password')
        password = password.replace('\\', '')
        if not password:
            password = getpass.getpass('Please set your Testrail password')
            keyring.set_password('testrail_password', 'password', password)
        return username, password

    def get_case(self, case_id):
        """
        :param case_id: The ID of the test case
        :return: an existing test case.
        """
        return do_request(method='GET', url='%s/get_case/%s' % (self.url, case_id), headers=self.headers)

    def get_cases(self, project_id=None, suite_id=None, section_id=None, test_name=None, offset=0):
        """
        :param project_id: The ID of the project
        :param suite_id: The ID of the test suite (optional if the project is operating in single suite mode)
        :param section_id: The ID of the section (optional)
        :return: a list of test cases for a test suite or specific section in a test suite.
        """
        # 23 Nov 2021 - Added filter by title in parameter, now testcase will retrieve based on the title
        project_id = project_id if project_id is not None else self.project_id
        suite_id = suite_id if suite_id is not None else self.suite_id
        params = {
            'suite_id': suite_id,
        }
        if section_id is not None:
            params.update({'section_id': section_id})
        params_str = '&'.join(['%s=%s' % (k, v) for k, v in params.items()])
        return do_request(method='GET',
                          url='{host_name}/get_cases/{project_id}&suite_id={suite_id}&offset={offset}&filter={test_name}'
                          .format(host_name=self.url, project_id=project_id, suite_id=suite_id, offset=offset, test_name=test_name),
                          headers=self.headers)

    def add_case(self, title, section_id='', custom_device=None, custom_brand=None, custom_readiness=None,
                 custom_automatedd=None, custom_purpose=None, custom_feature=None, custom_complexity=None):
        """
        Method used for creation new testcase in TestRail
        :param title: Required name of test
        :type title: str
        :param section_id: Id of section where test should be located
        :type section_id: str or int
        :param custom_device: 1 – mobile, 2 – tablet, 3 – desktop. By default - all devices
        :type custom_device: list
        :param custom_brand: 1 – Coral only, 2 – Ladbrokes, 3 – both. By default – both Coral and Ladbrokes
        :type custom_brand: int
        :param custom_readiness: 1 - Work in Progress, 2 - Automation Review, 3 - Ready. By default - Ready
        :type custom_readiness: int
        :param custom_automatedd: 1 - Manual, 2 - Automated, 3 - Cannot be automated. By default - Automated
        :type custom_automatedd: int
        :param custom_purpose: 1 - Positive, 2 - Negative. By default - Positive
        :type custom_purpose: int
        :param custom_feature: Id of feature. By default - Other
        :type custom_feature: int
        :param custom_complexity: 1 - Simple, 2 - Medium, 3 - Complex
        :type custom_complexity: int
        :return: same as get_case
        """
        custom_device = custom_device if custom_device else [1, 2, 3]
        custom_brand = custom_brand if custom_brand else 3
        custom_readiness = custom_readiness if custom_readiness else 3
        custom_automatedd = custom_automatedd if custom_automatedd else 2
        custom_purpose = custom_purpose if custom_purpose else 1
        custom_feature = custom_feature if custom_feature else 17
        custom_complexity = custom_complexity if custom_complexity else 2
        return do_request(method='POST',
                          url='{host_name}/add_case/{section_id}'.format(host_name=self.url, section_id=section_id),
                          headers=self.headers,
                          data={'title': title,
                                'custom_device': custom_device,
                                'custom_brand': custom_brand,
                                'custom_readiness': custom_readiness,
                                'custom_automatedd': custom_automatedd,
                                'custom_purpose': custom_purpose,
                                'custom_feature': custom_feature,
                                'custom_complexity': custom_complexity
                                })

    def update_case(self, case_id, data):
        """
        Updates an existing test case (partial updates are supported, i.e. you can submit and update specific fields only).
        :param case_id: The ID of the test case
        :return: the same response format as get_case
        """
        return do_request(method='POST',
                          url='{host_name}/update_case/{case_id}'.format(host_name=self.url, case_id=case_id),
                          headers=self.headers,
                          data=data)

    def get_section(self, section_id):
        """
        :param section_id: The ID of the section
        :return: an existing section
        """
        return do_request(method='GET',
                          url='{host_name}/get_section/{section_id}'.format(host_name=self.url, section_id=section_id),
                          headers=self.headers)

    def add_section(self, data):
        """
        Creates a new section.
        :param project_id: The ID of the project
        :param suite_id: The ID of the suite
        :param data: post data
        :return: the same as get_section
        """
        return do_request(method='POST',
                          url='{host_name}/add_section/{project_id}&suite_id={suite_id}'
                              .format(host_name=self.url, project_id=self.project_id, suite_id=self.suite_id),
                          headers=self.headers,
                          data=data)

    def get_sections(self, offset=0):
        """
        :param offset: Number that sets the position where the response should start from
        :param project_id:
        :param suite_id:
        :return: a list of sections for a project and test suite.
        :Code update date: 07/10/2021
        :Below are the changes with respect to new api change -version TestRail 7.2.1
        :Adding parameter offset=0 and change the url format
        """
        return do_request(method='GET',
                          url='{host_name}/get_sections/{project_id}&suite_id={suite_id}&offset={offset}'
                          .format(host_name=self.url, project_id=self.project_id, suite_id=self.suite_id,
                                  offset=offset),
                          headers=self.headers)

    def get_runs(self, is_completed=0):
        """
        :param project_id: The ID of the project
        :param is_completed: 1 to return completed test runs only. 0 to return active test runs only.
        :return: a list of test runs for a project
        """
        return do_request(method='GET',
                          url='{host_name}/get_runs/{project_id}&is_completed={is_completed}'
                          .format(host_name=self.url, project_id=self.project_id, is_completed=is_completed),
                          headers=self.headers)

    def get_run(self, run_id):
        """
        :param run_id: The ID of the test run
        :return: an existing test run
        """
        return do_request(method='GET',
                          url='{host_name}/get_run/{run_id}'
                          .format(host_name=self.url, run_id=run_id),
                          headers=self.headers)

    def add_run(self, data):
        """
        Creates a new test run.
        :param project_id:
        :return: the same response as get_run.
        """
        return do_request(method='POST',
                          url='{host_name}/add_run/{project_id}'.format(host_name=self.url, project_id=self.project_id),
                          headers=self.headers,
                          data=data)

    def update_run(self, data, run_id):
        """
        Updates an existing test run
        :param data:
        :param run_id: The ID of the test run
        :return: the same response as get_run.
        """
        return do_request(method='POST',
                          url='{host_name}/update_run/{run_id}'.format(host_name=self.url, run_id=run_id),
                          headers=self.headers,
                          data=data)

    def close_run(self, run_id):
        """
        Closes an existing test run and archives its tests & results.
        :param run_id: The ID of the test run
        :return: the same response as get_run.
        """
        return do_request(method='POST',
                          url='{host_name}/close_run/{run_id}'.format(host_name=self.url, run_id=run_id),
                          headers=self.headers)

    def delete_run(self, run_id):
        """
        Deletes an existing test run.
        :param run_id: The ID of the test run
        :return: 200: Success, the test run and all its tests & results were deleted
        :return: 400: Invalid or unknown test run
        :return: 403: No permissions to delete test runs or no access to the project
        """
        return do_request(method='POST',
                          url='{host_name}/delete_run/{run_id}'.format(host_name=self.url, run_id=run_id),
                          headers=self.headers)

    def get_tests(self, run_id, offset=0):
        """
        :param offset: Number that sets the position where the response should start from
        :param run_id: The ID of the test run
        :return: a list of tests for a test run.
        :Code update date: 21/09/2021
        :Below are the changes with respect to new api change -version TestRail 7.2.1
        :Adding parameter offset=0 and change the url format
        """
        url = '{host_name}/get_tests/{run_id}&status_id=1,2,4,5&offset={offset}'.format(host_name=self.url,
                                                                                        run_id=run_id, offset=offset)
        return do_request(method='GET',
                          url=url,
                          headers=self.headers)

        # return do_request(method='GET',
        #                   url='{host_name}/get_tests/{run_id}'.format(host_name=self.url, run_id=run_id),
        #                   headers=self.headers)

    def add_result(self, test_id, data):
        """
        Adds a new test result, comment or assigns a test.
        :param test_id: The ID of the test the result should be added to
        :return: the new test result
        """
        return do_request(method='POST',
                          url='{host_name}/add_result/{test_id}'.format(host_name=self.url, test_id=test_id),
                          headers=self.headers,
                          data=data)

    def add_results(self, run_id, data):
        """
        Adds one or more new test results, comments or assigns one or more tests.
        :param run_id: The ID of the test run the results should be added to
        :param data:
        :return: the same response as get_results
        """
        return do_request(method='POST',
                          url='{host_name}/add_results/{run_id}'.format(host_name=self.url, run_id=run_id),
                          headers=self.headers,
                          data=data)

    def add_results_for_cases(self, run_id, data):
        """
        Adds one or more new test results, comments or assigns one or more tests using the case IDs.
        :param run_id: The ID of the test run the results should be added to
        :param data:
        :return: the same response as get_results
        """
        return do_request(method='POST',
                          url='{host_name}/add_results_for_cases/{run_id}'.format(host_name=self.url, run_id=run_id),
                          headers=self.headers,
                          data=data)

    def add_result_for_case(self, run_id, case_id, data):
        """
        Adds a new test result, comment or assigns a test (for a test run and case combination).
        :param run_id: The ID of the test run
        :param case_id: The ID of the test case
        :param data: dict with possible keys:
                status_id 	int 	The ID of the test status
                comment 	string 	The comment / description for the test result
                version 	string 	The version or build you tested against
                elapsed 	timespan 	The time it took to execute the test, e.g. "30s" or "1m 45s"
                defects 	string 	A comma-separated list of defects to link to the test result
                assignedto_id 	int 	The ID of a user the test should be assigned to
            Custom fields are supported as well and must be submitted with their system name, prefixed with 'custom_'
        :return: If successful, this method returns the new test result using the same response format as get_results, but with a single result instead of a list of results.
        """
        return do_request(method='POST',
                          url='{host_name}/add_result_for_case/{run_id}/{case_id}'.format(host_name=self.url, run_id=run_id, case_id=case_id),
                          headers=self.headers,
                          data=data)

    def get_all_sections_data(self):
        """
        Date-07 Oct 2021
        To get all sections data use this method. Added method with respect new API's update from Testrail API-7.2.1
        :return: If successful, this method returns all the sections data from the respective suite
        """
        self._logger.info('********* Collecting Section data from testrail **********')
        print('********* Collecting Section data from testrail **********')
        count = 0
        while True:
            sections = self.get_sections(offset=count)
            all_section_data.extend(sections['sections'])
            next_link = sections['_links']['next'] if sections['_links']['next'] != None else None
            if next_link is None:
                break
            count += 250

        return all_section_data

    def get_current_section_for_case(self, path):
        """
        :param path: path to the test (e.g. tests.pack003.test_C29588 or tests/pack003/test_C29588.py)
        :return: Current section where testcase is placed
        """
        path = path.replace('.', '/').split('/')
        path[0] = 'Automation Tests'

        # available_sections = self.get_sections()
        # parent_section_id = None
        # for folder in path:
        #     if folder.startswith('test_'):
        #         break
        #     current_section = next((section for section in available_sections['sections']
        #                             if (section['name'] == folder and section['parent_id'] == parent_section_id)), None)
        #     if not current_section:
        #         current_section = self.add_section(data={'name': folder, 'parent_id': parent_section_id, 'suite_id': self.suite_id})
        #     parent_section_id = current_section['id']
        #     # self._logger.debug('*** Parent section id %s' % parent_section_id)

        # Added below changes with respective new API change from testrail. Testrail API - 7.2.1 (Date - 07 Oct 2021)
        global all_section_data
        try:
            if not all_section_data:
                self.get_all_sections_data()
        except Exception as e:
            all_section_data.clear()
            self.get_all_sections_data()

        parent_section_id = None
        for folder in path:
            if folder.startswith('test_'):
                break
            current_section = next((section for section in all_section_data
                                    if (section['name'] == folder and section['parent_id'] == parent_section_id)), None)
            if not current_section:
                current_section = self.add_section(
                    data={'name': folder, 'parent_id': parent_section_id, 'suite_id': self.suite_id})
            parent_section_id = current_section['id']

        return current_section

    def get_all_cases_data(self, current_section):

        """
        To get all test cases data from respective suite use this method. Added method with respect new API's update from Testrail API-7.2.1 (Date - 07 Oct 2021)
        :param current_section:
        :return: If successful, it will return all the testcase data.
        """
        self._logger.info('********* Collecting Cases data from testrail **********')
        print('********* Collecting Get Cases data from testrail**********')
        count = 0
        while True:
            # cases = self.get_cases(section_id=current_section['id'], offset=count)
            # Date : 18 nov 2021 : Data from current section method is not beign used anywhere hence passing blank value for section_id
            cases = self.get_cases(section_id=current_section, offset=count)
            all_cases_data.extend(cases['cases'])
            next_link = cases['_links']['next'] if cases['_links']['next'] != None else None
            if next_link is None:
                break
            count += 250

        return all_cases_data

    def get_current_case_from_section(self, current_section, test_name, path):
        """
        :param path: Testcase path
        :param current_section:
        :param test_name: Name of the test
        :return:
        """
        # all_cases = self.get_cases(section_id=current_section['id'])
        # current_test = next((test for test in all_cases['cases'] if test['title'] == test_name), None)
        # if not current_test:
        #     current_test = self.add_case(title=test_name, section_id=current_section['id'])
        # # self._logger.debug('*** Current test information: %s' % current_test)

        # Added below changes with respective new API change from testrail. Testrail API - 7.2.1 (Date - 07 Oct 2021)
        # (Date - 23 Nov 2021) Commenting below batch wise code as implementing get_cases method with title
        # global all_cases_data
        # try:
        #     if not all_cases_data:
        #         self.get_all_cases_data(current_section)
        # except Exception as e:
        #     all_cases_data.clear()
        #     self.get_all_cases_data(current_section)
        #current_test = next((test for test in all_cases_data if test['title'] == test_name), None)

        cases = self.get_cases(test_name=test_name)
        current_test = None
        if cases['cases']:
            # case = cases['cases'][0]
            current_test = cases['cases'][0] if cases['cases'][0]['title'] == test_name else next((test for test in cases['cases'] if test['title'] == test_name), None)
        if not current_test:
            # Adding get current section code, since add case method require section-id
            print('********* Adding new Test Case in testrail ********** %s ' % test_name)
            current_section = self.get_current_section_for_case(path)
            current_test = self.add_case(title=test_name, section_id=current_section['id'])

        return current_test

    def update_steps(self, steps, current_test):
        """
        :param steps: step methods from test class
        :param current_test:
        :return:
        """
        steps_list = []
        for step in steps:
            step_docstring = step.__doc__
            step_name = step.__name__
            if step_docstring is None:
                raise TestRailAPIError('Please add DESCRIPTION/EXPECTED fields into docstring for step "%s"' % step_name)
            split_string = step_docstring.split('\n')
            description = [line.replace('DESCRIPTION:', '') for line in split_string if line.strip().startswith('DESCRIPTION')]
            description = description if description else '* ' + step_name
            description = '* '+'\n* '.join(description) if isinstance(description, list) else description
            expected = '* '+'\n* '.join([line.replace('EXPECTED:', '') for line in split_string if line.strip().startswith('EXPECTED')])

            # self._logger.debug('*** Step description %s' % description)
            # self._logger.debug('*** Step expected result %s' % expected)
            steps_list.append({'content': description, 'expected': expected})
        if steps_list == current_test['custom_steps_separated']:
            # self._logger.info('*** No need to update steps for test')
            pass
        else:
            self.update_case(case_id=current_test['id'], data={'custom_steps_separated': steps_list})

    def get_testcase_name(self, string):
        """
        :param string: docstring of current test
        :return: Actual name of the test
        """
        name = re.search(r'NAME: (.+)', string)
        if not name:
            raise TestRailAPIError('Test docstring "%s" do not match required parameters' % string)
        return ((name.group(1).split('DESCRIPTION:')[0]).split('PRECONDITIONS')[0][:250]).strip()

    def get_testcase_id(self, string):
        """
        :param string: docstring of current test
        :return: Actual id of the TestRail test case
        """
        id = re.search(r'TR_ID: (.+)', string)
        if not id:
            raise TestRailAPIError('Test docstring "%s" do not match required parameters' % string)
        return re.findall('\d+', id.group(1))[0]

    def get_voltron_testcase_id(self, string):
        """
        :param string: docstring of current test
        :return: Actual id of the TestRail test case for Voltron tests
        """
        vol_id = re.search(r'VOL_ID: (C\d+)', string)
        return None if not vol_id else re.findall('\d+', vol_id.group(1))[0]

    def add_attachment_to_result(self, result_id: (str, int), attachment: str) -> dict:
        """
        Adds attachment to a result based on the result ID. The maximum allowable upload size is set to 256mb.
        :param result_id: The ID of the result the attachment should be added to
        :param attachment: path to attachment file
        :return: dict with attachment_id. e.g {'attachment_id': 86}
        """
        headers = self.headers.copy()
        headers.pop('Content-Type')
        return do_request(method='POST',
                          url='{host_name}/add_attachment_to_result/{result_id}'.format(host_name=self.url, result_id=result_id),
                          files={'attachment': open(attachment, 'rb')},
                          headers=headers)
