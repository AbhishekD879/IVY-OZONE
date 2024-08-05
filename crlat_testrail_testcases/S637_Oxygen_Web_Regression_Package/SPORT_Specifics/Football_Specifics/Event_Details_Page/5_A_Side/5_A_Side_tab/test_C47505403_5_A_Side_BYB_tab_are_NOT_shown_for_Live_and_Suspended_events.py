import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.build_your_bet
@vtest
class Test_C47505403_5_A_Side_BYB_tab_are_NOT_shown_for_Live_and_Suspended_events(Common):
    """
    TR_ID: C47505403
    NAME: '5-A-Side'/BYB tab are NOT shown for Live and Suspended events
    DESCRIPTION: This test case verifies that '5-A-Side' and BYB tabs are NOT shown for Live and Suspended events
    PRECONDITIONS: **5-A-Side config:**
    PRECONDITIONS: - Feature is enabled in CMS > System Configuration -> Structure -> FiveASide
    PRECONDITIONS: - Banach leagues are added and enabled for 5-A-Side in CMS -> BYB -> Banach Leagues -> select league -> ‘Active for 5 A Side’ is ticked
    PRECONDITIONS: - Event under test is mapped on Banach side and created in OpenBet (T.I) (‘events’ request to Banach should return event under test)
    PRECONDITIONS: - 'Player Bets' market data is provided by Banach ("hasPlayerProps: true" is returned in .../events/{event_id} response)
    PRECONDITIONS: - Event is prematch (not live)
    PRECONDITIONS: **FE removes '5-A-Side'/BYB tabs based on the event status sent from Banach [status: 0 (event is suspended) and status: 2 (event is live)]:**
    PRECONDITIONS: To check status for Banach event see query https://buildyourbet-prd0.coralsports.prod.cloud.ladbrokescoral.com/api/v1/events/event_id
    PRECONDITIONS: ![](index.php?/attachments/get/48623426)
    PRECONDITIONS: Use Charles tool to edit response i.e. change status from 1 to 2 and 0 in https://buildyourbet-prd0.coralsports.prod.cloud.ladbrokescoral.com/api/v1/events/event_id
    PRECONDITIONS: **Steps:**
    PRECONDITIONS: 1. Load the app
    PRECONDITIONS: 2. Navigate to the prematch event details page where '5-A-Side' tab is available
    """
    keep_browser_open = True

    def test_001_open_5_a_side_or_byb_tab_before_event_goes_live(self):
        """
        DESCRIPTION: Open '5-A-Side' or BYB tab before event goes Live
        EXPECTED: Status parameter from the feed provider equals 1.
        """
        pass

    def test_002_wait_on_edp_until_event_goes_live_status_parameter_from_the_feed_provider_equals_2_and_perform_page_refresh(self):
        """
        DESCRIPTION: Wait on EDP until event goes live (status parameter from the feed provider equals 2) and perform page refresh
        EXPECTED: '5-A-Side'/BYB tabs are removed from the UI when status code 2 is received in the response
        """
        pass

    def test_003_wait_on_edp_until_event_gets_suspended_status_parameter_from_the_feed_provider_equals_0_and_perform_page_refresh(self):
        """
        DESCRIPTION: Wait on EDP until event gets suspended (status parameter from the feed provider equals 0) and perform page refresh
        EXPECTED: '5-A-Side'/BYB tabs are removed from the UI when status code 0 is received in the response
        """
        pass

    def test_004_from_matches_tab_on_football_open_the_event_with_banach_which_is_live_or_suspended(self):
        """
        DESCRIPTION: From Matches tab on Football open the event with Banach which is live or suspended
        EXPECTED: When event is opened '5-A-Side'/BYB tabs are not shown
        """
        pass
