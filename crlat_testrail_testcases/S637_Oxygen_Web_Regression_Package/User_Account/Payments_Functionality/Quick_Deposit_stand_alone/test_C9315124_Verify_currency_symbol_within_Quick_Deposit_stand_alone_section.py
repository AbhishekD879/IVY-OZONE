import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.high
@pytest.mark.user_account
@vtest
class Test_C9315124_Verify_currency_symbol_within_Quick_Deposit_stand_alone_section(Common):
    """
    TR_ID: C9315124
    NAME: Verify currency symbol within 'Quick Deposit' stand alone section
    DESCRIPTION: This test case verifies currency symbol within 'Quick Deposit' stand alone section
    DESCRIPTION: Autotests:
    DESCRIPTION: Mobile - C16473747
    PRECONDITIONS: 1. Make sure you have users with next currency:
    PRECONDITIONS: 'GBP': symbol = £;
    PRECONDITIONS: 'USD': symbol = $;
    PRECONDITIONS: 'EUR': symbol = €;
    PRECONDITIONS: 2. Users have the cards added to its account
    PRECONDITIONS: 3. Application is loaded
    PRECONDITIONS: 4. 'Quick Deposit' stand alone is opened (open 'Right' menu > tap on 'Deposit' button)
    """
    keep_browser_open = True

    def test_001_log_in_with_user_that_has_gbp_currency(self):
        """
        DESCRIPTION: Log in with user that has 'GBP' currency
        EXPECTED: User is logged in
        """
        pass

    def test_002_open_right_menu__tap_on_deposit_button(self):
        """
        DESCRIPTION: Open 'Right' menu > tap on 'Deposit' button
        EXPECTED: 'Quick Deposit' stand alone is opened
        """
        pass

    def test_003_verify_default_label_shown_within_the_deposit_amount_field(self):
        """
        DESCRIPTION: Verify default label shown within the 'Deposit Amount' field
        EXPECTED: Default label is '<currency symbol> 5 Min'
        EXPECTED: ![](index.php?/attachments/get/36329)
        EXPECTED: ---
        EXPECTED: <currency symbol> is shown according to chosen currency
        """
        pass

    def test_004_enter_valid_value_into_cvv_field(self):
        """
        DESCRIPTION: Enter valid value into 'CVV' field
        EXPECTED: 'CVV' field is populated with an entered value
        """
        pass

    def test_005_enter_less_than_minimum_allowed_value_into_deposit_amount_field(self):
        """
        DESCRIPTION: Enter less than minimum allowed value into 'Deposit Amount' field
        EXPECTED: 'Deposit Amount' field is populated with an entered value
        """
        pass

    def test_006_verify_currency_shown_along_with_the_input_in_the_deposit_amount_field(self):
        """
        DESCRIPTION: Verify currency shown along with the input in the 'Deposit Amount' field
        EXPECTED: 'GBP' currency/pound symbol is displayed in 'Deposit Amount' field
        """
        pass

    def test_007_tap_deposit(self):
        """
        DESCRIPTION: Tap 'Deposit'
        EXPECTED: Error message is displayed below 'Deposit Amount' field:
        EXPECTED: "The minimum deposit amount is <currency symbol> 5"
        EXPECTED: ![](index.php?/attachments/get/36330)
        """
        pass

    def test_008_close_quick_deposit__log_out_of_app(self):
        """
        DESCRIPTION: Close 'Quick Deposit' > Log out of app
        EXPECTED: User is logged out
        """
        pass

    def test_009_log_in_with_user_that_has_usd_currency_and_repeat_steps_2_7(self):
        """
        DESCRIPTION: Log in with user that has 'USD' currency and repeat steps #2-7
        EXPECTED: Expected results for steps #6,#7 reproduce with the dollar symbol
        """
        pass

    def test_010_log_in_with_user_that_has_eur_currency_and_repeat_steps_2_7(self):
        """
        DESCRIPTION: Log in with user that has 'EUR' currency and repeat steps #2-7
        EXPECTED: Expected results for steps #6,#7 reproduce with the euro symbol
        """
        pass
