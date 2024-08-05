import datetime
import logging
import json
import os
import time
from typing import List, Dict

from influxdb import InfluxDBClient

from crlat_testrail_integration.testrail import TestRailAPIClient


AUTO_FLAGS = ['manual', 'automated', 'cannot be automated']
PRIORITY = ['low', 'medium', 'high', 'critical']
OXYGEN_WEB_REGRESSION_PACKAGE_SUITE = 637
COEFFICIENT_CRITICAL = 4
COEFFICIENT_HIGH = 3
COEFFICIENT_MEDIUM = 2
COEFFICIENT_LOW = 1


class AutomationUITestsCoverage:

    TESTS_LIST = None

    def __init__(self):
        self.coverage_general = None
        self.coverage_critical = None
        self.coverage_high = None
        self.coverage_medium = None
        self.coverage_low = None
        logging.basicConfig(level=logging.DEBUG)
        self.logger = logging.getLogger('automation_ui_tests_coverage')

    def get_all_cases(self) -> List:
        """
        Get all test cases of the test suite or specific section in a test suite
        :return: a list of test cases for a test suite or specific section in a test suite
        """
        tr_user = os.getenv('TR_USER')
        tr_passwd = os.getenv('TR_PASSWD')
        tr = TestRailAPIClient(user=tr_user, password=tr_passwd)
        self.TESTS_LIST = tr.get_cases(suite_id=OXYGEN_WEB_REGRESSION_PACKAGE_SUITE)
        return self.TESTS_LIST

    def sort_test_cases(self) -> Dict:
        """
        Sort test cases by the priority and manual/automated flag
        :return: a dict with sorted test cases by the priority and manual/automated flag
        """
        manual_vs_auto = {name: 0 for name in AUTO_FLAGS}
        tests_by_priority = {n: dict(manual_vs_auto) for n in PRIORITY}
        for testcase in self.TESTS_LIST:
            try:
                if testcase['custom_readiness'] is 3:
                    automated_value = testcase.get('custom_automatedd')
                    auto_index = automated_value - 1 if isinstance(automated_value, int) else 0
                    prio_index = testcase.get('priority_id', 1)-1
                    auto_index = auto_index
                    tests_by_priority[PRIORITY[prio_index]][AUTO_FLAGS[auto_index]] += 1
            except Exception as err:
                self.logger.exception(
                    'Error "%s" processing testcase data: \n%s' % (err, json.dumps(testcase, indent=2)))
                raise err
        return tests_by_priority

    def calculate_coverage(self):
        """
        Calculate coverage of automation test cases using defined formula:
        Coverage = 100*(CriticalAuto*4+HighAuto*3+MediumAuto*2+LowAuto*1)/(CriticalALL*4+HighALL*3+MediumALL*2+LowALL*1)
        :return: coverage in percent of automated testcases (Critical, High, Medium, Low, General)
        """
        self.logger.debug(f'Sorted dictionary of test cases: {json.dumps(self.sort_test_cases(), indent=2)}')
        sorted_testcases = self.sort_test_cases()

        critical_auto = sorted_testcases['critical']['automated']
        high_auto = sorted_testcases['high']['automated']
        medium_auto = sorted_testcases['medium']['automated']
        low_auto = sorted_testcases['low']['automated']

        critical_all = critical_auto + sorted_testcases['critical']['manual']
        high_all = high_auto + sorted_testcases['high']['manual']
        medium_all = medium_auto + sorted_testcases['medium']['manual']
        low_all = low_auto + sorted_testcases['low']['manual']

        self.coverage_critical = 100 * (critical_auto / critical_all)
        self.coverage_high = 100 * (high_auto / high_all)
        self.coverage_medium = 100 * (medium_auto / medium_all)
        self.coverage_low = 100 * (low_auto / low_all)

        self.coverage_general = 100 * (critical_auto * COEFFICIENT_CRITICAL + high_auto * COEFFICIENT_HIGH +
                                       medium_auto * COEFFICIENT_MEDIUM + low_auto * COEFFICIENT_LOW) /\
                                      (critical_all * COEFFICIENT_CRITICAL + high_all * COEFFICIENT_HIGH +
                                       medium_all * COEFFICIENT_MEDIUM + low_all * COEFFICIENT_LOW)

        self.logger.debug(f'Calculated coverage CRITICAL: "{self.coverage_critical}", HIGH: "{self.coverage_high}, '
                          f'MEDIUM: "{self.coverage_medium}", LOW: "{self.coverage_low}", '
                          f'COVERAGE_GENERAL: "{self.coverage_general}"')
        return self.coverage_critical, self.coverage_high, self.coverage_medium, self.coverage_low, self.coverage_general

    def post_to_influxdb(self):
        """
        POST calculated coverage of Automation UI test cases to InfluxDB
        """
        measurement_name = 'Automation tests coverage'
        db_name = 'UI coverage'
        time_value = datetime.datetime.utcfromtimestamp(time.time()).isoformat('T') + 'Z'
        measurement = {
            'measurement': measurement_name,
            'time': time_value,
            'fields': {
                'coverage': self.coverage_general,
                'coverage_critical': self.coverage_critical,
                'coverage_high': self.coverage_high,
                'coverage_medium': self.coverage_medium,
                'coverage_low': self.coverage_low,
            },
        }
        self.logger.debug(f'Influxdb data measurement: "{json.dumps([measurement], indent=2)}"')
        client = InfluxDBClient(
            host='monitor.crlat.net',
            port=8086,
            database='_internal')
        client.create_database(db_name)
        client.write_points([measurement], database=db_name)


if __name__ == '__main__':
    auto_coverage = AutomationUITestsCoverage()
    auto_coverage.get_all_cases()
    auto_coverage.calculate_coverage()
    auto_coverage.post_to_influxdb()
