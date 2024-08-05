import itertools
import os
import random
import re
from collections import defaultdict

from crlat_testrail_integration.testrail import TestRailAPIClient

HOSTNAME = os.environ.get('OX_HOSTNAME', None)
AUTOMATION_EMAIL = 'lcl.aqa@ladbrokescoral.com'
STATUS_TO_ID_MAP = {
    'PASSED': 1,
    'BLOCKED': 2,
    'UNTESTED': 3,
    'RETEST': 4,
    'FAILED': 5,
}
ID_TO_STATUS_MAP = {v: k for k, v in STATUS_TO_ID_MAP.items()}

tr = TestRailAPIClient(user=os.environ.get('TESTRAIL_USER', None),
                       password=os.environ.get('TESTRAIL_PASSWD', None))


def generate_device_table(device_count):
    # Calculate the maximum length of device names
    max_device_length = max(len(key) for key in device_count.keys())
    colors = ["#87e5e5", '#bffc4e', '#38a59d', '#eacf9a', '#dbdcff']
    # Create table rows with cycling colors
    color_cycle = itertools.cycle(colors)
    table_rows = [
        f"<tr>"
        f"<td style='padding: 5px; width: {max_device_length}em; background-color: {next(color_cycle)}; border: 1px solid black; border-radius: 4px;'>{key}</td>"
        f"<td style='padding: 5px; border: 1px solid black;'>{value}</td>"
        f"</tr>"
        for key, value in device_count.items()
    ]

    # Join rows to form the table
    devices_table = (
        f"<table style='border-collapse: collapse; text-align: center; border: 1px solid black; display: inline-table;'>"
        f"<tr>"
        f"<th style='padding: 10px; border: 1px solid black; background-color:#b4c6e7'>Device</th>"
        f"<th style='padding: 10px; border: 1px solid black; background-color:#b4c6e7'>Count</th>"
        f"</tr>"
        f"{''.join(table_rows)}"
        f"</table>"
    )

    return devices_table


