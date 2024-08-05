import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.races
@vtest
class Test_C1159141_Quick_access_to_the_virtual_races(Common):
    """
    TR_ID: C1159141
    NAME: Quick access to the virtual races
    DESCRIPTION: This test case verifies quick access for the virtual race module
    PRECONDITIONS: - Ordering of HR Inspired Virtual Carousel module is configured in CMS
    PRECONDITIONS: - Video starts on 1min20 sec earlier than event starts (Video starts = eventStartTime + 1min20 sec. )
    PRECONDITIONS: - "eventIsOff" time = 45 seconds after stream for an event is finished.
    PRECONDITIONS: - To get the Inspired Virtual events check modules ('Virtual Race Carousel' module, the name can be changed in CMS) in 'FEATURED_STRUCTURE_CHANGED' request from websocket (wss://featured-sports)
    PRECONDITIONS: Example of Virtual event structure:
    PRECONDITIONS: {
    PRECONDITIONS: id: "230549330",
    PRECONDITIONS: name: "Derby Downs",
    PRECONDITIONS: startTime: "2020-06-19T17:26:00Z",
    PRECONDITIONS: classId: "285"
    PRECONDITIONS: }
    PRECONDITIONS: - Amount of events in Inspired Virtual carousel can be set in CMS: Sports Pages-> Sport Categories -> Horse Racing/Greyhounds -> **'limit'** field
    PRECONDITIONS: Default value is 5, min is 1, max is 12 events.
    PRECONDITIONS: - Types and classes for Inspired Virtuals can be changed in CMS: Sports Pages-> Sport Categories -> Horse Racing/Greyhounds -> **'excludeTypeIDs'** and **'classId'** fields
    PRECONDITIONS: **'excludeTypeIDs' default values for different profiles are**:
    PRECONDITIONS: tst: ['3048', '3049', '3123'],
    PRECONDITIONS: stg: ['16576', '16575', '16602'],
    PRECONDITIONS: prod: ['28977', '28975', '29346']
    PRECONDITIONS: **'classId'** default value is **285** (for Horse Racing) and **286** (for Greyhounds)
    """
    keep_browser_open = True

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load Oxygen application
        EXPECTED: Oxygen application is loaded
        """
        pass

    def test_002_on_homepage_tap_horse_racing_icon_from_the_sports_menu_ribbon(self):
        """
        DESCRIPTION: On homepage tap 'Horse Racing' icon from the Sports Menu Ribbon
        EXPECTED: Horse Racing landing page is opened
        """
        pass

    def test_003_navigate_to_the_inspired_virtual_race_module(self):
        """
        DESCRIPTION: Navigate to the 'Inspired Virtual race' module
        EXPECTED: 'Inspired Virtual race' module is shown as Carousel module
        """
        pass

    def test_004_click_on_the_bet_now_link_of_a_meeting_card_with_available_count_down_timer(self):
        """
        DESCRIPTION: Click on the 'Bet Now' link of a meeting card with available count down timer
        EXPECTED: User is redirected to a corresponding event details on 'Inspired virtual' page
        """
        pass

    def test_005_go_back_to_hr_landing_page_gt_click_on_the_meeting_card_with_available_live_badge(self):
        """
        DESCRIPTION: Go back to HR landing page &gt; Click on the meeting card with available 'LIVE' badge
        EXPECTED: - User is redirected to a corresponding event details on 'Inspired virtual' page
        EXPECTED: -  If video stream of an event has already ended and "evenIsOff" time =45 sec (see preconditions) has not yet passed, warning message is shown on the red background on event details page: "Requested race is OFF and we propose to see the following:"
        """
        pass

    def test_006_go_back_to_hr_landing_page_gt_swipe_to_the_last_view_all_virtual_events_card_gt_tap_on_the__view_all_virtual_events_link(self):
        """
        DESCRIPTION: Go back to HR landing page &gt; Swipe to the last 'View all virtual events' card &gt; Tap on the  'View all virtual events' link
        EXPECTED: User is redirected to the 'Inspired virtual' page &gt; first available event details tab
        """
        pass
