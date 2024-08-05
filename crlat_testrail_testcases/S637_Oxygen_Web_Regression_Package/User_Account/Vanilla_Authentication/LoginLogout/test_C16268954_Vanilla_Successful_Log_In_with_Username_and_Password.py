import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.critical
@pytest.mark.user_account
@vtest
class Test_C16268954_Vanilla_Successful_Log_In_with_Username_and_Password(Common):
    """
    TR_ID: C16268954
    NAME: [Vanilla] Successful Log In with Username and Password
    DESCRIPTION: This test case verifies successful Log In with existing credentials.
    DESCRIPTION: AUTOTEST: [C9689880]
    PRECONDITIONS: User is logged out.
    PRECONDITIONS: **NOTE**: if other pop-up messages are expected after log in then the order of pop-up appearing should be the following:
    PRECONDITIONS: *   Tutorial overlay -> FreeBets -> Odds Boost -> FreeBet expiration message.
    """
    keep_browser_open = True

    def test_001_clicktap_on_log_in_button(self):
        """
        DESCRIPTION: Click/Tap on 'Log In' button
        EXPECTED: 'Log in' pop-up is displayed
        """
        pass

    def test_002_enter_existing_correct_users_username(self):
        """
        DESCRIPTION: Enter existing correct user's 'Username'
        EXPECTED: Username is displayed
        """
        pass

    def test_003_enter_correct_corresponding_password(self):
        """
        DESCRIPTION: Enter correct corresponding 'Password'
        EXPECTED: Entered password is displayed as ******
        """
        pass

    def test_004_clicktap_on_log_in_button(self):
        """
        DESCRIPTION: Click/Tap on 'Log In' button
        EXPECTED: * Log in popup is closed
        EXPECTED: * User is logged in successfully
        EXPECTED: * User Balance is displayed
        EXPECTED: ![](index.php?/attachments/get/34257)
        EXPECTED: * Page from which user made log in is still shown
        """
        pass
