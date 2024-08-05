import os
import pytest
import urllib3
from crlat_testrail_integration.helpers.conftest_helpers import get_test_module_path
from crlat_testrail_integration.helpers.conftest_helpers import publish_test_result
from crlat_testrail_integration.helpers.conftest_helpers import PyTestStatus
from crlat_testrail_integration.helpers.conftest_helpers import get_test_class_data
from voltron.environments.devices import Devices
from voltron.environments.hosts import hosts
from voltron.utils.get_screenshot import SCREENSHOTS
import cmd_config
from voltron.environments.browser_stack_devices import BS_Devices

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def pytest_addoption(parser):
    parser.addoption('--hostname', action='store', default=hosts.LADBROKES_PROD,
                     help='Provide hostname as a base for URLs, --hostname=invictus.coral.co.uk')
    parser.addoption('--device_name', action='store', default=Devices.GALAXY_S9,
                     help='select device name, one of: Galaxy S9, Note 4, Nexus 5, iPhone 6S, S7, S8, Desktop Chrome etc.')
    parser.addoption('--environment', action='store', default='stg',
                     help='Selects environment for tests execution')
    parser.addoption('--ios_app_path', action='store', default='/Users/Shared',
                     help='Set app path for native iOS app')
    parser.addoption('--browser_stack_device', action='store',
                     default=BS_Devices.SAMSUNG_GALAXY_S23_ANDROID_V13_0_ANDROID,
                     help="Browser stack device")
    parser.addoption('--use_browser_stack', action='store', default=False,
                     help="Run tests using the browser stack")
    parser.addoption('--build_name', action='store', default=None,
                     help="Build Name for grouping build")


def pytest_runtest_setup(item):
    previousfailed = getattr(item.parent, '_previousfailed', None)
    if previousfailed is not None:
        pytest.skip('previous test failed (%s)' % previousfailed.name)


def pytest_terminal_summary(terminalreporter, exitstatus):
    """
    VOLTRON USAGE: to raise custom exception to be able to re-run tests failed on CI
    Add a section to terminal summary reporting.

    :param _pytest.terminal.TerminalReporter terminalreporter: the internal terminal reporter object
    :param int exitstatus: the exit status that will be reported back to the OS

    :return:
    """
    from pytest import ExitCode
    if exitstatus != ExitCode.TESTS_FAILED:
        return
    exceptions_to_rerun = (
        'VoltronException',  # for pageobject exceptions
        'OBException',  # in case smth goes wrong with event creation
        'StaleElementReferenceException',  # in case of unpredictable refresh of DOM/parent
        'ElementNotVisibleException',
        'Error occurred during account request',  # in case of slow response from accounts sharing
        'ConnectionError',  # sometimes it can not connect to SS or CMS
        'SiteServeException',  # in case we accidentally get event without required fields
        'HTTPConnectionPool',  # in case browser failed to start on jenkins grid
        'Timed out receiving message from renderer',  # TimeoutException in case of fail while opening site
    )
    try:
        exception_msg = terminalreporter.stats['failed'][0].longrepr.reprcrash.message
    except Exception as e:
        print(e)
        exception_msg = ''

    if any((True for ex in exceptions_to_rerun if ex in exception_msg)) and os.getenv('RERUN_TEST', 'False') == 'True':
        terminalreporter._session.exitstatus = 86


def get_exception_message_and_trace(excinfo, pyteststatus, report):
    """
    from allure.utils import get_exception_message
    :param excinfo: a :py:class:`py._code.code.ExceptionInfo` from call.excinfo
    :param pyteststatus: the failed/xfailed/xpassed thing
    get exception message from pytest's internal ``report`` object
    """

    message = (excinfo and excinfo.value) or \
              (hasattr(report, 'wasxfail') and report.skipped and 'xfailed') or \
              (hasattr(report, 'wasxfail') and report.failed and 'xpassed') or \
              (pyteststatus) or report.outcome
    stack_trace = report.longrepr or hasattr(report, 'wasxfail') and report.wasxfail
    trace = f'\n\n---\n# Stack-trace: \n    {stack_trace}'

    message_and_trace = {'message': str(message), 'trace': str(trace)}
    if message != 'passed':
        message_and_trace.update({'exception_type': excinfo.typename})

    return message_and_trace


