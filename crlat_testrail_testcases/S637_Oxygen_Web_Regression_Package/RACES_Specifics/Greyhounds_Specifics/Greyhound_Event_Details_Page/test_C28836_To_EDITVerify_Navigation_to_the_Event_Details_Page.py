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
class Test_C28836_To_EDITVerify_Navigation_to_the_Event_Details_Page(Common):
    """
    TR_ID: C28836
    NAME: [To EDIT]Verify Navigation to the Event Details Page
    DESCRIPTION: This test case verifies how user can get to the event details page for Greyhounds sport type
    PRECONDITIONS: 
    """
    keep_browser_open = True

    def test_001_load_invictus_application(self):
        """
        DESCRIPTION: Load Invictus application
        EXPECTED: 
        """
        pass

    def test_002_tap_greyhounds_icon_from_the_sports_menu_ribbon(self):
        """
        DESCRIPTION: Tap 'Greyhounds' icon from the sports menu ribbon
        EXPECTED: 'Greyhounds' the landing page is opened
        """
        pass

    def test_003_select_today_tab_by_meeting_sorting_type(self):
        """
        DESCRIPTION: Select 'Today' tab, 'By Meeting' sorting type
        EXPECTED: 'Today' tab is selected
        """
        pass

    def test_004_go_to_the_event_details_page_by_tapping_event_off_time_from_the_event_off_time_ribbon(self):
        """
        DESCRIPTION: Go to the event details page by tapping event off time from the event off time ribbon
        EXPECTED: Event details page is opened
        """
        pass

    def test_005_on_event_details_page_tap_another_event_off_time(self):
        """
        DESCRIPTION: On event details page tap another event off time
        EXPECTED: Event details page for other event is opened
        """
        pass

    def test_006_select_today_tab_by_time_sorting_type(self):
        """
        DESCRIPTION: Select 'Today' tab, 'By Time' sorting type
        EXPECTED: 'By Time' sorting type is selected
        """
        pass

    def test_007_go_to_the_event_details_page_by_tapping_event_name(self):
        """
        DESCRIPTION: Go to the event details page by tapping event name
        EXPECTED: Event details page is opened
        """
        pass

    def test_008_verify_steps__3___7_for_tomorrow_tab(self):
        """
        DESCRIPTION: Verify steps # 3 - 7 for 'Tomorrow' tab
        EXPECTED: Step #5 should be skipped for 'Tomorrow' tab
        """
        pass
