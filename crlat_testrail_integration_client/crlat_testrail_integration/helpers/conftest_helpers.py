"""
Moving all pytest/testrail methods here to keep conftest.py clear
"""
import os
import re
AUTOMATION_REGRESSION_SUITE_ID = 3779
AUTOMATION_SANITY_SUITE_ID = 43740
IOS_FULLY_NATIVE_REGRESSION_PACKAGE_SUITE_ID = 74883
LCG_UAT_AUTOMATION_SUITE_ID = 44818
AUTOMATION_GRID_SUITE_ID = 73189
AUTOMATION_CONNECT_SUITE_ID = 73190

def parse_doc_str(docstring) -> dict:
    """
    Parsing test doctring
    :param docstring:
    :return: dict
    """
    result = {}
    for line in docstring.split('\n'):
        line = line.strip()
        if len(line) == 0:
            continue
        tag_value_list = [subline.strip() for subline in line.split(':', 1)]
        if len(tag_value_list) < 2:
            continue
        tag, value = tag_value_list
        if tag not in result.keys():
            result[tag] = []
        result[tag].append(value)
    result = {tag: '\n'.join(values) for tag, values in result.items()}
    return result


def get_test_module_path(test_method) -> str:
    """
    to get test path
    :param test_method:
    :return:
    """
    return str(test_method.parent.parent.obj.__file__.replace(os.getcwd(), ''))


def get_test_class_data(test_method):
    """
    :param test_method:
    :return:
    """
    test_class_data = {}
    test_class = test_method.parent.obj
    device_name = str(test_class.device_name)  # will return [NONE] for None
    parsed_class_doc_str = parse_doc_str(test_class.__doc__)
    marks = test_class.pytestmark
    marks_dict = {}
    for mark in marks:
        if mark.name == 'incremental':
            continue

        mark_value = mark.args[0] if mark.args else []
        if mark.name in marks_dict:
            marks_dict[mark.name].append(mark_value)
        else:

            marks_dict[mark.name] = [mark_value]

    test_class_data['class_name'] = test_class.__name__
    test_class_data['docstring'] = test_class.__doc__
    test_class_data['device_name'] = device_name
    test_class_data['tr_test_name'] = f'[{device_name.upper()}] {parsed_class_doc_str["NAME"]}'
    test_class_data['marks'] = marks_dict
    test_class_data['steps'] = {}

    return test_class_data


class PyTestStatus(object):
    PASSED = 'passed'
    SKIPPED = 'skipped'
    BROKEN = 'broken'
    FAILED = 'failed'
    CANCELED = 'canceled'
    BLOCKED = 'blocked'
    RETEST = 'retest'


