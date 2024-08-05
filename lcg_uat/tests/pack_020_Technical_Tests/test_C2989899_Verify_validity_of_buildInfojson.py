from json import JSONDecodeError

import pytest
import json
import tests
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.desktop
@pytest.mark.high
@pytest.mark.safari
@pytest.mark.other
@vtest
class Test_C2989899_Verify_validity_of_buildInfojson(Common):
    """
    TR_ID: C2989899
    NAME: Verify validity of buildInfo.json
    DESCRIPTION: This test case verifies whether buildInfo.json file is generated correctly after application deployment
    """
    keep_browser_open = True

    def test_001_navigate_to_url_your_environment_buildinfojson(self):
        """
        DESCRIPTION: Navigate to URL: https://<<your_environment>>/buildInfo.json
        DESCRIPTION: (e.g. https://invictus.coral.co.uk/buildInfo.json)
        EXPECTED: buildInfo.json file is present
        """
        self.device.navigate_to(f'{tests.HOSTNAME}/buildInfo.json')
        build_info_json = self.site.build_info_json_page.get_json_content()
        self.assertTrue(build_info_json, msg='Text content on buildInfo.json is not present')

    def test_002_validate_json_file(self):
        """
        DESCRIPTION: Validate json file
        EXPECTED: buildInfo.json adheres to the JavaScript Object Notation specification
        """
        build_info_json = self.site.build_info_json_page.get_json_content()
        try:
            result = json.loads(build_info_json)
        except JSONDecodeError as e:
            self._logger.warn(e)
            result = None
        self.assertTrue(result, msg='buildInfo.json is not JSON serializable')
