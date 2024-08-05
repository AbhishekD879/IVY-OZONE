import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.sports
@vtest
class Test_C28710_NOT_IMPLEMENTED_Verify_2_3_Balls_tab(Common):
    """
    TR_ID: C28710
    NAME: NOT IMPLEMENTED: Verify '2/3 Balls' tab
    DESCRIPTION: This test case verifies presence of '2/3 Balls' tab instead 'Matches' tab
    DESCRIPTION: **JIRA Tickets:**
    DESCRIPTION: BMA-12292: Golf - Rename Matches tab and remove duplicated content
    PRECONDITIONS: 
    """
    keep_browser_open = True

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_go_to_golf_page(self):
        """
        DESCRIPTION: Go to 'Golf' page
        EXPECTED: Golf Landing Page is opened
        """
        pass

    def test_003_verify_23_balls_tab_presence(self):
        """
        DESCRIPTION: Verify 2/3 Balls tab presence
        EXPECTED: *   '2/3 Balls' tab is shown instead 'Matches' tab
        EXPECTED: *   '2/3 Balls' tab is displayed after 'In-Play' tab
        EXPECTED: *   '2/3 Balls' tab is present for logged in and logged out users
        EXPECTED: *   '2/3 Balls' -> 'Today' page is opened by default
        """
        pass
