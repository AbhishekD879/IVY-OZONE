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
class Test_C1049081_Verify_Navigation_to_the_Event_Details_Page_from_Featured_tab(Common):
    """
    TR_ID: C1049081
    NAME: Verify Navigation to the Event Details Page from Featured tab
    DESCRIPTION: This test case verifies how a user can get to the event details page for <Horse Racing> sport type
    DESCRIPTION: Applies to mobile, tablet & desktop
    DESCRIPTION: AUTOTEST: [C1501651]
    DESCRIPTION: AUTOTEST: [C1792286]
    PRECONDITIONS: For checking info regarding event use the following link:
    PRECONDITIONS: http://backoffice-tst2.coral.co.uk/openbet-ssviewer/Drilldown/X.XX/EventToOutcomeForEvent/ZZZZ
    PRECONDITIONS: where,
    PRECONDITIONS: X.XX - currently supported version of OpenBet release
    PRECONDITIONS: ZZZZ - an event id
    """
    keep_browser_open = True

    def test_001_tap_on_horse_racing_icon_from_the_sports_menu_ribbon(self):
        """
        DESCRIPTION: Tap on 'Horse Racing' icon from the Sports Menu Ribbon
        EXPECTED: * 'Horse Racing' landing page is opened.
        EXPECTED: * Featured tab is opened by default
        """
        pass

    def test_002_go_to_the_event_details_page_by_tapping_event_off_time_from_the_event_off_time_ribbon(self):
        """
        DESCRIPTION: Go to the Event details page by tapping event off time from the event off time ribbon
        EXPECTED: Event details page is opened
        """
        pass

    def test_003_go_to_the_event_details_page_from_the_next_4_module_by_tapping_view_full_race_card_link(self):
        """
        DESCRIPTION: Go to the event details page from the 'Next 4' module by tapping 'View Full race Card' link
        EXPECTED: Event details page is opened
        """
        pass

    def test_004_on_event_details_page_tap_another_event_off_time(self):
        """
        DESCRIPTION: On event details page tap another event off time
        EXPECTED: Event details page for other event is opened
        """
        pass

    def test_005_go_back_to_landing_page__scroll_to_the_race_grid_accordion_where_day_switchers_are_available(self):
        """
        DESCRIPTION: Go back to landing page > scroll to the Race Grid accordion where day switchers are available
        EXPECTED: Day switcher name is day of the week
        """
        pass

    def test_006_go_to_the_event_details_page_from_next_day_switcher_by_tapping_event_off_time_from_the_event_off_time_ribbon(self):
        """
        DESCRIPTION: Go to the Event details page from next Day switcher by tapping event off time from the event off time ribbon
        EXPECTED: Event details page is opened
        """
        pass
