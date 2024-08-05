import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.low
@pytest.mark.other
@vtest
class Test_C2000008_Tracking_of_adding_PayPal_account(Common):
    """
    TR_ID: C2000008
    NAME: Tracking of adding PayPal account
    DESCRIPTION: This test case verifies tracking in the Google Analytic's data Layer of addition PayPal
    PRECONDITIONS: - The test case should be run on Mobile, Tablet and Wrappers
    PRECONDITIONS: - Browser console should be opened
    PRECONDITIONS: - User is logged in without added PayPal account
    """
    keep_browser_open = True

    def test_001_load_oxygen_app(self):
        """
        DESCRIPTION: Load Oxygen app
        EXPECTED: Homepage is opened
        """
        pass

    def test_002_tap_right_menu_icon__deposit(self):
        """
        DESCRIPTION: Tap Right menu icon > Deposit
        EXPECTED: - Deposit page is opened
        EXPECTED: - My Payments tab is selected by default
        """
        pass

    def test_003_tap_add_paypal_tab(self):
        """
        DESCRIPTION: Tap 'Add PayPal' tab
        EXPECTED: 'Add PayPal' tab is opened
        """
        pass

    def test_004_enter_valid_amount_manually_or_using_quick_deposit_buttons__tap_on_deposit_button(self):
        """
        DESCRIPTION: Enter valid amount manually or using quick deposit buttons > Tap on 'Deposit' button
        EXPECTED: Pop-up is shown:
        EXPECTED: - header "Redirecting"
        EXPECTED: - body "Redirecting to PayPal"
        EXPECTED: - Loading spinner
        """
        pass

    def test_005_login_a_new_user_on_paypal_form(self):
        """
        DESCRIPTION: Login a new user on PayPal form
        EXPECTED: 
        """
        pass

    def test_006_tap_pay_now_button(self):
        """
        DESCRIPTION: Tap 'Pay Now' button
        EXPECTED: - User is redirected to 'My Payments' tab
        EXPECTED: - Successful message: **"Your deposit of <currency symbol> XX.XX was successful.**
        EXPECTED: - PayPal payment method is shown first in 'Select Payment Method' drop-down list in the format: "PayPal(email@address.com)"
        """
        pass

    def test_007_type_in_browser_console_datalayer_and_tap_enter(self):
        """
        DESCRIPTION: Type in browser console "dataLayer" and tap 'Enter
        EXPECTED: The following event with corresponding parameters is present in data layer:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'deposit',
        EXPECTED: 'eventAction' : 'add paypal',
        EXPECTED: 'eventLabel' : 'success'
        EXPECTED: });
        """
        pass

    def test_008_go_back_to_add_paypal_tab(self):
        """
        DESCRIPTION: Go back to 'Add PayPal' tab
        EXPECTED: 'Add PayPal' tab is opened
        """
        pass

    def test_009_enter_valid_amount_manually_or_using_quick_deposit_buttons__tap_on_deposit_button(self):
        """
        DESCRIPTION: Enter valid amount manually or using quick deposit buttons > Tap on 'Deposit' button
        EXPECTED: Pop-up is shown:
        EXPECTED: - header "Redirecting"
        EXPECTED: - body "Redirecting to PayPal"
        EXPECTED: - Loading spinner
        """
        pass

    def test_010_login_with_already_used_paypal_user_account_on_paypal_form(self):
        """
        DESCRIPTION: Login with already used PayPal user_account on PayPal form
        EXPECTED: 
        """
        pass

    def test_011_tap_pay_now_button(self):
        """
        DESCRIPTION: Tap 'Pay Now' button
        EXPECTED: - User is redirected to 'My Payments' tab
        EXPECTED: - Error message is shown at the top of the tab on the red background: "Cancelled by Payment Method Processor"
        """
        pass

    def test_012_type_in_browser_console_datalayer_and_tap_enter(self):
        """
        DESCRIPTION: Type in browser console "dataLayer" and tap 'Enter
        EXPECTED: The following event with corresponding parameters is present in data layer:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'deposit',
        EXPECTED: 'eventAction' : 'add paypal',
        EXPECTED: 'eventLabel' : 'failure'
        EXPECTED: 'errorMessage' : '<< ERROR MESSAGE >>',
        EXPECTED: 'errorCode' : '<< ERROR CODE >>'
        EXPECTED: });
        """
        pass
