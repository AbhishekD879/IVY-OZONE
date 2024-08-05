import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.sports
@vtest
class Test_C44870214_Customer_can_see_error_message_on_placing_bets_with_insufficient_funds_in_wallet(Common):
    """
    TR_ID: C44870214
    NAME: Customer can see error message on placing bets with insufficient funds in wallet
    DESCRIPTION: This test case verify insufficient balance
    PRECONDITIONS: UserName: goldenbuild  Password:Password1
    """
    keep_browser_open = True

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load oxygen application
        EXPECTED: HomePage opened
        """
        pass

    def test_002_login_with_valid_credentials(self):
        """
        DESCRIPTION: Login with valid credentials
        EXPECTED: user logged in
        """
        pass

    def test_003_go_to_any_sport_and_add_selection_to_bqbetslip(self):
        """
        DESCRIPTION: Go to any sport and add selection to bQ/Betslip
        EXPECTED: Selection added
        """
        pass

    def test_004_verify__message_display_when_user_enter_stake_more_than_the_account_balance_to(self):
        """
        DESCRIPTION: Verify  message display when user Enter stake more than the account balance to
        EXPECTED: 'Please deposit a min £XX.XX to continue placing your bet' message displayed in betslip.
        """
        pass

    def test_005_verify_qd_pop_opens_when_user_click_on_make_a_deposit_button(self):
        """
        DESCRIPTION: Verify QD pop opens when user click on Make a deposit button
        EXPECTED: QD pop displayed
        EXPECTED: -Visa card - registered
        EXPECTED: -Deposit Amount
        EXPECTED: -CVV
        EXPECTED: -CTA
        EXPECTED: -Total stake
        EXPECTED: Potential Returns
        """
        pass

    def test_006_verify_acceptdeposit__place_bet_button_gets_enabled_once_user_enter_the_amount_and_cvv(self):
        """
        DESCRIPTION: Verify Accept(DEPOSIT & PLACE BET) button gets enabled once user enter the amount and CVV
        EXPECTED: Accept(DEPOSIT & PLACE BET) button is  enabled
        """
        pass

    def test_007_verify_bet_is_placed_when_user_tapsclick_on_acceptdeposit__place_bet_button(self):
        """
        DESCRIPTION: Verify bet is placed when user taps/click on Accept(DEPOSIT & PLACE BET) button
        EXPECTED: Bet placed successfully
        """
        pass
