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
class Test_C8146835_Verify_Bet_history_for_pending_bets(Common):
    """
    TR_ID: C8146835
    NAME: Verify Bet history for pending bets
    DESCRIPTION: This test case verifies triggered pending bets by overask functionality are not displayed in bet History
    DESCRIPTION: MESSAGES TO BE UPDATED
    PRECONDITIONS: To retrieve *bet status* value check Network tab: **accountHistory** request -> bet ->stake -> status
    PRECONDITIONS: 1.User is logged in to application
    PRECONDITIONS: 2.Overask functionality is enabled for the user
    """
    keep_browser_open = True

    def test_001_add_selection_and_go_betslip_singles_section(self):
        """
        DESCRIPTION: Add selection and go Betslip, 'Singles' section
        EXPECTED: 
        """
        pass

    def test_002_enter_value_in_stake_field_that_exceeds_max_allowed_bet_limit_for_particular_selection_and_click__tap_bet_now_button(self):
        """
        DESCRIPTION: Enter value in 'Stake' field that exceeds max allowed bet limit for particular selection and click / tap 'Bet Now' button
        EXPECTED: The bet is sent to Openbet system for review
        """
        pass

    def test_003_verify_betslip(self):
        """
        DESCRIPTION: Verify Betslip
        EXPECTED: - 'Please wait, your bet is being reviewed by one of our Traders'This normally takes less than a minute.' message is displayed on yellow background above 'Bet now' button
        EXPECTED: - Loading spinner is displayed on the green button, replacing - 'Bet Now' label
        EXPECTED: - 'Stake', 'Est. Returns' fields, Quick Stake, 'Clear Betslip' and - - 'Bet Now' buttons are disabled and greyed out
        """
        pass

    def test_004_wait_till_the_referred_bet_to_trader_times_out_or_offered_bet_times_out_at_customer_side(self):
        """
        DESCRIPTION: Wait till the referred bet to trader times out or offered bet times out at customer side
        EXPECTED: - Bet is not placed
        EXPECTED: - "One or more of your bets have been declined" message is displayed on yellow background
        EXPECTED: - "Continue" button are active
        """
        pass

    def test_005_tap_continue_button(self):
        """
        DESCRIPTION: Tap "Continue" button
        EXPECTED: - Betslip page is closed
        """
        pass

    def test_006_navigate_to_bet_history(self):
        """
        DESCRIPTION: Navigate to Bet history
        EXPECTED: - Pending bets ( **status as "P"** in request) are not displayed in Bet History
        """
        pass
