import os

from behave.model import ScenarioOutline
from behave.model_core import Status
from behave.reporter.base import Reporter
from crlat_testrail_integration.testrail import TestRailAPIClient

OPTIONAL_STEPS = (Status.untested,)
STATUS_ORDER = (
    Status.passed,
    Status.failed,
    Status.skipped,
    Status.undefined,
    Status.untested,
)


def format_summary(statement_type, summary):
    """
    Format TestRail report summary
    :param statement_type: str, TestRail info summary string
    :param summary: dict, summary map with status: number of testcases
    :return: str, formatted summary str
    """
    parts = []
    for status in STATUS_ORDER:
        if status.name not in summary:
            continue
        counts = summary[status.name]
        if status in OPTIONAL_STEPS and counts == 0:
            # -- SHOW-ONLY: For relevant counts, suppress: untested items, etc.
            continue
        statement_type = f'{statement_type}s' if counts != 1 else statement_type
        part = f'{counts} {statement_type} {status.name}' if not parts else f'{counts} {status.name}'
        parts.append(part)
    return f', '.join(parts)


class TestrailReporter(Reporter):
    STATUS_PASSED = 1
    STATUS_BLOCKED = 2
    STATUS_UNTESTED = 3
    STATUS_RETEST = 4
    STATUS_FAILED = 5
    show_failed_cases = True

    CASE_TAG_PREFIX = 'testrail-C'
    ISSUE_TAG_PREFIX = 'JIRA_ID:'

    STATUS_MAP = {
        'passed': STATUS_PASSED,
        'failed': STATUS_FAILED,
        'skipped': STATUS_UNTESTED,
        'undefined': STATUS_UNTESTED,
        'executing': STATUS_UNTESTED,
        'untested': STATUS_UNTESTED,
    }

    def __init__(
            self,
            run_name,
            testrail_project_id,
            testrail_project_suite_id
    ):
        super(Reporter, self).__init__()
        self.testrail_client = None
        self.run_name = run_name
        self.duration = 0.0
        self.failed_cases = []
        self._testrail_project_id = testrail_project_id
        self._testrail_project_suite_id = testrail_project_suite_id
        self._testrail_project_name = f'{run_name}'
        self._testrail_project_test_run = None
        self._testrail_project_cases = {}
        self._testrail_project_milestone_id = None
        self.case_summary = {
            Status.passed.name: 0,
            Status.failed.name: 0,
            Status.skipped.name: 0,
            Status.untested.name: 0,
        }

    def feature(self, feature):
        """
        Called after a feature was processed.
        :param feature: Feature object (as :class:`behave.model.Feature`)
        """
        self.duration += feature.duration
        for scenario in feature:
            if isinstance(scenario, ScenarioOutline):
                self.process_scenario_outline(scenario)
            else:
                self.process_scenario(scenario)

    def end(self):
        """
        Called after all model elements are processed (optional-hook).
        """
        # Removing all untested tests of the run
        # tests = self.testrail_client.get_tests(run_id=self._testrail_project_test_run['id'])
        # not_untested_cases = [test.get('case_id') for test in tests if
        #                       test.get('status_id') != self.testrail_client.STATUSES.get('untested')]

        not_untested_cases = []
        count = 0
        while True:
            cases = self.testrail_client.get_tests(run_id=self._testrail_project_test_run['id'], offset=count)
            not_untested_cases.extend([test.get('case_id') for test in cases['tests']])
            next_link = cases['_links']['next'] if cases['_links']['next'] is not None else None
            if next_link is None:
                break
            count += 250

        print(f'*** Found {len(not_untested_cases)} tests for run {self._testrail_project_test_run["id"]}')
        self.testrail_client.update_run(run_id=self._testrail_project_test_run['id'],
                                        data={
                                            'include_all': False,
                                            'case_ids': not_untested_cases
                                        })
        # Failed testcases summary result
        if self.show_failed_cases and self.failed_cases:
            print(f'\nTestRail results of failed test cases: "{self.failed_cases}" \n')
            print(f'\n')
        # -- SHOW SUMMARY COUNTS:
        print(format_summary('TestRail test case', self.case_summary))
        timings = (int(self.duration / 60.0), self.duration % 60)
        print('Took %dm%02.3fs\n' % timings)

    def _get_testrail_client(self):
        """
        Get TestRail client
        :return: TestRail client
        """
        if not self.testrail_client:
            self.testrail_client = TestRailAPIClient(
                project_id=self._testrail_project_id,
                suite_id=self._testrail_project_suite_id,
                milestone_id=self._testrail_project_milestone_id,
                user=os.environ.get('TESTRAIL_USER', None),
                password=os.environ.get('TESTRAIL_PASSWD', None)
            )
        return self.testrail_client

    def _load_test_cases_for_project(self):
        """
        Load testcases for project
        """
        # cases = self._get_testrail_client().get_cases(self._testrail_project_id, self._testrail_project_suite_id)
        # self._testrail_project_cases = {str(case['id']): case for case in cases}

        count = 0
        while True:
            cases = self._get_testrail_client().get_cases(self._testrail_project_id, self._testrail_project_suite_id,
                                                          offset=count)
            self._testrail_project_cases.update({str(case['id']): case for case in cases['cases']})
            next_link = cases['_links']['next'] if cases['_links']['next'] is not None else None
            if next_link is None:
                break
            count += 250

    def _get_step_info(self, step):
        general_info = f'{step.keyword} {step.name}'
        if step.status == Status.failed:
            exception = f'\n EXCEPTION: "{step.exception}" occurred in'
            location = f'\n LOCATION: "{step.location}"'
            comment = ' \n'.join([f'-> {general_info} {exception} {location} [{step.status}]'])
        else:
            comment = ' \n'.join([f'-> {general_info} [{step.status}]'])
        return comment

    def _buid_comment_for_scenario(self, scenario):
        """
        Build comment for executed scenario
        :param scenario: object behave.scenario
        :return: str, created comment
        """
        comment = f'{scenario.name} \n'
        comment_list = [self._get_step_info(step) for step in scenario.steps]
        comment_as_str = ','.join(comment_list)
        comment += comment_as_str.replace(',', '\n')
        return comment

    def _get_testcase_defect(self, scenario):
        """
        Add Jira defect id to test case
        :param scenario: object behave.scenario
        :return: str, Jira defect link
        """
        defects = None
        for tag in scenario.tags + scenario.feature.tags:
            if tag.startswith(TestrailReporter.ISSUE_TAG_PREFIX):
                defects = tag[len(TestrailReporter.ISSUE_TAG_PREFIX):]
        return defects

    def setup_test_run(self):
        """
        Sets up the TestRail run for testrail_project.
        :return: self._testrail_project_test_run: dict with TestRail project run data
        """
        testrail_project_test_runs = self._get_testrail_client().get_runs()['runs']
        for test_run in testrail_project_test_runs:
            if test_run['name'] == self._testrail_project_name:
                self._testrail_project_test_run = test_run
                return self._testrail_project_test_run
            else:
                data = {
                    'name': self._testrail_project_name,
                    'suite_id': self._testrail_project_suite_id,
                    'include_all': True,
                    'milestone_id': self._testrail_project_milestone_id,
                }
                self._testrail_project_test_run = self._get_testrail_client().add_run(data=data)
                return self._testrail_project_test_run

    def _format_duration(self, duration):
        """
        This function ensure the minimum duration is 1s to prevent TestRail API error:
        Field :elapsed is not in a valid time span format.
        :param duration: float, duration time
        :return: str, string formatted as (duration_in_seconds + 's')
        """
        duration_seconds = max(1, int(duration))
        return f'{duration_seconds}s'

    def _add_test_result(self, case_id, status, comment=f'', elapsed_seconds=1, defects=None):
        """
        Add result of test run
        :param case_id: str, test case id
        :param status: str, status of test case execution
        :param comment: str, comment to test case
        :param elapsed_seconds: str, elapsed seconds
        :param defects: str, defect Jira link id
        :return: result of test run
        """
        if not self._testrail_project_test_run:
            self.setup_test_run()
        elapsed_seconds_formatted = self._format_duration(elapsed_seconds)
        full_test_result_data = {
            'case_id': case_id,
            'status_id': status,
            'comment': comment,
            'elapsed': elapsed_seconds_formatted,
            'defects': defects
        }
        return self._get_testrail_client().add_result_for_case(
            run_id=self._testrail_project_test_run['id'],
            case_id=case_id,
            data=full_test_result_data
        )

    def process_scenario(self, scenario):
        """
        Reports the test results for the given scenario to the TestRail run.
        :param scenario: object behave.scenario
        """
        for tag in scenario.tags + scenario.feature.tags:
            case_id = tag[len(TestrailReporter.CASE_TAG_PREFIX):] \
                if tag.startswith(TestrailReporter.CASE_TAG_PREFIX) else None
            self._load_test_cases_for_project() if not self._testrail_project_cases \
                else self._testrail_project_cases
            if case_id in self._testrail_project_cases:
                testrail_status = self.STATUS_MAP[scenario.status.name]
                # When adding a test result untested status is not allowed status
                # @see http://docs.gurock.com/testrail-api2/reference-results#add_result
                if testrail_status is self.STATUS_UNTESTED:
                    self.case_summary[Status.skipped.name] += 1
                    continue
                comment = self._buid_comment_for_scenario(scenario)
                defects = self._get_testcase_defect(scenario)
                self._add_test_result(
                    case_id=case_id,
                    status=testrail_status,
                    comment=comment,
                    elapsed_seconds=scenario.duration,
                    defects=defects
                )
                if testrail_status == self.STATUS_PASSED:
                    self.case_summary[Status.passed.name] += 1
                if testrail_status == self.STATUS_FAILED:
                    self.failed_cases.append(f'C{case_id}')
                    self.case_summary[Status.failed.name] += 1
            else:
                self.case_summary[Status.untested.name] += 1

    def process_scenario_outline(self, scenario_outline):
        """
        Reports the test results for the given scenario outline to the TestRail run.
        :param scenario_outline: object behave scenario_outline
        """
        for scenario in scenario_outline.scenarios:
            self.process_scenario(scenario)
