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
class Test_C44870131_Verify_new_user_can_add_multiple_payment_methods_and_deposit_money(Common):
    """
    TR_ID: C44870131
    NAME: Verify new user can add multiple payment methods and deposit money
    DESCRIPTION: Note: For test accounts only Master card, Visa & Maestro are available.
    PRECONDITIONS: User is registered.
    PRECONDITIONS: In order to get number of credit card the following links can be used:
    PRECONDITIONS: http://www.getcreditcardnumbers.com/how-to-get-a-master-card-credit-card
    PRECONDITIONS: http://www.getcreditcardnumbers.com/how-to-get-a-visa-credit-card
    """
    keep_browser_open = True

    def test_001_tap_on_the_balance_or_avataron_the_top_right_of_the_appwebtap_deposit_button_on_the_bottom_of_the_page(self):
        """
        DESCRIPTION: Tap on the 'Balance' or 'Avatar'on the top right of the App/Web
        DESCRIPTION: Tap 'Deposit' button on the bottom of the page
        EXPECTED: My Balance & Menu is opened respectively.
        EXPECTED: 'Deposit' page is opened
        """
        pass

    def test_002_select_payment_option_page_is_displayed_with_following_fields(self):
        """
        DESCRIPTION: Select payment option page is displayed with following fields
        EXPECTED: VISA/MASTERCARD/MAESTRO are available
        """
        pass

    def test_003_verify_adding_of_visa_card_tap_visafill_in_all_required_fields_and_tap_deposit_button(self):
        """
        DESCRIPTION: Verify adding of '**Visa**' card (Tap 'VISA')
        DESCRIPTION: Fill in all required fields and tap 'Deposit' button
        EXPECTED: Deposit page with Visa card payment method is opened
        EXPECTED: Successful message: **"Your deposit of <currency symbol> XX.XX was successful.
        """
        pass

    def test_004_click_okverify_user_balance(self):
        """
        DESCRIPTION: click "OK"
        DESCRIPTION: Verify user Balance
        EXPECTED: User is taken to homepage
        EXPECTED: Balance is increased on sum of deposit
        """
        pass

    def test_005_tap_deposit_button_on_the_bottom_of_the_pageclick_on_the_down_arrow_located_next_to_the_current_card_number(self):
        """
        DESCRIPTION: Tap 'Deposit' button on the bottom of the page
        DESCRIPTION: Click on the Down arrow located next to the Current card number
        EXPECTED: 'Deposit' page is opened with Amount/Card number/ CVV etc
        EXPECTED: 'Other payment options' available.
        """
        pass

    def test_006_click_on_other_payment_options_to_add_a_new_card(self):
        """
        DESCRIPTION: Click on 'Other payment options' to add a new card
        EXPECTED: VISA/MASTERCARD/MAESTRO are available
        """
        pass

    def test_007_verify_adding_and_depositing_via_master_card_cardverify_user_balance(self):
        """
        DESCRIPTION: Verify adding and depositing via '**Master Card**' card
        DESCRIPTION: Verify user Balance
        EXPECTED: User is able to add the Master card.
        EXPECTED: Successful message: **"Your deposit of <currency symbol> XX.XX was successful.
        EXPECTED: Balance is increased on sum of deposit.
        """
        pass

    def test_008_tap_on_the_balance_or_avataron_the_top_right_of_the_appwebtap_deposit_button_on_the_bottom_of_the_page(self):
        """
        DESCRIPTION: Tap on the 'Balance' or 'Avatar'on the top right of the App/Web
        DESCRIPTION: Tap 'Deposit' button on the bottom of the page
        EXPECTED: 'Deposit' page is opened
        """
        pass

    def test_009_and_now_click_on_all_options_on_the_deposit_cashier_page(self):
        """
        DESCRIPTION: and now click on "All options" on the Deposit cashier page
        EXPECTED: Page with all options of cards are available.
        EXPECTED: Eg: VISA/MASTERCARD/MAESTRO are available
        """
        pass

    def test_010_verify_adding_and_depositing_via_maestro_cardverify_user_balance(self):
        """
        DESCRIPTION: Verify adding and depositing via '**Maestro**' card.
        DESCRIPTION: Verify user Balance
        EXPECTED: User is able to add the Maestro card.
        EXPECTED: Successful message: **"Your deposit of <currency symbol> XX.XX was successful.
        EXPECTED: Balance is increased on sum of deposit.
        """
        pass
