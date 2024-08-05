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
class Test_C17728057_Vanilla_Verify_successful_Deposit_via_PayPal(Common):
    """
    TR_ID: C17728057
    NAME: [Vanilla] Verify successful Deposit via PayPal
    DESCRIPTION: This test case verifies Successful Depositing functionality via PayPal.
    PRECONDITIONS: In CMS > System Configuration > 'Pay Pal' section > 'viaSafeCharge' check box is NOT checked
    PRECONDITIONS: User is logged in
    PRECONDITIONS: User has a valid (unrestricted) PayPal account from which his/her can deposit funds via
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

    def test_004_select_paypal_payment_method(self):
        """
        DESCRIPTION: Select PayPal payment method
        EXPECTED: Deposit page with PayPal payment method is opened
        """
        pass

    def test_005_enter_valid_amount_manually_or_using_quick_deposit_buttons(self):
        """
        DESCRIPTION: Enter valid amount manually or using quick deposit buttons
        EXPECTED: Amount is displayed in Amount edit field
        """
        pass

    def test_006_enter_account_number_in_account_number_field(self):
        """
        DESCRIPTION: Enter Account number in Account number field
        EXPECTED: Account number is displayed
        """
        pass

    def test_007_tap_deposit__amount_button(self):
        """
        DESCRIPTION: Tap 'Deposit * amount' button
        EXPECTED: User is redirected to PayPal page
        """
        pass

    def test_008_login_to_paypal_accountchoose_a_card_for_paymenttap_on_pay_now_button(self):
        """
        DESCRIPTION: Login to PayPal account
        DESCRIPTION: Choose a card for payment
        DESCRIPTION: Tap on 'Pay Now' button
        EXPECTED: 'Your deposit of *amount has been successful' is displayed
        """
        pass

    def test_009_close_deposit_viewcheck_balance_in_the_header(self):
        """
        DESCRIPTION: Close Deposit view
        DESCRIPTION: Check Balance in the header
        EXPECTED: Balance is increased on sum of deposit
        """
        pass
