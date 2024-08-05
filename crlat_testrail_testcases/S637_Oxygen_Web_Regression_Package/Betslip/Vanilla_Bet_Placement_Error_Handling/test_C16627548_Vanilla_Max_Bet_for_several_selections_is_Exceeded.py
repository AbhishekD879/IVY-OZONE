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
class Test_C16627548_Vanilla_Max_Bet_for_several_selections_is_Exceeded(Common):
    """
    TR_ID: C16627548
    NAME: [Vanilla] Max Bet for several selections is Exceeded
    DESCRIPTION: This test case verifies Error Handling When Max Bet for several selections is exceeded
    PRECONDITIONS: 1. The user's account balance is sufficient to cover the max bet stake
    PRECONDITIONS: 2. Overask is turned on
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

    def test_002_add_multiple_selections_to_the_bet_slip(self):
        """
        DESCRIPTION: Add multiple selections to the Bet Slip
        EXPECTED: Betslip counter is increased with number of selections
        """
        pass

    def test_003_enter_stakes_value_which_exceed_max_bet_stake_for_current_events_in_stake_fieldclick_place_bet_button(self):
        """
        DESCRIPTION: Enter stakes value which exceed Max Bet Stake for current events in 'Stake' field
        DESCRIPTION: Click 'PLACE BET' button
        EXPECTED: * Bet is NOT placed
        EXPECTED: * There is a message that stake exceeds the max stake allowed and it's being reviewed by trading team
        """
        pass

    def test_004_decline_bets_in_backoffice_httpsbackoffice_tst2coralcoukti____bet___bi_request(self):
        """
        DESCRIPTION: Decline bets in backoffice https://backoffice-tst2.coral.co.uk/ti --> BET -->BI Request)
        EXPECTED: * Bet is not set
        EXPECTED: * Selection of bet is still visible in Betslip
        """
        pass

    def test_005_remove_bets_that_exceed_maximum_stake_from_betslip_and_try_to_do_another_bet_that_does_not_exceed_market_minmax_stake(self):
        """
        DESCRIPTION: Remove bets that exceed maximum stake from betslip and try to do another bet that does not exceed market min/max stake
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
