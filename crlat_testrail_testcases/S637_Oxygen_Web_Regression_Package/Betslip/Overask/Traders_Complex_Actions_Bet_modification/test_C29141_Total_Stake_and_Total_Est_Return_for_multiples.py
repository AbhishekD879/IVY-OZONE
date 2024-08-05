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
class Test_C29141_Total_Stake_and_Total_Est_Return_for_multiples(Common):
    """
    TR_ID: C29141
    NAME: Total Stake and Total Est. Return for multiples
    DESCRIPTION: This test case verifies that 'Total stake' and 'Total Est. Returns' updates with new value after selection and deselection of modified bets
    DESCRIPTION: Jira ticket:
    DESCRIPTION: BMA-9500 Overask - Total Est. Return and Total stake Update after bet interception
    DESCRIPTION: BMA-20390 New Betslip - Overask design improvements
    PRECONDITIONS: 1. Load Oxygen application and login ( OverAsk is enabled for user)
    PRECONDITIONS: 2. Add to betslip 3 bets from different events
    PRECONDITIONS: 3. Open Dev Tools -> Network -> XHR tab in order to check 'readBet' response
    """
    keep_browser_open = True

    def test_001____enter_higher_than_maximum_allowed_stake_for_2_bets___enter_lower_than_maximum_allowedstake_for_1_bet___enter_higher_and_lower_than_maximum_allowedstake_for_multiples___select_bet_now_button(self):
        """
        DESCRIPTION: *   Enter higher than maximum allowed stake  for 2 bets
        DESCRIPTION: *   Enter lower than maximum allowed stake for 1 bet
        DESCRIPTION: *   Enter  higher and lower than maximum allowed stake for multiples
        DESCRIPTION: *   Select 'Bet Now' button
        EXPECTED: *   OverAsk is triggered.
        EXPECTED: *   Message is shown for user: 'Please wait, your bet is being reviewed by one of our Traders. This normally takes less than a minute.'
        """
        pass

    def test_002____in_backoffice_modify_stake_values_and_confirm_offer(self):
        """
        DESCRIPTION: *   In backoffice modify stake values and confirm offer
        EXPECTED: *   Message is shown "Please wait, your bet is being reviewed by one of our Traders. This normally takes less than a minute."
        """
        pass

    def test_003_check_offer_appears_in_bet_slip_in_oxygen_app(self):
        """
        DESCRIPTION: Check offer appears in Bet Slip in Oxygen app
        EXPECTED: *   Modified stake value is displayed in red stake box
        EXPECTED: *   Modified bets are unselected and checkbox is available
        EXPECTED: *   'Total Stake' is counted and displayed for selected bets (that were not modified)
        """
        pass

    def test_004_verify_est_returns_value(self):
        """
        DESCRIPTION: Verify 'Est. Returns' value
        EXPECTED: *   'Est. Returns' value corresponds to **bet.[i].payout.potential** attribute from **readBet** response,
        EXPECTED: where **i** is taken from the object where **isOffer="Y"**
        EXPECTED: * The 'Est. return' value is equal to **N/A** if no attribute is returned
        EXPECTED: * The 'Est. return' value is highlighted in red
        """
        pass

    def test_005_select_few_offers_and_check_total_stake_and_total_est_return_values(self):
        """
        DESCRIPTION: Select few offers and check 'Total Stake' and 'Total Est. Return' values
        EXPECTED: Total stake = All stakes selected.
        EXPECTED: Total Est. Returns = All Est. Returns selected
        """
        pass

    def test_006_deselect_one_bet_and_check_total_stake_and_total_est_returns_values(self):
        """
        DESCRIPTION: Deselect one bet and check 'Total Stake' and 'Total Est. Returns' values
        EXPECTED: Total stake is decreased and show actual value of selected stakes
        EXPECTED: Total Est. Returns are decreased how actual value of selected est. returns
        """
        pass

    def test_007_click_confirm_button_and_checktotal_stake_and_total_est_returns_values_in_bet_receipt(self):
        """
        DESCRIPTION: Click 'Confirm' button and check 'Total Stake' and 'Total Est. Returns' values in Bet Receipt
        EXPECTED: 'Total Stake' and 'Total Est. Returns' values should be the same as before placing bet ( potentialPayout:"" in Network>getBetDetaile?betId=''>bet>leg)
        """
        pass
