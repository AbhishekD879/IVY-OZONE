import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.other
@vtest
class Test_C17723970_Vanilla_Verify_successful_Deposit_via_Neteller(Common):
    """
    TR_ID: C17723970
    NAME: [Vanilla] Verify successful Deposit via Neteller
    DESCRIPTION: This test case verifies Successful Depositing functionality via NETELLER.
    PRECONDITIONS: User is logged in
    PRECONDITIONS: User has a valid NETELLER account from which they can deposit funds from
    PRECONDITIONS: Balance is enough for deposit from
    PRECONDITIONS: Confluence page for payments test data https://confluence.egalacoral.com/display/SPI/GVC+Payment+Methods
    """
    keep_browser_open = True

    def test_001_click_on_user_avatar_icon_on_the_header(self):
        """
        DESCRIPTION: Click on User "Avatar" icon on the header
        EXPECTED: User menu is opened
        """
        pass

    def test_002_click_on_cashier_section_in_user_menu(self):
        """
        DESCRIPTION: Click on "Cashier" section in User menu
        EXPECTED: Cashier Menu is opened and "Deposit" section is present in the list
        """
        pass

    def test_003_click_on_deposit_section(self):
        """
        DESCRIPTION: Click on "Deposit" section
        EXPECTED: "Deposit" menu is opened with a list of all available payment methods for the User;
        EXPECTED: VISA
        EXPECTED: MasterCard
        EXPECTED: Netteller
        EXPECTED: Maestro
        EXPECTED: PayPal
        EXPECTED: etc.
        """
        pass

    def test_004_select_neteller_payment_method(self):
        """
        DESCRIPTION: Select Neteller payment method
        EXPECTED: Deposit page with Neteller payment method is opened
        """
        pass

    def test_005_enter_valid_account_or_email_into_account_idemail_field(self):
        """
        DESCRIPTION: Enter valid Account or Email into 'Account ID/Email:' field
        EXPECTED: Account/Email is displayed
        """
        pass

    def test_006_enter_valid_security_id_into_secure_id_or_authentication_code_field(self):
        """
        DESCRIPTION: Enter valid Security ID into 'Secure ID or Authentication Code:' field
        EXPECTED: Secure ID or Authentication Code is displayed
        """
        pass

    def test_007_enter_valid_amount_manually_or_using_quick_deposit_buttons(self):
        """
        DESCRIPTION: Enter valid amount manually or using quick deposit buttons
        EXPECTED: Amount is displayed in Amount edit field
        """
        pass

    def test_008_tap_deposit_button(self):
        """
        DESCRIPTION: Tap 'Deposit' button
        EXPECTED: Successful message: 'Your deposit of <currency symbol> XX.XX was successful' is displayed
        """
        pass

    def test_009_close_deposit_viewcheck_balance_in_the_header(self):
        """
        DESCRIPTION: Close Deposit view
        DESCRIPTION: Check Balance in the header
        EXPECTED: Balance is increased on sum of deposit
        """
        pass
