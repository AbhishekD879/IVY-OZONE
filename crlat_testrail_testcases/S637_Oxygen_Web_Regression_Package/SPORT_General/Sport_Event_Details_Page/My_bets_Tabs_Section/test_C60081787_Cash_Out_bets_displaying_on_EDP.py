import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.cash_out
@vtest
class Test_C60081787_Cash_Out_bets_displaying_on_EDP(Common):
    """
    TR_ID: C60081787
    NAME: Cash Out bets displaying on EDP
    DESCRIPTION: This test case verifies displaying Cashout available Bets on 'My Bets' tab on Event Details page
    PRECONDITIONS: *   User is logged in;
    PRECONDITIONS: *   User has placed Single and Multiple bets for different events with available cash out
    """
    keep_browser_open = True

    def test_001_navigate_to_my_bets_tab_on_event_details_page_of_first_event_with_placed_single_bet_with_available_cash_out(self):
        """
        DESCRIPTION: Navigate to 'My bets' tab on Event Details page of first event with placed **Single** bet with available cash out
        EXPECTED: * 'My Bets' tab is opened
        EXPECTED: * WS Cashout connection is established.
        EXPECTED: * List of bets placed is received in Cashout WS ONLY for current EventId
        """
        pass

    def test_002_verify_list_of_bets_is_displayed_according_to_the_list_of_bets_received_in_cashout_ws(self):
        """
        DESCRIPTION: Verify list of bets is displayed according to the list of bets received in Cashout WS
        EXPECTED: * Number of Bets received in Cashout WS corresponds to number of bets displaying on 'My Bets' tab
        EXPECTED: * WS request URL has related query parameter e.g. &eventId=10589545 to get next format:
        EXPECTED: wss://cashout-dev0.coralsports.dev.cloud.ladbrokescoral.com:8443/socket.io/?token=%tokenValue%&eventId=%eventIDofChosenEvent%
        EXPECTED: &EIO=3&transport=websocket
        """
        pass

    def test_003_navigate_to_my_bets_tab_on_event_details_page_of_first_event_with_placed_multiple_bet_with_available_cash_out(self):
        """
        DESCRIPTION: Navigate to 'My bets' tab on Event Details page of first event with placed **Multiple** bet with available cash out
        EXPECTED: * 'My Bets' tab is opened
        EXPECTED: * WS Cashout connection is established.
        EXPECTED: * List of bets placed is received in Cashout WS ONLY for current EventId
        """
        pass

    def test_004_repeat_step_2(self):
        """
        DESCRIPTION: Repeat step 2
        EXPECTED: Results are the same
        """
        pass

    def test_005_repeat_steps_1_2_for_single_and_multiple_bets_for_one_event(self):
        """
        DESCRIPTION: Repeat steps #1-2 for **Single** and **Multiple** bets for one event
        EXPECTED: Results are the same
        """
        pass
