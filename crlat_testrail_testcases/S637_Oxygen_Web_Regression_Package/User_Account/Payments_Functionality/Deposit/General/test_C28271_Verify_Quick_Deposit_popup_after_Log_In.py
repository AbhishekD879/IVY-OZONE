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
class Test_C28271_Verify_Quick_Deposit_popup_after_Log_In(Common):
    """
    TR_ID: C28271
    NAME: Verify Quick Deposit popup after Log In
    DESCRIPTION: This test case verifies Quick Deposit functionality after Log In.
    DESCRIPTION: AUTOTEST: [C2594259]
    PRECONDITIONS: 1.  User is logged out
    PRECONDITIONS: 2.  User balance is 0.
    PRECONDITIONS: **NOTE**: if other pop-up messages are expected after log in then the order of pop-up appearing should be the following:
    PRECONDITIONS: *   Terms and Conditions -> Verify Your Account (Netverify) -> Deposit Limits -> Quick Deposit
    PRECONDITIONS: **NOTE:**
    PRECONDITIONS: * in order to see list with all payment methods, user's balance MUST be < 100 (regardless of currency) - otherwise, only the default payment method is shown. This concerns 'Quick deposit' as well - if user's balance is > 100, only ONE card of all registered cards for this user will be shown (only the default card)
    """
    keep_browser_open = True

    def test_001_log_in_into_application_using_correct_credentials(self):
        """
        DESCRIPTION: Log in into application using correct credentials
        EXPECTED: *   User is successfully logged in
        EXPECTED: *   Home page is opened if user has positive amount on his balance
        EXPECTED: *   'Quick Deposit' pop-up message is shown ('Hi <username>, You currently have <currency symbol>0.00 in your account.') if user's balance is equal to 0. 'Deposit Now' button is present on 'Quick Deposit' pop up
        """
        pass

    def test_002_verifyquick_deposit_pop_up(self):
        """
        DESCRIPTION: Verify 'Quick Deposit' pop-up
        EXPECTED: 'Quick Deposit' pop-up consists of the following:
        EXPECTED: 1.  TITLE: **'Quick Deposit'**
        EXPECTED: 2.  BODY: 'Hi [**username**], You currently have <currency symbol> 0.00 in your account.'
        EXPECTED: 3.  BUTTON: **'Deposit Now'**
        EXPECTED: [FOR LADBROKES ONLY]: 4. BUTTON: **'Cancel'**
        EXPECTED: ![](index.php?/attachments/get/36310)
        """
        pass

    def test_003_verifydeposit_now_button(self):
        """
        DESCRIPTION: Verify 'Deposit Now' button
        EXPECTED: Tapping 'Deposit Now' button takes user to the 'Deposit' page with 'My Payments' tab selected
        """
        pass

    def test_004_for_ladbrokes_only_verify_cancel_buttonfor_coral_only_verify_x_button(self):
        """
        DESCRIPTION: [FOR LADBROKES ONLY]: Verify 'Cancel' button
        DESCRIPTION: [FOR CORAL ONLY]: Verify 'x' button
        EXPECTED: It is possible to close the notification by:
        EXPECTED: *
        EXPECTED: [FOR LADBROKES ONLY]: clicking on the 'Cancel' button
        EXPECTED: *
        EXPECTED: [FOR CORAL ONLY]: clicking on the 'x' button
        EXPECTED: *
        EXPECTED: [FOR BOTH]: clicking away anywhere on the screen
        """
        pass

    def test_005_verify_currency_symbol_on_quick_deposit_pop_up(self):
        """
        DESCRIPTION: Verify currency symbol on Quick Deposit pop-up
        EXPECTED: Currency symbol is correctly displayed within body of the pop-up. (€, $, Kr)
        """
        pass
