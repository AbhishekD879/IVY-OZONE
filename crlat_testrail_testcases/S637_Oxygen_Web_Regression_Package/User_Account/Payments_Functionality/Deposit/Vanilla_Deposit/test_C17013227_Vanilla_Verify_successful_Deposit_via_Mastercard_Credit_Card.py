import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.other
@vtest
class Test_C17013227_Vanilla_Verify_successful_Deposit_via_Mastercard_Credit_Card(Common):
    """
    TR_ID: C17013227
    NAME: [Vanilla] Verify successful Deposit via  Mastercard Credit Card
    DESCRIPTION: This test case verifies successful deposit functionality for Mastercard payment method
    DESCRIPTION: [C29507202]
    DESCRIPTION: [C28967699]
    PRECONDITIONS: User has registered supported cards(e.g Mastercard);
    PRECONDITIONS: Balance of card is enough for deposit from;
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

    def test_002_click_on_banking_section_in_user_menu(self):
        """
        DESCRIPTION: Click on "Banking" section in User menu
        EXPECTED: Cashier Menu is opened and "Deposit" section is present in the list
        """
        pass

    def test_003_click_on_deposit_section(self):
        """
        DESCRIPTION: Click on "Deposit" section
        EXPECTED: "Deposit" menu is opened with a list of all available payment methods for the User:
        EXPECTED: VISA
        EXPECTED: MasterCard
        EXPECTED: Netteller
        EXPECTED: etc.
        EXPECTED: Note: for test users Deposit page with Mastercard payment method is opened
        """
        pass

    def test_004_select_mastercard_payment_method(self):
        """
        DESCRIPTION: Select Mastercard payment method
        EXPECTED: Deposit page with Mastercard payment method is opened
        """
        pass

    def test_005_enter_valid_cv2_into_cv2_field(self):
        """
        DESCRIPTION: Enter valid CV2 into CV2 field
        EXPECTED: CV2 is entered.
        """
        pass

    def test_006_enter_valid_amount_manually_or_using_plus___buttons(self):
        """
        DESCRIPTION: Enter valid amount manually or using '+', '-' buttons
        EXPECTED: Amount is displayed in Amount edit field
        """
        pass

    def test_007_tap_deposit_button(self):
        """
        DESCRIPTION: Tap 'Deposit' button
        EXPECTED: Successful message: 'Your deposit of <currency symbol> XX.XX has been successful' appears
        EXPECTED: Also, Deposit view closed automatically
        """
        pass

    def test_008_check_balance_in_the_header(self):
        """
        DESCRIPTION: Check Balance in the header
        EXPECTED: Balance is increased on sum of deposit
        """
        pass
