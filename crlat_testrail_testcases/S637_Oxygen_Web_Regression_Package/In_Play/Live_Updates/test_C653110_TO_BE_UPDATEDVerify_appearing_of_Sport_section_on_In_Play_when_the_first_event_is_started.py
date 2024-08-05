import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.in_play
@vtest
class Test_C653110_TO_BE_UPDATEDVerify_appearing_of_Sport_section_on_In_Play_when_the_first_event_is_started(Common):
    """
    TR_ID: C653110
    NAME: [TO BE UPDATED]Verify appearing of <Sport> section on In-Play when the first event is started
    DESCRIPTION: First step - to be updated (and now the event is moved to In-Play without refresh)
    DESCRIPTION: This test case verifies appearing of <Sport> section on In-Play when the first event is started
    PRECONDITIONS: 1. Load Oxygen app
    PRECONDITIONS: 2. Navigate to 'In-Play' page from the Sports Menu Ribbon (for mobile/tablet) or 'Main Navigation' menu at the 'Universal Header' (for Desktop) and choose 'Watch Live' tab > 'Live Now' section/switcher
    PRECONDITIONS: 3. Make sure that Live events are present in 'Live Now' section (for mobile/tablet) or when 'Live Now' switcher is selected (for Desktop)
    PRECONDITIONS: 4. To reach upcoming events scroll the page down to 'Upcoming' section (for mobile/tablet) or select 'Upcoming' switcher (for Desktop)
    PRECONDITIONS: **Note:**
    PRECONDITIONS: * To check Live Serv notifications open Dev tools -> Network tab -> WS tab -> Frames section -> choose **?EIO=3&transport=websocket** record
    PRECONDITIONS: * Make sure that no events are present within tested Sport
    """
    keep_browser_open = True

    def test_001_start_new_event_within_sport_section_that_is_not_present_on_current_page(self):
        """
        DESCRIPTION: Start new event within <Sport> section that is not present on current page
        EXPECTED: 'IN_PLAY_STRUCTURE_CHANGED' record is sent with update and <Sport> is listed in its response
        """
        pass

    def test_002_verify_sport_displaying(self):
        """
        DESCRIPTION: Verify <Sport> displaying
        EXPECTED: <Sport> section appears at the bottom Live Now/Upcoming section in collapsed state disregarding it's Display Order
        """
        pass

    def test_003_refresh_page_or_navigate_between_tabs_and_back(self):
        """
        DESCRIPTION: Refresh page or navigate between tabs and back
        EXPECTED: Newly added <Sport> section changes it's position on the page taking into consideration **disporder** on category level
        """
        pass

    def test_004_repeat_steps_1_3_for_upcoming_section(self):
        """
        DESCRIPTION: Repeat steps 1-3 for 'Upcoming' section
        EXPECTED: 
        """
        pass

    def test_005_for_mobiletabletnavigate_to_homepage__in_play_tab_and_repeat_steps_1_4(self):
        """
        DESCRIPTION: **For Mobile/Tablet:**
        DESCRIPTION: Navigate to Homepage > 'In-Play' tab and repeat steps 1-4
        EXPECTED: 
        """
        pass
