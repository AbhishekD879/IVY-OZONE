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
class Test_C1274044_Verify_Watch_Free_Information_not_displayed(Common):
    """
    TR_ID: C1274044
    NAME: Verify Watch Free Information-not displayed
    DESCRIPTION: Verify Watch Free Information is no longer displayed in both the brands
    PRECONDITIONS: **Jira tickets: **
    PRECONDITIONS: *   BMA-17787 Live Sim/Watch Free Display Change for Information Pop Up
    PRECONDITIONS: *   BMA-19409 Change the wording in the QL Watch Free Pop Up
    PRECONDITIONS: *   Applicaiton is loaded
    PRECONDITIONS: *   Horse Racing Landing page is opened
    PRECONDITIONS: *   Make sure there is mapped race visualization for tested event
    PRECONDITIONS: *   Quantum Leap/Live Sim product is displayed only when it's available based on CMS configs (Log in to CMS and navigate to 'System-configuration' -> 'Config'/'Structure' tab (Coral and Ladbrokes) -> 'QuantumLeapTimeRange')
    PRECONDITIONS: **NOTE**: It event attribute **'typeFlagCodes' **contains 'UK' or 'IE' parameter, this event is included in the group 'UK & IRE'.
    PRECONDITIONS: **NOTE**: not all UK&IRE races can have LiveSim visuaisation mapped by Quantum Leap. If event is present in this feed then it should have QL LiveSim mapped: http://xmlfeeds-tst2.coral.co.uk/oxi/pub?template=getEvents&class=223
    """
    keep_browser_open = True

    def test_001_load_oxygen_app(self):
        """
        DESCRIPTION: Load Oxygen app
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_tap_horse_racing_icon_from_the_sports_menu_ribbon(self):
        """
        DESCRIPTION: Tap <Horse Racing> icon from the Sports Menu Ribbon
        EXPECTED: Horse Racing landing page is opened
        """
        pass

    def test_003_go_to_the_event_details_page_with_race_visualization_mapping(self):
        """
        DESCRIPTION: Go to the event details page with race visualization mapping
        EXPECTED: 
        """
        pass

    def test_004_navigate_to_media_area(self):
        """
        DESCRIPTION: Navigate to media area
        EXPECTED: **For mobile&tablet:**
        EXPECTED: * Twо buttons 'PRE-PARADE' and 'WATCH' are displayed and inActive
        EXPECTED: **For desktop:**
        EXPECTED: * Twо switchers 'PRE-PARADE' and 'WATCH' are displayed and inActive
        """
        pass

    def test_005_tap_inactive_pre_parade_button_and_verify_that_watch_free_text_is_no_longer_displayed(self):
        """
        DESCRIPTION: Tap inActive 'PRE-PARADE' button and verify that Watch free text is no longer displayed
        EXPECTED: *   The area below 'PRE-PARADE' button is expanded
        EXPECTED: *   'PRE-PARADE' button becomes Active
        EXPECTED: *   Visualisation video object is shown
        """
        pass