test_results = {}


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    import time
    global test_results
    s = PyTestStatus

    path = get_test_module_path(item)
    test_method = item.obj.__name__

    if call.when == 'setup':
        if path not in test_results.keys():
            test_results[path] = {
                'class_name': item.parent.obj.__name__,
                'device_name': item.parent.obj.device_name,
                'test_data': get_test_class_data(item),
                'custom_step_results': test_results[path]['custom_step_results'] if test_results.get(path) and
                                                                                    test_results[path].get(
                                                                                        'custom_step_results') else {},
            }
        test_results[path]['custom_step_results'].update({test_method: {
            'docstring': item.obj.__doc__,
            'status': '',
        }})

    if not test_results[path].get('start'):
        test_results[path]['start'] = time.time()

    report = (yield).get_result()

    status = item.config.hook.pytest_report_teststatus(report=report, config=item.config)
    status = status and status[0]

    test = test_results[path]

    if report.when == 'call':
        test['status'] = s.PASSED if report.passed else s.FAILED
        if report.passed:
            test_results[path]['custom_step_results'][test_method]['status'] = test['status']
        if report.failed:
            test['failure'] = get_exception_message_and_trace(excinfo=call.excinfo, pyteststatus=status, report=report)
            if test_method not in test['failure'].get('trace').split(test_method, maxsplit=1)[-1] \
                    and test['failure'].get('exception_type') == 'SoftAssertException':
                # to handle situation when there are softAssert failures in test, but last step was passed. It is
                # needed to mark last step passed(if it is passed ofc)
                test['status'] = s.PASSED
            test_results[path]['custom_step_results'][test_method]['status'] = test['status']

    elif report.when == 'setup':  # setup / teardown
        if test.get('status', '') not in [s.PASSED, '']:
            # handle skipped
            test_results[path]['custom_step_results'][test_method]['status'] = s.SKIPPED
        else:
            test['status'] = s.BROKEN
            test['failure'] = get_exception_message_and_trace(excinfo=call.excinfo, pyteststatus=status, report=report)

    elif report.when == 'teardown':
        if not report.passed:
            if report.skipped:
                test_results[path]['custom_step_results'][test_method]['status'] = s.SKIPPED
            elif test['status'] == s.PASSED:
                # if test was OK but failed at teardown => broken
                test['status'] = s.BROKEN
                test['failure'] = get_exception_message_and_trace(excinfo=call.excinfo, pyteststatus=status,
                                                                  report=report)
                test_results[path]['custom_step_results'][test_method]['status'] = test['status']
            elif test['status'] == s.FAILED and test.get('failure').get('message') == 'passed':
                # to handle soft asserts in the last step
                test['status'] = s.BROKEN
                test['failure'] = get_exception_message_and_trace(excinfo=call.excinfo, pyteststatus=status,
                                                                  report=report)
                test_results[path]['custom_step_results'][test_method]['status'] = test['status']
            elif test['status'] == s.FAILED and \
                    get_exception_message_and_trace(excinfo=call.excinfo, pyteststatus=status,
                                                    report=report).get('exception_type') == 'SoftAssertException':
                # to handle situation when some step was failed not because of softAssert, but there are softAssert
                # fails in run
                pass
            else:
                test['status'] = s.BROKEN
                test_results[path]['custom_step_results'][test_method]['status'] = test['status']

    test['stop'] = time.time()
    test_results[path]['custom_step_results'][test_method]['log'] = f'\n{report.caplog}\n'
    test_results[path]['screenshots'] = SCREENSHOTS


def pytest_sessionfinish(session, exitstatus):
    import psutil
    cmdline = psutil.Process(os.getpid()).cmdline()
    import tests
    location = tests.location
    if not any(['--collect-only' in cmdline,
                'gocd_test_runner.py' in cmdline,
                'jenkins_test_discovery.py' in cmdline,
                location == 'IDE']):
        global test_results
        use_browser_stack = session.config.getoption("use_browser_stack")
        if use_browser_stack:
            bs_session_details = session.items[0].parent.obj._bs_session_details
            session_id = session.items[0].parent.obj._bs_session_id
            test_path, test_data = list(test_results.items())[0]
            test_results[test_path]['bs_session_id'] = session_id
            test_results[test_path]['bs_public_url'] = bs_session_details.get("public_url")
        publish_test_result(result=test_results)


def pytest_configure(config):
    cmd_config.hostname = config.getoption("--hostname")
    cmd_config.device_name = config.getoption("--device_name")
    cmd_config.environment = config.getoption("--environment")
    cmd_config.ios_app_path = config.getoption("--ios_app_path")
    cmd_config.browser_stack_device = config.getoption("--browser_stack_device")
    cmd_config.use_browser_stack = config.getoption("--use_browser_stack")
    cmd_config.build_name = config.getoption("--build_name")