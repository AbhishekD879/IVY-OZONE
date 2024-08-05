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
class Test_C16627549_Not_Valid_test_case__need_to_be_UpdatedVanilla_Bet_Placement_when_Stake_value_is_lower_than_MinStake(Common):
    """
    TR_ID: C16627549
    NAME: [Not Valid test case - need to be Updated][Vanilla] Bet Placement when Stake value is lower than MinStake
    DESCRIPTION: This test case verifies bet slip error handling in case when user's individual bet is lower than min value for selected market
    PRECONDITIONS: 1.  The user's account balance is sufficient to cover the max bet stake
    PRECONDITIONS: 2. Overask is turned off for used user
    PRECONDITIONS: For <Sport> it is possible to place a bet from:
    PRECONDITIONS: - event landing page
    PRECONDITIONS: - event details page
    PRECONDITIONS: For <Races> it is possible to place a bet from:
    PRECONDITIONS: - 'Next 4' module
    PRECONDITIONS: - event landing page
    """
    keep_browser_open = True

    def test_001_log_in_to_application(self):
        """
        DESCRIPTION: Log in to application
        EXPECTED: User is logged in
        """
        pass

    def test_002_add_selection_to_the_bet_slip(self):
        """
        DESCRIPTION: Add selection to the Bet Slip
        EXPECTED: Betslip counter is increased
        """
        pass

    def test_003_enter_stake_value_which_is_lower_than_min_bet_stake_for_current_event_in_stake_fieldclick_place_bet_button(self):
        """
        DESCRIPTION: Enter stake value which is lower than Min Bet Stake for current event in 'Stake' field
        DESCRIPTION: Click 'PLACE BET' button
        EXPECTED: * Bet is NOT placed
        EXPECTED: * There is a message that stake is lower than min stake allowed and it's being reviewed by trading team
        """
        pass

    def test_004_decline_the_bet_in_backoffice_httpsbackoffice_tst2coralcoukti____bet___bi_request(self):
        """
        DESCRIPTION: Decline the bet in backoffice https://backoffice-tst2.coral.co.uk/ti --> BET -->BI Request)
        EXPECTED: * Bet is not set
        EXPECTED: * Selection of bet is still visible in Betslip
        """
        pass

    def test_005_remove_bet_that_is_lower_than_minimum_stake_from_betslip_and_try_to_do_another_bet_that_does_not_exceed_market_minmax_stake(self):
        """
        DESCRIPTION: Remove bet that is lower than minimum stake from betslip and try to do another bet that does not exceed market min/max stake
        EXPECTED: * Bet with exceeded maximum stake is removed from the Betslip
        EXPECTED: * User is able to set another bet
        """
        pass

    def test_006_repeat_seps_1_3(self):
        """
        DESCRIPTION: Repeat seps 1-3
        EXPECTED: 
        """
        pass

    def test_007_accept_the_bet_in_backoffice_httpsbackoffice_tst2coralcoukti____bet___bi_request(self):
        """
        DESCRIPTION: Accept the bet in backoffice https://backoffice-tst2.coral.co.uk/ti --> BET -->BI Request)
        EXPECTED: * Bet is placed successfully
        EXPECTED: * Bet Receipt is displayed
        """
        pass
