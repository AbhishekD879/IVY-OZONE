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
class Test_C16852870_Verify_Quick_Deposit_for_UK_Tote_bets(Common):
    """
    TR_ID: C16852870
    NAME: Verify Quick Deposit for UK Tote bets
    DESCRIPTION: Verify that the user is redirected on Deposit page after clicking the "Deposit" button on the header in the betslip
    PRECONDITIONS: User is logged in
    """
    keep_browser_open = True

    def test_001_go_to_the_horse_racing_page(self):
        """
        DESCRIPTION: Go to the Horse racing page
        EXPECTED: Horse racing page is opened
        """
        pass

    def test_002_click_on_the_event_with_the_tote_available(self):
        """
        DESCRIPTION: Click on the event with the Tote available
        EXPECTED: The event is loaded
        """
        pass

    def test_003_click_on_the_add_to_betslip_button_ex_add_2_selections_for_exacta_tote_pool(self):
        """
        DESCRIPTION: Click on the "Add to Betslip" button (e.x. add 2 selections for Exacta Tote Pool)
        EXPECTED: The selections are added to Betslip
        """
        pass

    def test_004_go_to_the_betslip(self):
        """
        DESCRIPTION: Go to the Betslip
        EXPECTED: Betslip is opened and the added Tote bet is displayed
        """
        pass

    def test_005_enter_the_stake_that_is_bigger_than_the_user_balance_tap_place_bet_button(self):
        """
        DESCRIPTION: Enter the stake that is bigger than the user balance, tap 'Place Bet' button
        EXPECTED: The "insufficient funds in your account to place bet" message is displayed
        """
        pass

    def test_006_click_on_the_user_balance_on_the_header_in_the_betslip(self):
        """
        DESCRIPTION: Click on the user balance on the header in the betslip
        EXPECTED: Two sections are opened:
        EXPECTED: - Hide Balance
        EXPECTED: - Deposit
        """
        pass

    def test_007_click_on_the_deposit_button(self):
        """
        DESCRIPTION: Click on the "Deposit" button
        EXPECTED: Betslip is closed and the user is redirected to the main Deposit Page
        """
        pass