def publish_test_result(result):
    if not result:
        raise Exception('No data for test')

    from crlat_testrail_integration.testrail import TestRailAPIClient
    tr = TestRailAPIClient(user=os.environ.get('TESTRAIL_USER', None),
                           password=os.environ.get('TESTRAIL_PASSWD', None))
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

    tr.suite_id = suite_id

    third_party_exceptions = [
        'SiteServeException',
        'CMSException',
        'OBException',
        'CmsClientException',
        'ThirdPartyDataException',
        'GVCException',
        'PreconditionNotMetException'
    ]

    soft_assert_exception = 'SoftAssertException'

    test_path, test_data = list(result.items())[0]

    docstring = test_data.get('test_data').get('docstring').replace('NAME:', 'NAME: [%s]' % test_data.get('device_name').upper())

    test_name = tr.get_testcase_name(string=docstring)

    path = re.search('(tests.+)', test_path).group(1)
    # Date : 18 nov 2021 : Data from current section method is not beign used anywhere hence commenting the line
    # current_section = tr.get_current_section_for_case(path=path)
    current_section = ''
    current_test = tr.get_current_case_from_section(current_section=current_section, test_name=test_name, path=path)
    test_case_id = current_test['id']

    custom_step_results = []
    for step_name, step_result in test_data.get('custom_step_results').items():
        logs = step_result.get('log').replace('\n', '\n    ')
        content = f'{step_result.get("docstring")} \n {logs}'
        custom_step_results.append({'content': content,
                                    'status_id': tr.STATUSES.get(step_result.get('status'))})

    comment = f'{test_data.get("failure").get("message")} \n {test_data.get("failure").get("trace")}'
    is_test_passed = test_data.get('status') == 'passed' and soft_assert_exception not in comment
    comment = '' if is_test_passed else comment

    if test_data.get("bs_public_url", None):
        comment = f"Browser Stack Public URl: {test_data.get('bs_public_url')} \n \n {comment}"

    if test_data.get('bs_session_id', None):
        comment = f"BS_Session: {test_data.get('bs_session_id')} \n {comment}"

    test_run_id = os.environ.get('TESTRAIL_ID', None)
    if not test_run_id:
        with open('test_run_id.txt', 'r') as test_run_id_file:
            test_run_id = test_run_id_file.read()
            test_run_id_file.close()

    execution_time = str(int((test_data.get('stop') - test_data.get('start'))))
    execution_time = '1' if float(execution_time) < 1 else execution_time
    elapsed = f'{execution_time}.s'

    full_test_result_data = {
        'case_id': test_case_id,
        'status_id': tr.STATUSES.get(test_data['status']),
        'comment': comment,
        'custom_step_results': custom_step_results,
        'elapsed': elapsed,
    }

    if is_test_passed:
        tr.add_result_for_case(run_id=test_run_id, case_id=test_case_id, data=full_test_result_data)

    else:
        defects = test_data.get('test_data').get('marks').get('issue')
        if defects:
            defects_list = [re.search(r'jira\.\w+\.com\/browse\/([\w]+-[\d]+)', defect).group(1) for defect in defects]
            defects_list = ','.join(defects_list)
            full_test_result_data['defects'] = defects_list
        else:
            defects = test_data.get('failure').get('message')
            for exception in third_party_exceptions:
                defects = defects.replace(f'{exception}:', '')
            defects = defects.strip().split('Current content state is:', maxsplit=1)[0][:200]
            full_test_result_data['defects'] = defects
        if any([status in comment for status in ['TestFailure', 'VoltronException']]):
            # exceptions where screenshot/video attachments are present
            if soft_assert_exception in comment:
                status_id = tr.STATUSES['blocked']
            else:
                status_id = tr.STATUSES['failed'] if 'TestFailure' in comment else tr.STATUSES['retest']
            full_test_result_data['status_id'] = status_id
            initial_test_result_data = {
                'case_id': test_case_id,
                'status_id': status_id,
            }
            screenshots = test_data.get('screenshots')

            if screenshots:
                tr_test_result = tr.add_result_for_case(run_id=test_run_id, case_id=test_case_id,
                                                        data=initial_test_result_data)

                screenshot = screenshots[-1]
                import base64
                imgdata = base64.b64decode(screenshot)
                filename = 'screenshot.png'
                with open(filename, 'wb') as f:
                    f.write(imgdata)
                attachment = tr.add_attachment_to_result(result_id=tr_test_result['id'], attachment=filename)
                os.remove(filename)
                attachment_id = attachment.get('attachment_id')
                comment = f'![](https://ladbrokescoral.testrail.com/index.php?/attachments/get/{attachment_id})\n\n{comment}'
                full_test_result_data['comment'] = comment

        elif any([status in comment for status in third_party_exceptions]):
            status_id = tr.STATUSES['blocked']
            full_test_result_data['status_id'] = status_id
        elif 'SKIPIF' in comment:
            # it is needed to mark as 'untested' skipped tests from our framework using 'skipif' mark
            status_id = tr.STATUSES['untested']
            full_test_result_data['status_id'] = status_id
        else:
            # all other exceptions not handled above
            status_id = tr.STATUSES['retest']
            full_test_result_data['status_id'] = status_id
        tr.add_result_for_case(run_id=test_run_id, case_id=test_case_id, data=full_test_result_data)
