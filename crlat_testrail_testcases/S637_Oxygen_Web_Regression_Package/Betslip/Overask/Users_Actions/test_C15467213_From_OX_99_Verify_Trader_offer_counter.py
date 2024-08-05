import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.betslip
@vtest
class Test_C15467213_From_OX_99_Verify_Trader_offer_counter(Common):
    """
    TR_ID: C15467213
    NAME: [From OX 99] Verify Trader offer counter
    DESCRIPTION: This test case verifies Offer expires counter
    PRECONDITIONS: * User is logged in
    PRECONDITIONS: * User's balance is more that allowed Max stake value
    PRECONDITIONS: ![](index.php?/attachments/get/31369)
    PRECONDITIONS: ![](index.php?/attachments/get/31370)
    """
    keep_browser_open = True

    def test_001_add_selection_and_go_to_betslip(self):
        """
        DESCRIPTION: Add selection and go to Betslip
        EXPECTED: 
        """
        pass

    def test_002_enter_a_value_in_stake_field_that_exceeds_max_allowed_bet_limit_for_particular_selection_and_clicktap_place_bet_button(self):
        """
        DESCRIPTION: Enter a value in 'Stake' field that exceeds max allowed bet limit for particular selection and click/tap 'Place bet' button
        EXPECTED: * The bet is sent to Openbet system for review
        """
        pass

    def test_003_verify_betslip(self):
        """
        DESCRIPTION: Verify Betslip
        EXPECTED: * Overask overlay appears
        """
        pass

    def test_004_trigger_offer_with_the_max_bet_by_a_trader_in_openbet_system(self):
        """
        DESCRIPTION: Trigger offer with the max bet by a trader in OpenBet system
        EXPECTED: * Confirmation is sent and received in Oxygen app
        """
        pass

    def test_005_verify_betslip(self):
        """
        DESCRIPTION: Verify Betslip
        EXPECTED: *   Selection with the maximum bet offer is expanded
        EXPECTED: *   The maximum bet offer for selected on step #2 bet and [X] remove button is shown to the user
        EXPECTED: *   Message 'Sorry your bet has not gone through, we are offering you the following bet as an alternative' appears on the grey background above the selection
        EXPECTED: *   **Expire counter appears**
        EXPECTED: * **readBet** response **offerExpiresAt: “timestamp”** **where timestamp** is **“2019-07-08T13:16:55.000+01:00” e.g** date when the offer is expired
        EXPECTED: *   'Place Bet  and 'Cancel' buttons are present
        EXPECTED: *   'Place Bet  and 'Cancel' buttons are enabled
        """
        pass

    def test_006_close_betslip_by_close_button_x(self):
        """
        DESCRIPTION: Close betslip by close button [X]
        EXPECTED: Betslip is closed
        """
        pass

    def test_007_open_betslip_again(self):
        """
        DESCRIPTION: Open betslip again
        EXPECTED: * Betslip is opened
        EXPECTED: * Selection is displayed
        EXPECTED: * Counter displayed correctly
        """
        pass

    def test_008_wait_for_the_counter_is_ended_000(self):
        """
        DESCRIPTION: Wait for the counter is ended (0:00)
        EXPECTED: The trader offer is expired, betslip is changed to (look at the design for Coral and Ladbrokes):
        EXPECTED: *   'Place Bet' button is present
        EXPECTED: *   'Place Bet' button is disabled
        EXPECTED: *  For Ladbrokes  **Your offer has expired** text appears on the top and on the bottom.
        EXPECTED: *  For Coral - **Your offer has expired** text appears only on the bottom.
        """
        pass

    def test_009_repeat_steps_1_7(self):
        """
        DESCRIPTION: Repeat steps 1-7
        EXPECTED: 
        """
        pass

    def test_010_tap_place_bet_button_to_accept_traders_offer(self):
        """
        DESCRIPTION: Tap "Place bet" button to accept Trader's offer
        EXPECTED: * Accepted bet is successfully placed
        EXPECTED: * Bet receipt is displayed
        """
        pass
