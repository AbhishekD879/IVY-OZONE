import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.critical
@pytest.mark.user_account
@vtest
class Test_C34375808_Verify_that_user_with_000_balance_can_make_a_deposit(Common):
    """
    TR_ID: C34375808
    NAME: Verify that user with 0.00 balance can make a deposit
    DESCRIPTION: Verify that the user  with 0.00 balance can make a deposit
    DESCRIPTION: AUTOMATED [C46287317]
    PRECONDITIONS: 
    """
    keep_browser_open = True

    def test_001_login_to_oxygen_app_with_a_user_who_has_no_funds_in_the_account(self):
        """
        DESCRIPTION: Login to Oxygen app with a user who has no funds in the account
        EXPECTED: 'Low balance' tooltip is displayed within Betslip
        EXPECTED: (Handled on GVC side)
        """
        pass

    def test_002_click_on_deposit_button_from_navigation_bar_for_desktop_or_deposit_button_from_my_account_menu_for_desktopmobiletablet(self):
        """
        DESCRIPTION: Click on 'Deposit' button from Navigation bar (For Desktop) or 'Deposit' button from 'My Account' menu (For Desktop/Mobile/Tablet)
        EXPECTED: Deposit page is opened.
        """
        pass

    def test_003_select_a_credit_card_typeenter_an_amount_eg_10enter_a_cv2_eg_123click_on_deposit(self):
        """
        DESCRIPTION: Select a credit card type
        DESCRIPTION: Enter an amount (e.g. 10£)
        DESCRIPTION: Enter a CV2 (e.g. 123)
        DESCRIPTION: Click on Deposit
        EXPECTED: "Your deposit of XX.XX GBP has been successful" message is displayed on green background
        """
        pass

    def test_004_observe_the_balance_of_the_account(self):
        """
        DESCRIPTION: Observe the balance of the account
        EXPECTED: The balance is correctly updated within seconds
        """
        pass

    def test_005_click_on_user_menu___logout(self):
        """
        DESCRIPTION: Click on User Menu -> logout
        EXPECTED: User is logged out
        """
        pass
