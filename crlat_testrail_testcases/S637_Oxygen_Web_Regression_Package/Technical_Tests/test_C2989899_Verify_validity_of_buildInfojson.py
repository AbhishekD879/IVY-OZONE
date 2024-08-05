import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.other
@vtest
class Test_C2989899_Verify_validity_of_buildInfojson(Common):
    """
    TR_ID: C2989899
    NAME: Verify validity of buildInfo.json
    DESCRIPTION: This test case verifies whether buildInfo.json file is generated correctly after application deployment
    PRECONDITIONS: 
    """
    keep_browser_open = True

    def test_001_navigate_to_url_httpsyour_environmentbuildinfojson_eg_httpsinvictuscoralcoukbuildinfojson(self):
        """
        DESCRIPTION: Navigate to URL: https://<<your_environment>>/buildInfo.json (e.g. https://invictus.coral.co.uk/buildInfo.json)
        EXPECTED: buildInfo.json file is present
        """
        pass

    def test_002_validate_json_file(self):
        """
        DESCRIPTION: Validate json file
        EXPECTED: buildInfo.json adheres to the JavaScript Object Notation specification
        """
        pass
