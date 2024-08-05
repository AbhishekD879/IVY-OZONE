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
class Test_C1924740_Verify_Add_PayPal_tab(Common):
    """
    TR_ID: C1924740
    NAME: Verify 'Add PayPal' tab
    DESCRIPTION: This test case verifies 'Add PayPal' tab.
    PRECONDITIONS: *  In CMS > System Configuration > 'Pay Pal' section > 'viaSafeCharge' check box is NOT checked
    PRECONDITIONS: *   User is logged in
    PRECONDITIONS: *   User has a valid (unrestricted) PayPal account from which his/her can deposit funds via
    PRECONDITIONS: Available PayPal Accounts:
    PRECONDITIONS: *   ppone@yopmail.com / devine12
    PRECONDITIONS: *   pptwo@yopmail.com / devine12
    PRECONDITIONS: *   ppthree@yopmail.com / devine12
    PRECONDITIONS: *   ppfour@yopmail.com / devine12
    PRECONDITIONS: *   ppfive@yopmail.com / devine12
    PRECONDITIONS: Paypal Prod account ( works with external users, not registered on test@playtech.com and with UK VPN): IanTevez33@gmail.com/Lanzini6266
    PRECONDITIONS: Oxygen Prod account : paypaltest1/test123
    """
    keep_browser_open = True

    def test_001_open_deposit_page(self):
        """
        DESCRIPTION: Open 'Deposit' page
        EXPECTED: 
        """
        pass

    def test_002_tap_add_paypal_tab(self):
        """
        DESCRIPTION: Tap 'Add PayPal' tab
        EXPECTED: *   'Add PayPal' tab is selected
        EXPECTED: *   If PayPal account was registered befor the following info is shown at the top of the PayPal page:
        EXPECTED: **Your Registered PayPal Account:**
        EXPECTED: **"email@address.com"**
        """
        pass

    def test_003_verify_quick_deposit_buttons(self):
        """
        DESCRIPTION: Verify quick deposit buttons
        EXPECTED: 1.  Quick deposit buttons are displayed below the '**Add Amount':** label
        EXPECTED: 2.  The following values are shown:
        EXPECTED: *   +5
        EXPECTED: *   +10
        EXPECTED: *   +20
        EXPECTED: *   +50
        EXPECTED: *   +100
        """
        pass

    def test_004_verify_amount_edit_field(self):
        """
        DESCRIPTION: Verify Amount edit field
        EXPECTED: *   'Enter Amount:' label and edit field are present below the quick deposit buttons
        EXPECTED: *   Amount field is empty by default
        """
        pass

    def test_005_verify_deposit_button(self):
        """
        DESCRIPTION: Verify 'Deposit' button
        EXPECTED: - 'Deposit' button is enabled by default
        EXPECTED: - Help text is displayed (if enabled in CMS: Static block) under Deposit button: "Please note: Sometimes we have to complete additional identity verification checks, click here for more information.
        EXPECTED: - Click here coral directs to: https://help.coral.co.uk/s/article/Identity-Verification-C
        """
        pass

    def test_006_verify_set_my_deposit_limits_link(self):
        """
        DESCRIPTION: Verify 'Set my deposit limits' link
        EXPECTED: 'Set my deposit limits' link redirects user to 'My Limits' page
        """
        pass

    def test_007_verify_message_below_the_deposit_button(self):
        """
        DESCRIPTION: Verify message below the 'Deposit' button
        EXPECTED: **"Please note that the PayPal account you register to your Coral account must belong to you and the name details must match our records.”** is shown
        """
        pass

    def test_008_verify_how_to_add_paypal_info_block(self):
        """
        DESCRIPTION: Verify **HOW TO ADD PAYPAL** info block
        EXPECTED: - Info block is displayed underneath ADD PAYPAL tab
        EXPECTED: - Section name and text corresponds to Static Block set in CMS
        """
        pass

    def test_009_verify_live_chat_link(self):
        """
        DESCRIPTION: Verify **Live Chat** link
        EXPECTED: - The **Need Help? Click here to activate Coral Live Chat** link located on the bottom of the page
        """
        pass
