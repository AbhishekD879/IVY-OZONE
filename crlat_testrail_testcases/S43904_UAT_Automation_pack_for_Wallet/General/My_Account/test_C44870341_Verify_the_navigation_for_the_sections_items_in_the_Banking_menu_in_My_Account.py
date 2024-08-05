import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.user_account
@vtest
class Test_C44870341_Verify_the_navigation_for_the_sections_items_in_the_Banking_menu_in_My_Account(Common):
    """
    TR_ID: C44870341
    NAME: Verify the navigation for the sections/items in the Banking menu in My Account.
    DESCRIPTION: 
    PRECONDITIONS: User is logged in the application.
    """
    keep_browser_open = True

    def test_001_clicktap_my_account_button_avatar__balance(self):
        """
        DESCRIPTION: Click/tap My Account button (Avatar)-> Balance
        EXPECTED: Banking menu with My Balance, Deposit and Withdraw is displayed
        """
        pass

    def test_002_verify_my_balance_pageclick_on_my_balance(self):
        """
        DESCRIPTION: Verify My Balance Page
        DESCRIPTION: Click on My Balance
        EXPECTED: My Balance page is opened with list
        EXPECTED: Withdrawable - Online
        EXPECTED: Restricted
        EXPECTED: Available Balance
        EXPECTED: Total Balance
        """
        pass

    def test_003_click_back_button_on_my_balance_page(self):
        """
        DESCRIPTION: Click Back button on My Balance page
        EXPECTED: User is navigated to previous page
        """
        pass

    def test_004_verify_deposit_on_banking_pageclick_on_deposit(self):
        """
        DESCRIPTION: Verify Deposit on Banking page
        DESCRIPTION: Click on Deposit
        EXPECTED: Deposit Page is opened
        EXPECTED: Header with "Deposit" is displayed
        """
        pass

    def test_005_click_cancel_button_on_deposit_page(self):
        """
        DESCRIPTION: Click Cancel button on Deposit Page
        EXPECTED: User is navigate to HomePage
        """
        pass

    def test_006_verify_withdrawrepeat_step_1click_on_withdraw(self):
        """
        DESCRIPTION: Verify Withdraw
        DESCRIPTION: Repeat step 1
        DESCRIPTION: Click on Withdraw
        EXPECTED: Withdraw page is opened
        EXPECTED: Header with "Withdrawal" is displayed
        """
        pass

    def test_007_click_cancel_button_on_withdraw(self):
        """
        DESCRIPTION: Click Cancel button on Withdraw
        EXPECTED: User is navigated back to HomePage
        """
        pass
