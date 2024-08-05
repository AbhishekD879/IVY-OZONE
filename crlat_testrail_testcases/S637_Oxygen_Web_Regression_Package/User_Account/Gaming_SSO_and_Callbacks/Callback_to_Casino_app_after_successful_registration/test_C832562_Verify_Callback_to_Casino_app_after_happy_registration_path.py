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
class Test_C832562_Verify_Callback_to_Casino_app_after_happy_registration_path(Common):
    """
    TR_ID: C832562
    NAME: Verify Callback to Casino app after happy registration path
    DESCRIPTION: This test case verifies the functionality of a callback to Casino after happy completion of the BMA registration
    PRECONDITIONS: *   User should be logged out
    PRECONDITIONS: *   No open tabs with BMA app should be present
    PRECONDITIONS: The general rule should be: if there is no cbURL attribute the stay within the BMA app, if there is a cbURL then take the user to the URL in a separate tab.
    PRECONDITIONS: BMA-5238
    PRECONDITIONS: **Choosing the password should include following rules:**
    PRECONDITIONS: * At least 8 characters;
    PRECONDITIONS: * Uppercase and lowercase letters;
    PRECONDITIONS: * Numbers and symbols
    """
    keep_browser_open = True

    def test_001_call_url_httpsbma_urlsignupcburlcasino_urleghttpsinvictuscoralcouksignupcburlhttpmcasino_tst2coralcouk(self):
        """
        DESCRIPTION: Call URL https://BMA_url/#/**signup?cbURL=**<Casino_url>
        DESCRIPTION: (e.g.  https://invictus.coral.co.uk/#/signup?cbURL=http://mcasino-tst2.coral.co.uk)
        EXPECTED: Invictus registration form appears
        EXPECTED: Page 'Join Us - Step 1 of  2' is shown
        """
        pass

    def test_002_enter_correct_data_to_all_required_fields_due_to_validation_rules(self):
        """
        DESCRIPTION: Enter correct data to all required fields due to validation rules
        EXPECTED: All mandatory fields are filled.
        EXPECTED: None of fields are highlighted in red
        """
        pass

    def test_003_tap_go_to_step_2_button(self):
        """
        DESCRIPTION: Tap 'Go to Step 2' button
        EXPECTED: Page 'Join Us - Step 2 of 2' is shown
        """
        pass

    def test_004_enter_correct_data_to_all_required_fields_due_to_validation_rules(self):
        """
        DESCRIPTION: Enter correct data to all required fields due to validation rules
        EXPECTED: All mandatory fields are filled.
        EXPECTED: None of fields are highlihted in red
        """
        pass

    def test_005_tap_complete_registration_button(self):
        """
        DESCRIPTION: Tap 'Complete Registration' button
        EXPECTED: * Registration is successfully completed
        EXPECTED: * Add debit/credit cards tab is opened
        """
        pass

    def test_006_fill_valid_credit_card_number_expiration_date_and_tap_on_submit_button(self):
        """
        DESCRIPTION: Fill valid credit card number, expiration date and tap on 'submit' button
        EXPECTED: Card is validated
        EXPECTED: User is redirected to Deposit > My payments tab
        """
        pass

    def test_007_enter_an_amount_eg_10enter_a_cv2_eg_123click_on_deposit(self):
        """
        DESCRIPTION: Enter an amount (e.g. 10£)
        DESCRIPTION: Enter a CV2 (e.g. 123)
        DESCRIPTION: Click on Deposit
        EXPECTED: The protection of funds pop-up is displayed. The text message is correct.
        EXPECTED: E.g.: "We hold your money in an independent trust account to ensure that it is completely protected. This meets the UK Gambling Commission's requirement for the protection of customer funds at the HIGH LEVEL of protection. For further information, you can visit the Gambling Commission's web site by "
        """
        pass

    def test_008_click_on_accept_button(self):
        """
        DESCRIPTION: Click on 'ACCEPT' button
        EXPECTED: * Funds are debited
        EXPECTED: * User is redirected to Casino application (e.g. http://mcasino-tst2.coral.co.uk)
        EXPECTED: * User is logged in there automatically
        """
        pass

    def test_009_observe_the_balance_of_the_account(self):
        """
        DESCRIPTION: Observe the balance of the account
        EXPECTED: The balance is correctly updated within seconds
        """
        pass

    def test_010_log_outrepeat_steps_1_5(self):
        """
        DESCRIPTION: Log out
        DESCRIPTION: Repeat steps #1-5
        EXPECTED: 
        """
        pass

    def test_011_tap_on_cancel_button(self):
        """
        DESCRIPTION: Tap on 'cancel' button
        EXPECTED: Deposit > Add debit/credit cards tab is closed
        EXPECTED: User comes back to casino homepage
        """
        pass
