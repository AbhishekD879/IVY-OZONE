import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.virtual_sports
@vtest
class Test_C869697_TO_EDIT_Verify_Forecast__Tricast_Section_When_Market__Event_Becomes_Suspended(Common):
    """
    TR_ID: C869697
    NAME: [TO EDIT] Verify 'Forecast' / 'Tricast' Section When Market / Event Becomes Suspended
    DESCRIPTION: This test case verifies 'Forecast' / 'Tricast' sections when event/market becomes suspended for
    DESCRIPTION: *   Virtual Motorsports (Class ID 288)
    DESCRIPTION: *   Virtual Cycling (Class ID 290)
    DESCRIPTION: *   Virtul Horse Racing (Class ID 285)
    DESCRIPTION: *   Virtual Greyhound Racing (Class ID 286)
    DESCRIPTION: *   Virtual Grand National (Class ID 26604)
    DESCRIPTION: **JIRA Ticket** :
    DESCRIPTION: BMA-9397 'Extend Forecast and Tricast betting to Virtual Sports'
    PRECONDITIONS: User is logged in
    PRECONDITIONS: **NOTE:**
    PRECONDITIONS: Need to update according to the new design in BMA-43681, BMA-42906.
    """
    keep_browser_open = True

    def test_001_load_oxygen(self):
        """
        DESCRIPTION: Load Oxygen
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_go_to_the_virtual_racing_event_details_page(self):
        """
        DESCRIPTION: Go to the <Virtual Racing> event details page
        EXPECTED: Event details page is opened
        """
        pass

    def test_003_add_two_selections_from_the_same_market_to_the_bet_slip(self):
        """
        DESCRIPTION: Add two selections from the same market to the Bet Slip
        EXPECTED: Selections are added
        """
        pass

    def test_004_open_bet_slip(self):
        """
        DESCRIPTION: Open Bet Slip
        EXPECTED: Bet Slip is opened
        """
        pass

    def test_005_trigger_the_situationmarketstatuscodes_for_market_from_which_outcomes_are_added(self):
        """
        DESCRIPTION: Trigger the situation:
        DESCRIPTION: **marketStatusCode='S'** for market from which outcomes are added
        EXPECTED: Error message appear
        """
        pass

    def test_006_enter_stake_in_a_stake_field_for_forecast__tricast_bet_and_tap_bet_now_button(self):
        """
        DESCRIPTION: Enter stake in a stake field for forecast / tricast bet and tap 'Bet Now' button
        EXPECTED: *   Error message 'The Outcome/Market/Event Has Been Suspended' is shown in above corresponding single
        EXPECTED: *   Error message 'One or more of your selections are unavailable, please remove them to get new multiples' is shown above 'Bet Now' button
        EXPECTED: *   Bet is NOT placed
        EXPECTED: NOTE, the text of error message may vary. It depends on what comes from the server
        """
        pass

    def test_007_refresh_the_page(self):
        """
        DESCRIPTION: Refresh the page
        EXPECTED: 'Forecast / Tricast (n)' section disappear from the Bet Slip
        """
        pass

    def test_008_unsuspend_the_suspended_market_and_refresh_the_page(self):
        """
        DESCRIPTION: Unsuspend the suspended market and refresh the page
        EXPECTED: 'Forecast / Tricast (n)' section appear
        """
        pass

    def test_009_repeat_steps_3___8_with_suspended_event(self):
        """
        DESCRIPTION: Repeat steps #3 - 8 with suspended event
        EXPECTED: 
        """
        pass

    def test_010_repeat_steps__3___8_with_started_event(self):
        """
        DESCRIPTION: Repeat steps # 3 - 8 with started event
        EXPECTED: 
        """
        pass
