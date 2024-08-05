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
class Test_C28243_Decline_New_Terms_and_Conditions(Common):
    """
    TR_ID: C28243
    NAME: Decline New Terms and Conditions
    DESCRIPTION: This test case verifies declining new terms and conditions.
    DESCRIPTION: **Jira ticket**: BMA-3725
    PRECONDITIONS: *   Terms & Conditions have been changed
    PRECONDITIONS: **NOTE**: if other pop-up messages are expected after log in then the order of pop-up appearing should be the following:
    PRECONDITIONS: *   Terms and Conditions -> Verify Your Account (Netverify) -> Deposit Limits -> Quick Deposit
    """
    keep_browser_open = True

    def test_001_load_oxygen_app(self):
        """
        DESCRIPTION: Load Oxygen app
        EXPECTED: 
        """
        pass

    def test_002_tap_log_in_button(self):
        """
        DESCRIPTION: Tap 'Log In' button
        EXPECTED: Log In pop-up opens
        """
        pass

    def test_003_fill_in_username_and_password_fields_with_correct_data___click_login_button(self):
        """
        DESCRIPTION: Fill in 'Username...' and 'Password...' fields with correct data -> Click 'Login' button
        EXPECTED: 'Terms & Conditions' pop-up window is shown with a message asking the user to accept new T&C
        """
        pass

    def test_004_tap_view_terms_button(self):
        """
        DESCRIPTION: Tap 'View Terms' button
        EXPECTED: Terms & Conditions is opened in a separate browser tab
        """
        pass

    def test_005_navigate_back_to_application_and_do_not_accept_new_tc(self):
        """
        DESCRIPTION: Navigate back to application and do NOT accept new T&C
        EXPECTED: It is NOT possible to log in without accepting new T&C
        EXPECTED: It is NOT possible to place a bet without accepting new T&C
        """
        pass
