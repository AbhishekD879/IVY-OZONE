import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.retail
@vtest
class Test_C2861363_Verify_SMS_parsing_has_been_removed_for_Android(Common):
    """
    TR_ID: C2861363
    NAME: Verify SMS parsing has been removed for Android
    DESCRIPTION: This test case verifies that SMS parsing has been removed and user has to manually enter the authorization code to create an account.
    DESCRIPTION: Platform: Android
    PRECONDITIONS: Android phone with a UK sim card is available.
    PRECONDITIONS: Coral Connect app is installed.
    PRECONDITIONS: For Debug build:
    PRECONDITIONS: In the app settings on the top right corner, choose the environment (prod or stg).
    PRECONDITIONS: Deselect Debug SMS and Apply.
    """
    keep_browser_open = True

    def test_001_tap_log_in_on_the_top_right_corner___create_account(self):
        """
        DESCRIPTION: Tap Log in on the top right corner - Create Account
        EXPECTED: Prompt appears to enter your mobile number
        """
        pass

    def test_002_enter_the_mobile_numbertap_next(self):
        """
        DESCRIPTION: Enter the mobile number.
        DESCRIPTION: Tap next.
        EXPECTED: A message appears :
        EXPECTED: We are sending you a device authorization code to {mobile number}
        """
        pass

    def test_003_tap_ok_send(self):
        """
        DESCRIPTION: Tap OK Send
        EXPECTED: A message appears as follows:
        EXPECTED: We sent you a code by SMS.
        EXPECTED: Enter authorization code.
        """
        pass

    def test_004_check_your_messages_for_the_codemanually_enter_the_codetap_enter(self):
        """
        DESCRIPTION: Check your messages for the code.
        DESCRIPTION: Manually enter the code.
        DESCRIPTION: Tap Enter.
        EXPECTED: The code is accepted.
        """
        pass

    def test_005_tap_nextenter_your_4_digit_pin_numbertap_finish(self):
        """
        DESCRIPTION: Tap Next
        DESCRIPTION: Enter your 4-digit pin number
        DESCRIPTION: Tap Finish
        EXPECTED: Your pin is accepted and account created successfully.
        """
        pass
