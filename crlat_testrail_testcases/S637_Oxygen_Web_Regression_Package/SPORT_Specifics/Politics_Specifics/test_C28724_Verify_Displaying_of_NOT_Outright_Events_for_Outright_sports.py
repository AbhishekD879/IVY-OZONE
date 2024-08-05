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
class Test_C28724_Verify_Displaying_of_NOT_Outright_Events_for_Outright_sports(Common):
    """
    TR_ID: C28724
    NAME: Verify Displaying of NOT Outright Events for 'Outright' sports
    DESCRIPTION: This test case verifies how events which are NOT Outright will be displayed for 'Outright' sports
    DESCRIPTION: **Jira Tickets:** BMA-4680
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/XXX?translationLang=LL
    PRECONDITIONS: *   XXX - event ID
    PRECONDITIONS: *   X.XX - current supported version of OpenBet release
    PRECONDITIONS: *   LL - language (e.g. en, ukr)
    """
    keep_browser_open = True

    def test_001_load_invictus_application(self):
        """
        DESCRIPTION: Load Invictus application
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_tap_golf_icon_from_the_sports_menu_ribbon(self):
        """
        DESCRIPTION: Tap 'Golf' icon from the Sports Menu Ribbon
        EXPECTED: **Desktop:**
        EXPECTED: *   'Golf' Landing Page is opened
        EXPECTED: *   '**Today**' tab is opened by default
        EXPECTED: *   Two sorting type buttons are visible: 'By Competitions' and 'By Time'
        EXPECTED: *   'By Competitions' sorting type is selected by default
        EXPECTED: **Mobile:**
        EXPECTED: * Politics Landing Page (single view) is opened
        """
        pass

    def test_003_ask_the_uat_to_create_an_event_with_attributeseventsortcodemtchandordispsortnameis_positive_eg_dispsortname3wwith_needed_start_date_and_time(self):
        """
        DESCRIPTION: Ask the UAT to create an event with attributes **'eventSortCode'='MTCH' **AND/OR **dispSortName **is positive (e.g. dispSortName="3W")** **with needed start date and time
        EXPECTED: Event is created on Site Server
        """
        pass

    def test_004_refresh_the_page_and_verify_created_event(self):
        """
        DESCRIPTION: Refresh the page and verify created event
        EXPECTED: Created event IS displayed on event landing page
        """
        pass

    def test_005_verify_displaying_of_created_event(self):
        """
        DESCRIPTION: Verify displaying of created event
        EXPECTED: Event is shown as 'Outright' event
        EXPECTED: Event name and 'Show All' button are shown
        """
        pass

    def test_006_verify_show_all_button(self):
        """
        DESCRIPTION: Verify 'Show All' button
        EXPECTED: 'Show All' button leads to Event Details Page
        EXPECTED: Event details page is shown as Outright event details page
        """
        pass

    def test_007_tap_tomorrow_tab_desktop(self):
        """
        DESCRIPTION: Tap** 'Tomorrow'** tab (Desktop)
        EXPECTED: **'Tomorrow'** tab is opened
        """
        pass

    def test_008_repeatsteps__3___6(self):
        """
        DESCRIPTION: Repeat steps # 3 - 6
        EXPECTED: 
        """
        pass

    def test_009_tap_future_tab_desktop(self):
        """
        DESCRIPTION: Tap** 'Future'** tab (Desktop)
        EXPECTED: **'Future'** tab is opened
        """
        pass

    def test_010_repeat_steps__3___6(self):
        """
        DESCRIPTION: Repeat steps # 3 - 6
        EXPECTED: 
        """
        pass

    def test_011_tap_in_play_tab_desktop(self):
        """
        DESCRIPTION: Tap **'In-Play' **tab (Desktop)
        EXPECTED: **'In-Play'** tab is opened
        """
        pass

    def test_012_ask_the_uat_to_create_an_event_with_attributeeventsortcodemtchandordispsortnameis_positive_eg_dispsortname3w_and_all_needed_attributes_for_event_to_be_displayed_for_live_now_and_upcoming_sorting_types(self):
        """
        DESCRIPTION: Ask the UAT to create an event with attribute **'eventSortCode'='MTCH' **AND/OR **dispSortName **is positive (e.g. dispSortName="3W") and all needed attributes for event to be displayed for 'Live Now' and 'Upcoming' sorting types
        EXPECTED: Event is created on Site Server
        """
        pass

    def test_013_repeat_steps__4___6(self):
        """
        DESCRIPTION: Repeat steps # 4 - 6
        EXPECTED: 
        """
        pass

    def test_014_tap_in_play_icon_from_the_footer_menu(self):
        """
        DESCRIPTION: Tap** 'In-Play' **icon from the footer menu
        EXPECTED: 'In - Play' page is opened
        EXPECTED: 'All Sports' tab is selected
        """
        pass

    def test_015_repeat_steps__12___13_for_all_sports_and_sport_tabs(self):
        """
        DESCRIPTION: Repeat steps # 12 - 13 for 'All Sports' and <Sport> tabs
        EXPECTED: 
        """
        pass
