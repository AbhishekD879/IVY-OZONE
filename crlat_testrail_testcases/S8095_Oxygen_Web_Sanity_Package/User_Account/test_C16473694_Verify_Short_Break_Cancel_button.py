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
class Test_C16473694_Verify_Short_Break_Cancel_button(Common):
    """
    TR_ID: C16473694
    NAME: Verify Short Break 'Cancel' button
    DESCRIPTION: This test case verifies 'Short Break' 'Cancel' button.
    PRECONDITIONS: Oxygen app is loaded and the user is logged in
    PRECONDITIONS: Navigate to 'My Account' -> 'Settings' -> 'Gambling Control'
    PRECONDITIONS: 'Gambling Controls' page is opened and 'Deposit Limits' option is selected by default
    """
    keep_browser_open = True

    def test_001_select_account_closure_option(self):
        """
        DESCRIPTION: Select 'Account Closure' option.
        EXPECTED: Option is selected and description is changed to 'Select this option if you would like to stop playing on some or all of our products'
        """
        pass

    def test_002_click_choose_button(self):
        """
        DESCRIPTION: Click 'CHOOSE' button.
        EXPECTED: Account Closure options are displayed as radio buttons:
        EXPECTED: - I’d like to close my account
        EXPECTED: - I’d like to take an irreversible time-out or exclude myself from gaming.
        """
        pass

    def test_003_click_cancel_button(self):
        """
        DESCRIPTION: Click 'CANCEL' button.
        EXPECTED: User returns to Gambling Controls page.
        EXPECTED: 'Deposit Limits' option is selected by default.
        """
        pass

    def test_004_select_account_closure_option_and_click_choose_button(self):
        """
        DESCRIPTION: Select 'Account Closure' option and click 'CHOOSE' button.
        EXPECTED: Account Closure options are displayed as radio buttons:
        EXPECTED: - I’d like to close my account
        EXPECTED: - I’d like to take an irreversible time-out or exclude myself from gaming.
        """
        pass

    def test_005_select_id_like_to_take_a_short_break_option_and_click_continue_button(self):
        """
        DESCRIPTION: Select 'I’d like to take a short break' option and click 'CONTINUE' button.
        EXPECTED: Service Closure page is displayed. It contains the list of products available to the user. Each product has its separate 'CLOSE' button.
        EXPECTED: At the bottom there is a 'CLOSE ALL' button to close all products.
        """
        pass

    def test_006_click_close__button_for_any_of_the_products(self):
        """
        DESCRIPTION: Click 'CLOSE'  button for any of the products.
        EXPECTED: User is taken to the page with the detailed information about service closure.
        """
        pass

    def test_007_click_cancel_button(self):
        """
        DESCRIPTION: Click 'CANCEL' button.
        EXPECTED: User returns to Gambling Controls page.
        EXPECTED: 'Deposit Limits' option is selected by default.
        """
        pass

    def test_008_repeat_steps_4_6(self):
        """
        DESCRIPTION: Repeat steps 4-6.
        EXPECTED: User is taken to the page with the detailed information about service closure.
        """
        pass

    def test_009_select_any_duration_radio_button(self):
        """
        DESCRIPTION: Select any 'Duration' radio button.
        EXPECTED: Duration is selected.
        """
        pass

    def test_010_select_any_reason_for_closure_radio_button(self):
        """
        DESCRIPTION: Select any 'Reason for closure' radio button.
        EXPECTED: Reason is selected.
        """
        pass

    def test_011_click_continue_button(self):
        """
        DESCRIPTION: Click 'CONTINUE' button.
        EXPECTED: Service Closure confirmation page is displayed.
        """
        pass

    def test_012_click_cancel_button(self):
        """
        DESCRIPTION: Click 'CANCEL' button.
        EXPECTED: User returns to Gambling Controls page.
        EXPECTED: 'Deposit Limits' option is selected by default.
        """
        pass