def create_data_for_email():
    test_run_id = os.environ.get('TESTRAIL_ID', None)
    if not test_run_id:
        with open('test_run_id.txt', 'r') as test_run_id_file:
            test_run_id = test_run_id_file.read()
            test_run_id_file.close()

    # tests = tr.get_tests(run_id=test_run_id)

    body = '<p>Hello All,<br/>Please find Sportsbook Automation run report:<br/></p>'

    body += \
        f"""
    <table style="margin-bottom:1rem;border-collapse:collapse;">
      <tr>
        <td style="padding:0.5rem 1rem;font-size:1.2em;border:1px solid black;"><h3 style="margin:0;font-size:1em;">Testrail Report:</h3></td>
        <td style="padding:0.5rem 1rem;font-size:1em;border:1px solid black;"><a href="https://ladbrokescoral.testrail.com/index.php?/runs/view/{test_run_id}" style="font-size:1em;">TestRail Run:{test_run_id}</a></td>
      </tr>
      <tr>
        <td style="padding:0.5rem 1rem;font-size:1.2em;border:1px solid black;"><h3 style="margin:0;font-size:1em;">Test Environment:</h3></td>
        <td style="padding:0.5rem 1rem;font-size:1em;border:1px solid black;"><a href="https://{HOSTNAME}" style="font-size:1em;">{HOSTNAME}</a></td>
      </tr>
    </table>
    """

    body += """
    <h1 style="margin:1rem 0;font-size:1.3em;text-decoration:underline;">Automation Test Summary:</h1>
    """

    # total_num_tests = len(tests)
    # summary = {status_name: 0 for status_name in STATUS_TO_ID_MAP.keys()}
    # for test in tests:
    #     case_status_int = test.get('status_id')
    #     summary[ID_TO_STATUS_MAP[case_status_int]] += 1

    # Date-21/09/2021- Below are the changes with respect to new api change (from line 50-67) -version TestRail 7.2.1
    test_list = []
    islink_present = True
    count = 0
    while islink_present:
        tests = tr.get_tests(run_id=test_run_id, offset=count)
        test_list.extend([tests['tests']])
        next_link = tests['_links']['next'] if tests['_links']['next'] != None else None
        if next_link is None:
            break
        count += 250

    summary = {status_name: 0 for status_name in STATUS_TO_ID_MAP.keys()}
    total_num_tests = 0
    device_pattern = re.compile(r'\[(.*?)\]')
    device_count = defaultdict(int)
    for test in test_list:
        for final in test:
            case_status_int = final.get('status_id')
            summary[ID_TO_STATUS_MAP[case_status_int]] += 1
            total_num_tests += 1
            match = device_pattern.search(final.get('title'))
            if match:
                # Extract the device name including square brackets
                device_name = match.group(0)
                # Increment the count for this device name
                device_count[device_name] += 1

    body += f"""
        <div style="display:flex;gap:1rem;align-items:center;margin-bottom:1rem;">
          <div style="display:flex;flex-direction:column;align-items:center;justify-content:center;width:8rem;aspect-ratio:1;background-color:#67c2ef;gap:.5rem;border-radius:4px;box-shadow:1px 1px 5px lightgrey;">
            <h1 style="margin:0;padding:0;font-size:2em;">{total_num_tests}</h1>
            <p style="margin:0;padding:0;font-size:1em;">Total</p>
          </div>

          <div style="display:flex;flex-direction:column;align-items:center;justify-content:center;width:8rem;aspect-ratio:1;background-color:#79c447;gap:.5rem;border-radius:4px;box-shadow:1px 1px 5px lightgrey;">
            <h1 style="margin:0;padding:0;font-size:2em;">{summary.get('PASSED')}</h1>
            <p style="margin:0;padding:0;font-size:1em;">Passed</p>
          </div>

          <div style="display:flex;flex-direction:column;align-items:center;justify-content:center;width:8rem;aspect-ratio:1;background-color:#ff5454;gap:.5rem;border-radius:4px;box-shadow:1px 1px 5px lightgrey;">
            <h1 style="margin:0;padding:0;font-size:2em;">{summary.get('FAILED')}</h1>
            <p style="margin:0;padding:0;font-size:1em;">Failed</p>
          </div>
           
           <div style="display:flex;flex-direction:column;align-items:center;justify-content:center;width:8rem;aspect-ratio:1;background-color:#eba56f;gap:.5rem;border-radius:4px;box-shadow:1px 1px 5px lightgrey;">
            <h1 style="margin:0;padding:0;font-size:2em;">{summary.get('BLOCKED')}</h1>
            <p style="margin:0;padding:0;font-size:1em;">Blocked</p>
          </div> 
            
          <div style="display:flex;flex-direction:column;align-items:center;justify-content:center;width:8rem;aspect-ratio:1;background-color:#fabb3d;gap:.5rem;border-radius:4px;box-shadow:1px 1px 5px lightgrey;">
            <h1 style="margin:0;padding:0;font-size:2em;">{summary.get('RETEST')}</h1>
            <p style="margin:0;padding:0;font-size:1em;">Retest</p>
          </div>
          
          <div style="display:flex;flex-direction:column;align-items:center;justify-content:center;width:8rem;aspect-ratio:1;background-color:#bebebe;gap:.5rem;border-radius:4px;box-shadow:1px 1px 5px lightgrey;">
            <h1 style="margin:0;padding:0;font-size:2em;">{summary.get('UNTESTED')}</h1>
            <p style="margin:0;padding:0;font-size:1em;">Untested</p>
          </div>
        </div>
    """

    body += f"""
        <h6 style="font-size:1.3em; margin:0; margin-bottom:.5rem;text-decoration:underline;">Execution Summary:</h6>
  
        {generate_device_table(device_count)}
    """
    body += """
    <p>
    If you have any questions, please reach out to:
    <h4 style="margin:0"><a href="mailto:IVY_LCG_SportsAutomationQA@entaingroup.com">IVY_LCG_SportsAutomationQA</a></h4>
      <br/>
    Thanks & Regards,
      <br/>
    Sportsbook Automation team
      <br/>
      <br/>
    </p>

    """
    print(body)

    with open('result.txt', 'w') as result:
        result.write(body)
        result.close()


def main():
    create_data_for_email()


if __name__ == '__main__':
    main()
