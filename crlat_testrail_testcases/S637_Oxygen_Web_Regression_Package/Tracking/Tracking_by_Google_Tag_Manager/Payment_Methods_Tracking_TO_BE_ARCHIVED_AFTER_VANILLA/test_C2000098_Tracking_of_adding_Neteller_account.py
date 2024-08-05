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
class Test_C2000098_Tracking_of_adding_Neteller_account(Common):
    """
    TR_ID: C2000098
    NAME: Tracking of adding Neteller account
    DESCRIPTION: This test case verifies tracking in the Google Analytic's data Layer of adding Neteller
    PRECONDITIONS: - The test case should be run on Mobile, Tablet and Wrappers
    PRECONDITIONS: - Browser console should be opened
    PRECONDITIONS: - User is logged in
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

    def test_003_tap_add_neteller_tab(self):
        """
        DESCRIPTION: Tap 'Add Neteller' tab
        EXPECTED: 'Add Neteller' tab is selected
        """
        pass

    def test_004_enter_valid_account_or_email_into_account_idemail_field(self):
        """
        DESCRIPTION: Enter valid Account or Email into 'Account ID/Email:' field
        EXPECTED: Account/Email is displayed
        """
        pass

    def test_005_enter_valid_security_id_into_secure_id_or_authentication_code_field(self):
        """
        DESCRIPTION: Enter valid Security ID into 'Secure ID or Authentication Code:' field
        EXPECTED: Secure ID or Authentication Code is displayed
        """
        pass

    def test_006_enter_valid_amount_manually_or_using_quick_deposit_buttons__tap_deposit_button(self):
        """
        DESCRIPTION: Enter valid amount manually or using quick deposit buttons > Tap 'Deposit' button
        EXPECTED: - User is redirected to 'My Payments' tab
        EXPECTED: - Successful message: **"Your deposit of <currency symbol> XX.XX was successful. Reference: #XXXXXXX"**
        """
        pass

    def test_007_type_in_browser_console_datalayer_and_tap_enter(self):
        """
        DESCRIPTION: Type in browser console "dataLayer" and tap 'Enter
        EXPECTED: The following event with corresponding parameters is present in data layer:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'deposit',
        EXPECTED: 'eventAction' : 'add neteller',
        EXPECTED: 'eventLabel' : 'success'
        EXPECTED: });
        """
        pass

    def test_008_go_back_to_add_neteller_tab(self):
        """
        DESCRIPTION: Go back to 'Add Neteller' tab
        EXPECTED: 'Add Neteller' tab is selected
        """
        pass

    def test_009_enter_invalid_account_or_email_into_account_idemail_field(self):
        """
        DESCRIPTION: Enter invalid Account or Email into 'Account ID/Email:' field
        EXPECTED: Account/Email is displayed
        """
        pass

    def test_010_enter_invalid_security_id_into_secure_id_or_authentication_code_field(self):
        """
        DESCRIPTION: Enter invalid Security ID into 'Secure ID or Authentication Code:' field
        EXPECTED: Secure ID or Authentication Code is displayed
        """
        pass

    def test_011_enter_valid_amount_manually_or_using_quick_deposit_buttons__tap_deposit_button(self):
        """
        DESCRIPTION: Enter valid amount manually or using quick deposit buttons > Tap 'Deposit' button
        EXPECTED: - User is stayed on 'NETELLER' tab
        EXPECTED: - Error message is shown at the top of the tab on the red background: "We are sorry, but your NETeller deposit has been declined"
        """
        pass

    def test_012_type_in_browser_console_datalayer_and_tap_enter(self):
        """
        DESCRIPTION: Type in browser console "dataLayer" and tap 'Enter
        EXPECTED: The following event with corresponding parameters is present in data layer:
        EXPECTED: dataLayer.push({
        EXPECTED: 'event' : 'trackEvent',
        EXPECTED: 'eventCategory' : 'deposit',
        EXPECTED: 'eventAction' : 'add neteller',
        EXPECTED: 'eventLabel' : 'failure'
        EXPECTED: 'errorMessage' : '<< ERROR MESSAGE >>',
        EXPECTED: 'errorCode' : '<< ERROR CODE >>'
        EXPECTED: });
        """
        pass
