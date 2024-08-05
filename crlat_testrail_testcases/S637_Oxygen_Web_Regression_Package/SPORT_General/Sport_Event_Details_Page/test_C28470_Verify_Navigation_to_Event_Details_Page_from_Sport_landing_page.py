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
class Test_C28470_Verify_Navigation_to_Event_Details_Page_from_Sport_landing_page(Common):
    """
    TR_ID: C28470
    NAME: Verify Navigation to Event Details Page from <Sport> landing page.
    DESCRIPTION: This test case verifies Navigation to Event Details Page from <Sport> landing page.
    PRECONDITIONS: Live and Pre Match events should be present
    """
    keep_browser_open = True

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_tapsporticon_from_the_sports_menu_ribbon(self):
        """
        DESCRIPTION: Tap '<Sport>' icon from the Sports Menu Ribbon
        EXPECTED: * <Sport> Landing Page is opened
        EXPECTED: * <Matches> tab ('Matches'/'Events'/'Races'/'Fights'/'Tournaments') ->'Today' tab on 'Today/Tomorrow/Future' Daily Switcher is opened by default (for desktop only)
        EXPECTED: * <Matches> tab ('Matches'/'Events'/'Races'/'Fights'/'Tournaments') with 'Today/Tomorrow' sub-headers for each league is opened by default (for mobile only)
        """
        pass

    def test_003_tapevent_name_on_the_event_section(self):
        """
        DESCRIPTION: Tap Event Name on the event section
        EXPECTED: <Sport> Event Details page is opened
        """
        pass

    def test_004_tap_on_eventdate_and_timeon_the_event_section(self):
        """
        DESCRIPTION: Tap on Event Date and Time on the event section
        EXPECTED: <Sport> Event Details page is opened
        """
        pass

    def test_005_tap_onstream_icon_on_the_event_section(self):
        """
        DESCRIPTION: Tap on Stream icon on the event section
        EXPECTED: <Sport> Event Details page is opened
        """
        pass

    def test_006_tap_onlive_text_on_the_event_section(self):
        """
        DESCRIPTION: Tap on LIVE text on the event section
        EXPECTED: <Sport> Event Details page is opened
        """
        pass

    def test_007_tap_on_any_remaining_blank_areas_of_window_on_the_event_section(self):
        """
        DESCRIPTION: Tap on any remaining blank areas of window on the event section
        EXPECTED: <Sport> Event Details page is opened
        """
        pass

    def test_008_go_to_matches_tab_matcheseventsracesfightstournaments__tomorrow_tab_on_todaytomorrowfuture_daily_switcher_and_repeat_steps_3_7_for_desktop_only(self):
        """
        DESCRIPTION: Go to <Matches> tab ('Matches'/'Events'/'Races'/'Fights'/'Tournaments') ->'Tomorrow' tab on 'Today/Tomorrow/Future' Daily Switcher and repeat steps 3-7 (for desktop only)
        EXPECTED: 
        """
        pass

    def test_009_go_tomatches_tab_eventsracesfightstournaments_future_tab_on_daily_switcher_and_repeat_steps_3_7_for_desktop_only(self):
        """
        DESCRIPTION: Go to 'Matches' tab ('Events'/'Races'/'Fights'/'Tournaments')->'Future' tab on Daily Switcher and repeat steps 3-7 (for desktop only)
        EXPECTED: 
        """
        pass

    def test_010_go_to_in_play_tab_and_repeat_steps_3_7(self):
        """
        DESCRIPTION: Go to 'In-Play' tab and repeat steps 3-7
        EXPECTED: 
        """
        pass

    def test_011_go_tocouponstaband_repeat_steps_3_7(self):
        """
        DESCRIPTION: Go to 'Coupons' tab and repeat steps 3-7
        EXPECTED: 
        """
        pass

    def test_012_go_tooutrightstaband_repeat_steps_3_7(self):
        """
        DESCRIPTION: Go to 'Outrights' tab and repeat steps 3-7
        EXPECTED: 
        """
        pass
