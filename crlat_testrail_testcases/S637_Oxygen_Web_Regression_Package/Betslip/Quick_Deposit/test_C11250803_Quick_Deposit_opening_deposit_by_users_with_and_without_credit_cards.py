import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.betslip
@vtest
class Test_C11250803_Quick_Deposit_opening_deposit_by_users_with_and_without_credit_cards(Common):
    """
    TR_ID: C11250803
    NAME: Quick Deposit: opening deposit by users with and without credit cards
    DESCRIPTION: This test case verifies Quick Deposit appearance for users with and without credit cards
    PRECONDITIONS: - You should have 2 users:
    PRECONDITIONS: 1) User with registered credit cards
    PRECONDITIONS: 2) User without registered credit cards
    PRECONDITIONS: - You should be logged in with a user with registered cards
    PRECONDITIONS: - Bestlip should be opened and have some selections added
    """
    keep_browser_open = True

    def test_001_tap_account_balance_area_in_the_betslip_header___deposit_button_and_verify_displaying_of_quick_deposit_section(self):
        """
        DESCRIPTION: Tap 'Account Balance' area in the Betslip header  > 'Deposit' button and verify displaying of Quick Deposit section
        EXPECTED: - Quick Deposit section is opened
        EXPECTED: - Account Balance is still displayed at the top right corner in  the Betslip header
        """
        pass

    def test_002___make_a_bet_and_tap_account_balance_area_in_the_betslip_header__deposit_button__verify_user_navigation_to_deposit_page(self):
        """
        DESCRIPTION: - Make a bet and tap 'Account Balance' area in the Betslip header > 'Deposit' button
        DESCRIPTION: - Verify user navigation to deposit page
        EXPECTED: **Coral**
        EXPECTED: User is redirected to 'Deposit' menu > 'My Payments' tab
        EXPECTED: **Ladbrokes**
        EXPECTED: User is redirected to accountone deposit page
        """
        pass

    def test_003___log_out_by_user_with_registered_credit_cards_and_login_by_user_without_registered_credit_cards__open_betslip__tap_account_balance_area_in_the_betslip_header___deposit_button_and_verify_redirecting_of_user_to_deposit_menu(self):
        """
        DESCRIPTION: - Log out by user with registered credit cards and login by user without registered credit cards
        DESCRIPTION: - Open betslip
        DESCRIPTION: - Tap 'Account Balance' area in the Betslip header  > 'Deposit' button and verify redirecting of user to Deposit menu
        EXPECTED: **Coral**
        EXPECTED: User is redirected to 'Deposit' menu > 'My Payments' tab
        EXPECTED: **Ladbrokes**
        EXPECTED: User is redirected to accountone deposit page
        """
        pass
