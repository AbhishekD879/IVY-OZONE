import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.races
@vtest
class Test_C1108084_Verify_SEE_ALL_Link(Common):
    """
    TR_ID: C1108084
    NAME: Verify ''SEE ALL' Link
    DESCRIPTION: This test case is for checking of 'View Full Race Card' link.
    DESCRIPTION: Need to run the test case on Mobile/Tablet/Desktop.
    PRECONDITIONS: 
    """
    keep_browser_open = True

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Homepage is loaded
        """
        pass

    def test_002__for_ladbrokes_navigate_to_horse_racing_landing_pageclick_on_next_races_tab(self):
        """
        DESCRIPTION: ** FOR LADBROKES **
        DESCRIPTION: Navigate to 'Horse Racing' Landing page
        DESCRIPTION: Click on Next races tab
        EXPECTED: * 'Horse Racing' landing page is loaded
        EXPECTED: * 'Featured' tab is opened by default
        EXPECTED: * 'Next Races' section is shown
        """
        pass

    def test_003_on_next_races_module_find_see_all_link(self):
        """
        DESCRIPTION: On 'Next Races' module find 'SEE ALL' link
        EXPECTED: * 'SEE ALL' is displayed for each event in 'Next Races' module
        EXPECTED: * Link is displayed at the top right corner of the section
        EXPECTED: * Link is aligned to the right
        EXPECTED: * Text is hyperlinked
        """
        pass

    def test_004_clicktap_see_all_link(self):
        """
        DESCRIPTION: Click/Tap 'SEE ALL' link
        EXPECTED: The event's details page is opened.
        """
        pass

    def test_005_clicktap_back_button(self):
        """
        DESCRIPTION: Click/Tap 'Back' button
        EXPECTED: The previously visited page is opened
        """
        pass

    def test_006_for_coral__ladbrokesnavigate_to_home_page__next_races_tab(self):
        """
        DESCRIPTION: **For CORAL & LADBROKES**
        DESCRIPTION: Navigate to Home page > Next races tab
        EXPECTED: **For CORAL& LADBROKES**
        EXPECTED: 'Next Races' section is shown
        """
        pass

    def test_007_for_coral__ladbrokesrepeat_steps__3___5(self):
        """
        DESCRIPTION: **For CORAL & LADBROKES**
        DESCRIPTION: Repeat steps # 3 - 5
        EXPECTED: 
        """
        pass
