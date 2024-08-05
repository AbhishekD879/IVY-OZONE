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
class Test_C29142_Total_Stake_and_Total_Est_Return_for_singles(Common):
    """
    TR_ID: C29142
    NAME: Total Stake and Total Est. Return for singles
    DESCRIPTION: This test case verifies that Total stake and Total Est. Returns updates with new values after selection and deselection of modified bets
    DESCRIPTION: Jira ticket:
    DESCRIPTION: BMA-9500 Overask - Total Est. Return and Total stake Update after bet interception
    DESCRIPTION: BMA-20390 New Betslip - Overask design improvements
    PRECONDITIONS: 1. Load Oxygen application and login ( OverAsk is enabled for user)
    PRECONDITIONS: 2. Add to betslip 2 single bets
    """
    keep_browser_open = True

    def test_001____enter_higher_than_maximum_allowed_stake_for_1_bets___enterlower_than_maximum_allowed_stake_value_for_1_bet___select_bet_now_button(self):
        """
        DESCRIPTION: *   Enter higher than maximum allowed stake  for 1 bets
        DESCRIPTION: *   Enter lower than maximum allowed  stake value for 1 bet
        DESCRIPTION: *   Select 'Bet Now' button
        EXPECTED: *   OverAsk is triggered.
        EXPECTED: *   Message is shown for user: 'Please wait, your bet is being reviewed by one of our Traders. This normally takes less than a minute.'
        """
        pass

    def test_002____in_backoffice_modify_stake_values_and_confirm_offer___check_offer_appears_in_bet_slip_in_oxygen_app(self):
        """
        DESCRIPTION: *   In backoffice modify stake values and confirm offer
        DESCRIPTION: *   Check offer appears in Bet Slip in Oxygen app
        EXPECTED: *   Message is shown "Please wait, your bet is being reviewed by one of our Traders"
        EXPECTED: *   Modified stake value is displayed in green stake box
        EXPECTED: *   Modified bets are selected and checkbox is available
        EXPECTED: *   'Total Stake' is counted and displayed for selected bets (that were not modified)
        EXPECTED: *   'Total Est. Returns' is equal to Est.Returns for auto-selected + offered bet
        """
        pass

    def test_003_check_total_stake_and_total_est_return_values(self):
        """
        DESCRIPTION: Check 'Total Stake' and 'Total Est. Return' values
        EXPECTED: Total stake =  stakes selected.
        EXPECTED: Total Est. Returns = total est. returns of selected stakes ( Total Est. Returns =  (Network> readbet> payout value)
        """
        pass

    def test_004_deselect_one_bet_and_check_total_stake_and_total_est_returns_values(self):
        """
        DESCRIPTION: Deselect one bet and check 'Total Stake' and 'Total Est. Returns' values
        EXPECTED: Total stake will decrease and show actual value of selected stakes
        EXPECTED: Total Est. Returns =  (Network> readbet> payout value)
        """
        pass

    def test_005_click_accept__bet_nuber_of_selected_bets_button_and_check_total_stake_and_total_est_returns_values_in_bet_receipt(self):
        """
        DESCRIPTION: Click 'Accept & Bet ([nuber of selected bets])' button and check 'Total Stake' and 'Total Est. Returns' values in Bet Receipt
        EXPECTED: 'Total Stake' and 'Total Est. Returns' values should be the same as before placing bet ( potentialPayout:"" in Network>getBetDetaile?betId=''>bet>leg)
        """
        pass
