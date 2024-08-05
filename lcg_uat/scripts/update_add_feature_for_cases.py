import os
import fileinput

from crlat_testrail_integration.testrail import TestRailAPIClient
from crlat_testrail_integration.utils.exceptions import TestRailAPIError

root = './../tests/'

TR = TestRailAPIClient()


FEATURE_MAP = {1: 'User Account',
               2: 'Betslip',
               3: 'Quick Bet',
               4: 'Bet History/Open Bets',
               5: 'Cash Out',
               6: 'Navigation',
               7: 'Sports',
               8: 'Races',
               9: 'In-Play',
               10: 'Streaming',
               11: 'Build Your Bet',
               12: 'Lotto',
               13: 'Virtual Sports',
               14: 'Retail',
               15: 'Featured',
               16: 'Promotions/Banners/Offers',
               17: 'Other'}

for path, subdirs, files in os.walk(root):
    for name in files:
        if name.startswith('test_') and name.endswith('.py'):
            file_path = os.path.join(path, name)
            print(file_path)

            s = open(file_path)
            line_with_test_rail_manual_id = next((line for line in s if 'TR_ID' in line), None)
            s.close()
            if not line_with_test_rail_manual_id:
                continue
            try:
                test_case_id = TR.get_testcase_id(string=line_with_test_rail_manual_id)
            except Exception:
                continue
            try:
                feature_id = TR.get_case(case_id=test_case_id).get('custom_feature')
            except (Exception, TestRailAPIError):
                feature_id = None
            if not feature_id:
                continue
            feature_name = FEATURE_MAP.get(feature_id).replace(' ', '_').replace('-', '_').replace('/', '_').lower()

            pytest_feature = f'@pytest.mark.{feature_name}'

            s = open(file_path)
            pytest_feature_presence = next((True for line in s if pytest_feature in str(line).strip()), None)
            s.close()
            if pytest_feature_presence:
                continue

            # print(s)
            for line in fileinput.FileInput(file_path, inplace=True):
                if str(line).strip().startswith('@vtest'):
                    line2 = pytest_feature
                    print(pytest_feature + '\n' + line.replace('\n', ''))
                else:
                    print(line.replace('\n', ''))
            print('')
