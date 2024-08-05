import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.in_play
@vtest
class Test_C331554_Verify_remember_last_Sport_functionality_on_In_Play_page_for_Logged_Out_user(Common):
    """
    TR_ID: C331554
    NAME: Verify remember last Sport functionality on In-Play page for Logged Out user
    DESCRIPTION: This test case verifies remember last Sport functionality on In-Play page for Logged Out user
    DESCRIPTION: To be run on mobile, tablet and desktop.
    PRECONDITIONS: 1. User should be logged out
    """
    keep_browser_open = True

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: 
        """
        pass

    def test_002_go_to_in_play_page(self):
        """
        DESCRIPTION: Go to In-Play page
        EXPECTED: * 'In-Play' Landing Page is opened
        EXPECTED: * First <Sport> tab is opened by default
        EXPECTED: * Two sections are visible: 'Live Now' and 'Upcoming'
        """
        pass

    def test_003_choose_any_sports_icon(self):
        """
        DESCRIPTION: Choose any Sports icon
        EXPECTED: * Selected Sports tab is underlined by red line
        EXPECTED: * The appropriate content is displayed for selected Sports
        """
        pass

    def test_004_navigate_across_application(self):
        """
        DESCRIPTION: Navigate across application
        EXPECTED: 
        """
        pass

    def test_005_back_to_in_play_page(self):
        """
        DESCRIPTION: Back to In-Play page
        EXPECTED: * 'In-Play' Landing Page is opened
        EXPECTED: * First <Sport> tab is opened by default and underlined by red line
        EXPECTED: * Two sections are visible: 'Live Now' and 'Upcoming'
        """
        pass
