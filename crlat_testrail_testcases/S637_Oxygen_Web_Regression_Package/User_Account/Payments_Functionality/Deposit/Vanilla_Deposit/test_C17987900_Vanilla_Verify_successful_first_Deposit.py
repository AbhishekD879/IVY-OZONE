import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.critical
@pytest.mark.other
@vtest
class Test_C17987900_Vanilla_Verify_successful_first_Deposit(Common):
    """
    TR_ID: C17987900
    NAME: [Vanilla] Verify successful first Deposit
    DESCRIPTION: This test case verifies successful first deposit flow using any of supported payment methods
    DESCRIPTION: AUTOTEST [C23137726] [C23137732]
    PRECONDITIONS: User has no registered any cards and user balance is 0.
    PRECONDITIONS: User logged into the application;
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
        EXPECTED: e.g:
        EXPECTED: VISA
        EXPECTED: MasterCard
        EXPECTED: etc.
        """
        pass

    def test_004_select_any_payment_method_eg_mastercard(self):
        """
        DESCRIPTION: Select any payment method (e.g. MasterCard)
        EXPECTED: Deposit page with selected(e.g. MasterCard) payment method is opened
        """
        pass

    def test_005_enter_credit_card_number_eg_5137658844677245(self):
        """
        DESCRIPTION: Enter credit card number (e.g. 5137658844677245)
        EXPECTED: card number is entered. Green tick appears in card number field
        """
        pass

    def test_006_enter_credit_card_name(self):
        """
        DESCRIPTION: Enter credit card name
        EXPECTED: card name is entered. Name tick appears in card name field
        """
        pass

    def test_007_enter_expiry_date(self):
        """
        DESCRIPTION: Enter Expiry date
        EXPECTED: The expiry date is entered. Green tick appears in the Expiry date field
        """
        pass

    def test_008_enter_valid_cv2_into_cv2_field(self):
        """
        DESCRIPTION: Enter valid CV2 into CV2 field
        EXPECTED: CV2 is entered. Green tick appears in CV2 field
        """
        pass

    def test_009_enter_valid_amount_manually_or_using_plus___buttons(self):
        """
        DESCRIPTION: Enter valid amount manually or using '+', '-' buttons
        EXPECTED: Amount is displayed in Amount edit field
        """
        pass

    def test_010_tap_deposit_button(self):
        """
        DESCRIPTION: Tap 'Deposit' button
        EXPECTED: Successfull message: 'Your deposit of <currency symbol> XX.XX has been successful' appears
        """
        pass

    def test_011_close_deposit_viewcheck_balance_in_the_header(self):
        """
        DESCRIPTION: Close Deposit view
        DESCRIPTION: Check Balance in the header
        EXPECTED: Balance is increased on sum of deposit
        """
        pass
