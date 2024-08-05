import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.other
@vtest
class Test_C29466_Verify_number_of_sport_category_requests(Common):
    """
    TR_ID: C29466
    NAME: Verify number of 'sport-category' requests
    DESCRIPTION: This test case verify number of 'sport-category' requests
    DESCRIPTION: **JIRA Tickets:**
    DESCRIPTION: BMA-10743 - We have noticed a duplicate call to sport-category, please investigate and remove the extra call
    PRECONDITIONS: For checking number of calls open Dev Tool->Network->sport-category
    """
    keep_browser_open = True

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Home page is opened
        """
        pass

    def test_002_open_dev_tool_network(self):
        """
        DESCRIPTION: Open Dev Tool->Network
        EXPECTED: Dev Tool is opened
        """
        pass

    def test_003_verifysport_category_request(self):
        """
        DESCRIPTION: Verify 'sport-category' request
        EXPECTED: *   'sport-category' request is sent only two times on mobile and tablet
        EXPECTED: *   'sport-category' request is sent only three times on desktop
        """
        pass
