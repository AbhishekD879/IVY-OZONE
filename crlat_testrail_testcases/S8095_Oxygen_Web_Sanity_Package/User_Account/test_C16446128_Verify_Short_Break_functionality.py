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
class Test_C16446128_Verify_Short_Break_functionality(Common):
    """
    TR_ID: C16446128
    NAME: Verify Short Break functionality
    DESCRIPTION: This test case verifies 'Short Break' functionality
    DESCRIPTION: AUTOTEST [C48173204] mobile
    DESCRIPTION: AUTOTEST [C48473982] desktop
    PRECONDITIONS: Oxygen app is loaded and the user is logged in
    PRECONDITIONS: Navigate to 'My Account' -> 'Gambling Control'
    PRECONDITIONS: 'Gambling Controls' page is opened and 'Deposit Limits' option is selected by default
    PRECONDITIONS: Please note that this feature is handled on GVC side ( text can be changed)
    """
    keep_browser_open = True

    def test_001_select_account_closure__reopening_option(self):
        """
        DESCRIPTION: Select 'Account Closure & Reopening' option.
        EXPECTED: Option is selected and description is changed to 'Select this option if you would like to stop playing on some or all of our products'
        """
        pass

    def test_002_click_choose_button(self):
        """
        DESCRIPTION: Click 'CHOOSE' button.
        EXPECTED: Account Closure options are displayed as radio buttons:
        EXPECTED: - I want to close my account or sections of it.
        EXPECTED: - I’d like to take an irreversible time-out or exclude myself from gaming.
        """
        pass

    def test_003_select_i_want_to_close_my_account_or_sections_of_it_option_and_click_continue_button(self):
        """
        DESCRIPTION: Select 'I want to close my account or sections of it' option and click 'CONTINUE' button.
        EXPECTED: Service Closure page is displayed. It contains the list of products available to the user. Each product has its separate 'CLOSE' button.
        EXPECTED: At the bottom there is a 'CLOSE ALL' button to close all products.
        """
        pass

    def test_004_click_close__button_for_any_of_the_products(self):
        """
        DESCRIPTION: Click 'CLOSE'  button for any of the products.
        EXPECTED: User is taken to the page with the detailed information about service closure.
        """
        pass

    def test_005_select_any_duration_radio_button(self):
        """
        DESCRIPTION: Select any 'Duration' radio button.
        EXPECTED: Duration is selected.
        """
        pass

    def test_006_select_any_reason_for_closure_radio_button(self):
        """
        DESCRIPTION: Select any 'Reason for closure' radio button.
        EXPECTED: Reason is selected.
        """
        pass

    def test_007_click_continue_button(self):
        """
        DESCRIPTION: Click 'CONTINUE' button.
        EXPECTED: User is taken to service closure confirmation page.
        """
        pass

    def test_008_click_close_product_name(self):
        """
        DESCRIPTION: Click 'CLOSE {PRODUCT_NAME}'
        EXPECTED: User is taken back to the page with the list of available products.
        EXPECTED: Information message says: Succesfully closed: {PRODUCT_NAME}.
        EXPECTED: Product is not listed in the list.
        """
        pass

    def test_009_click_close_all_button_at_the_bottom(self):
        """
        DESCRIPTION: Click 'CLOSE ALL' button at the bottom.
        EXPECTED: User is taken to the page with the detailed information about service closure. It lists all the products about to be closed.
        """
        pass

    def test_010_select_any_duration_and_reason_for_closure_radio_buttons(self):
        """
        DESCRIPTION: Select any 'Duration' and 'Reason for closure' radio buttons.
        EXPECTED: Duration and reason are selected.
        """
        pass

    def test_011_click_continue_button(self):
        """
        DESCRIPTION: Click 'CONTINUE' button.
        EXPECTED: User is taken to service closure confirmation page.
        """
        pass

    def test_012_click_close_my_account_button(self):
        """
        DESCRIPTION: Click 'CLOSE MY ACCOUNT' button.
        EXPECTED: User is taken back to the page with the list of available products.
        EXPECTED: Information message says: Succesfully closed: {LIST OF ALL CLOSED PRODUCTS}.
        """
        pass

    def test_013_go_back_to_account_closure_options(self):
        """
        DESCRIPTION: Go back to Account Closure options.
        EXPECTED: Select new option in the list: "I want to reopen account or sections of it"
        """
        pass

    def test_014_click_continue_button(self):
        """
        DESCRIPTION: Click 'CONTINUE' button.
        EXPECTED: Screen with the list of all the products is displayed as 'closed' with red circles.
        EXPECTED: Below status there is an information until when those products are closed.
        """
        pass
