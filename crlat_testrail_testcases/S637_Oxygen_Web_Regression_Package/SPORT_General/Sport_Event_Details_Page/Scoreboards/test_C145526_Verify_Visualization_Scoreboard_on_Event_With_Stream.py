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
class Test_C145526_Verify_Visualization_Scoreboard_on_Event_With_Stream(Common):
    """
    TR_ID: C145526
    NAME: Verify Visualization Scoreboard on Event With Stream
    DESCRIPTION: This test case verifies correctness of Visualisations Scoreboard  displaying after Watching Stream on Event details page
    PRECONDITIONS: Video is mapped :
    PRECONDITIONS: 1. SiteServer event should be configured to support Perform streaming (**'typeFlagCodes'**='PVA , ... ' AND **'drilldownTagNames'**='EVFLAG_PVM' flags should be set) and should be mapped to Perform stream event
    PRECONDITIONS: 2. Event should have the following attributes:  isStarted = "true",  isMarketBetInRun = "true"
    PRECONDITIONS: **NOTES:**
    PRECONDITIONS: * You can find how to map a stream to an event here: https://confluence.egalacoral.com/display/SPI/How+to+Map+Video+Streams+to+Events
    PRECONDITIONS: *   In order to get Visualisation scoreboard mapped use mapper tool (for Football and Tennis): https://coral-vis-rtc-tst2.symphony-solutions.eu/#/sports/tennis/provider/img/tournaments/all/events?_k=8ikbly (TST2 and Invictus)
    """
    keep_browser_open = True

    def test_001_load_invictus_application(self):
        """
        DESCRIPTION: Load Invictus application
        EXPECTED: 
        """
        pass

    def test_002_open_event_details_page_of_any_sport_for_the_event_which_satisfies_preconditions(self):
        """
        DESCRIPTION: Open Event Details page of any <Sport> for the event which satisfies Preconditions
        EXPECTED: * VIS Scoreboard is displayed correctly
        """
        pass

    def test_003_login_with_credentials_with_positive_balance(self):
        """
        DESCRIPTION: Login with credentials with positive balance
        EXPECTED: 
        """
        pass

    def test_004_open_event_details_page_of_any_sport_for_the_event_which_satisfies_preconditions(self):
        """
        DESCRIPTION: Open Event Details page of any <Sport> for the event which satisfies Preconditions
        EXPECTED: * VIS Scoreboard is displayed correctly
        EXPECTED: * 'Watch Live' tab is displayed
        """
        pass

    def test_005_tap_watch_live_tab(self):
        """
        DESCRIPTION: Tap 'Watch Live' tab
        EXPECTED: Stream is launched
        """
        pass

    def test_006_pause_stream_and_tap_stop_tab(self):
        """
        DESCRIPTION: Pause stream and tap 'Stop' tab
        EXPECTED: * Stream is stopped and collapsed
        EXPECTED: * VIS Scoreboard is displayed correctly
        """
        pass

    def test_007_tap_watch_live_tab(self):
        """
        DESCRIPTION: Tap 'Watch Live' tab
        EXPECTED: Stream is launched
        """
        pass

    def test_008_rotate_device_to_portraitelandscape_mode(self):
        """
        DESCRIPTION: Rotate device to Portraite/Landscape mode
        EXPECTED: Stream is performing
        """
        pass

    def test_009_pause_stream_and_tap_stop_tab(self):
        """
        DESCRIPTION: Pause stream and tap 'Stop' tab
        EXPECTED: * Stream is stopped and collapsed
        EXPECTED: * VIS Scoreboard is displayed correctly
        """
        pass

    def test_010_repeat_steps_2_10_for_the_following_sports_football_tennis_basketball_darts_snooker_cricket_rugby_nhl(self):
        """
        DESCRIPTION: Repeat steps ##2-10 for the following sports:
        DESCRIPTION: * Football
        DESCRIPTION: * Tennis
        DESCRIPTION: * Basketball
        DESCRIPTION: * Darts
        DESCRIPTION: * Snooker
        DESCRIPTION: * Cricket
        DESCRIPTION: * Rugby
        DESCRIPTION: * NHL
        EXPECTED: 
        """
        pass
