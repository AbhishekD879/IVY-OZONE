import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.retail
@vtest
class Test_C2064596_Verify_adding_Football_filter_results_to_betslip_online_betting_journey(Common):
    """
    TR_ID: C2064596
    NAME: Verify adding Football filter results to betslip (online betting journey)
    DESCRIPTION: This test case verifies adding filter selections to betslip from Football Filter
    DESCRIPTION: [Bet Types](https://confluence.egalacoral.com/display/SPI/Bet+Types)
    DESCRIPTION: [Work Around for calculating payout potential of Multiple Bet Types](https://confluence.egalacoral.com/display/SPI/Work+Around+for+calulating+payout+potential+of+Multiple+Bet+Types)
    PRECONDITIONS: User is logged in
    PRECONDITIONS: Open Football Filter results page:
    PRECONDITIONS: 1. Open Football -> Coupons tab -> Select any coupon that has couponSortCode parameter equal to "MR"
    PRECONDITIONS: 2. Tap Football Bet Filter
    PRECONDITIONS: 3. Scroll down and tap 'Find Bets'
    """
    keep_browser_open = True

    def test_001__football_filter_results_page_is_opened(self):
        """
        DESCRIPTION: * Football Filter results page is opened
        EXPECTED: 
        """
        pass

    def test_002_select_1_selection_and_tap_add_to_betslip_button(self):
        """
        DESCRIPTION: Select 1 selection and tap 'ADD TO BETSLIP' button
        EXPECTED: * Betslip is opened
        EXPECTED: * Only selected result is added to betslip
        EXPECTED: * The 1 single bet is formed
        """
        pass

    def test_003__return_back_to_football_filter_results_page_select_more_selections_and_tap_add_to_betslip_button(self):
        """
        DESCRIPTION: * Return back to Football Filter Results page
        DESCRIPTION: * Select more selections and tap 'ADD TO BETSLIP' button
        EXPECTED: - A user is on betslip
        EXPECTED: - Betslip is supplemented with newly added selections
        """
        pass

    def test_004_enter_correct_stake_in_stake_field_and_tap_bet_now(self):
        """
        DESCRIPTION: Enter correct Stake in 'Stake' field and tap 'Bet Now'
        EXPECTED: * Bet is placed successfully
        EXPECTED: * User 'Balance' is decreased by the value entered in 'Stake' field
        EXPECTED: * Bet Slip is replaced with a Bet Receipt view
        """
        pass

    def test_005_log_out(self):
        """
        DESCRIPTION: Log out
        EXPECTED: User is successfully logged out
        """
        pass

    def test_006_open_football_filter_results_look_at_preconditions(self):
        """
        DESCRIPTION: Open Football Filter results (look at preconditions)
        EXPECTED: Football Filter results page is opened
        """
        pass

    def test_007_select_1_selection_and_tap_add_to_betslip_button(self):
        """
        DESCRIPTION: Select 1 selection and tap 'ADD TO BETSLIP' button
        EXPECTED: * Betslip is opened
        EXPECTED: * Only selected result is added to betslip
        EXPECTED: * The 1 single bet is formed
        """
        pass

    def test_008_enter_correct_stake_in_stake_field_and_tap_login_and_place_bet(self):
        """
        DESCRIPTION: Enter correct Stake in 'Stake' field and tap 'Login And Place Bet'
        EXPECTED: Login pop-up is open
        """
        pass

    def test_009_log_in_to_the_app(self):
        """
        DESCRIPTION: Log in to the app
        EXPECTED: * User is logged in
        EXPECTED: * Bet is placed successfully:
        EXPECTED: 1. User 'Balance' is decreased by the value entered in 'Stake' field
        EXPECTED: 2. Bet Slip is replaced with a Bet Receipt view
        """
        pass
