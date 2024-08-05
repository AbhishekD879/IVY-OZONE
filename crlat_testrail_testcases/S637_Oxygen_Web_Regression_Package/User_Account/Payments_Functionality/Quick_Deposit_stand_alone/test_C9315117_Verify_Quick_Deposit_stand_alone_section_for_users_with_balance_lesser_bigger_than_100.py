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
class Test_C9315117_Verify_Quick_Deposit_stand_alone_section_for_users_with_balance_lesser_bigger_than_100(Common):
    """
    TR_ID: C9315117
    NAME: Verify 'Quick Deposit' stand alone section for users with balance lesser/bigger than 100
    DESCRIPTION: This test case verifies 'Quick Deposit' stand alone section for users with balance lesser/bigger than 100
    PRECONDITIONS: 1. User has a few credit cards, and other payment methods e.g. PayPal & Neteller payment methods added to his account
    PRECONDITIONS: 2. User has two accounts with balance:
    PRECONDITIONS: - Less than 100
    PRECONDITIONS: - Bigger than 100
    PRECONDITIONS: **Note: Balance of the user with the exact amount of 100 GBP will still result in cards dropdown being shown, instead of placeholder with only last card used for depositing.**
    """
    keep_browser_open = True

    def test_001_log_in_with_user_that_has_balance_less_than_100(self):
        """
        DESCRIPTION: Log in with user that has balance less than 100
        EXPECTED: User is logged in
        """
        pass

    def test_002_open_right_menu__tap_on_deposit_button(self):
        """
        DESCRIPTION: Open 'Right' menu > tap on 'Deposit' button
        EXPECTED: 'Quick Deposit' stand alone section is opened
        """
        pass

    def test_003_verify_payment_methods_available(self):
        """
        DESCRIPTION: Verify Payment methods available
        EXPECTED: - All credit cards are displayed within Credit Cards Dropdown, once it is expanded
        EXPECTED: ![](index.php?/attachments/get/36328)
        EXPECTED: - Other payment methods e.g. Paypal and Neteller are NOT displayed (even if one of them is a default paymet method)
        EXPECTED: --
        EXPECTED: **Expanded(tapped) Credit cards dropdown is a native device OS-dependent feature**
        """
        pass

    def test_004_log_out_from_app(self):
        """
        DESCRIPTION: Log out from app
        EXPECTED: User is logged out
        """
        pass

    def test_005_log_in_with_user_that_has_balance_bigger_than_100(self):
        """
        DESCRIPTION: Log in with user that has balance bigger than 100
        EXPECTED: User is logged in
        """
        pass

    def test_006_open_right_menu__tap_on_deposit_button(self):
        """
        DESCRIPTION: Open 'Right' menu > tap on 'Deposit' button
        EXPECTED: 'Quick Deposit' stand alone section is opened
        """
        pass

    def test_007_verify_payment_methods_available(self):
        """
        DESCRIPTION: Verify Payment methods available
        EXPECTED: - Only last added credit card is displayed 'Quick Deposit' stand alone section
        EXPECTED: ![](index.php?/attachments/get/36327)
        EXPECTED: - Other payment methods e.g. Paypal and Neteller are NOT displayed (even if one of them is a default paymet method)
        """
        pass
