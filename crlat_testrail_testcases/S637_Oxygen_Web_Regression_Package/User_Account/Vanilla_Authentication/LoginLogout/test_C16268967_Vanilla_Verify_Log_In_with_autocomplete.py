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
class Test_C16268967_Vanilla_Verify_Log_In_with_autocomplete(Common):
    """
    TR_ID: C16268967
    NAME: [Vanilla] Verify Log In with autocomplete
    DESCRIPTION: This test case verifies Log In with existing credentials by autocomplete.
    PRECONDITIONS: 1. Credentials are saved by the user for the ability to login by autocomplete
    PRECONDITIONS: 2. User is logged out
    PRECONDITIONS: **NOTE**: if other pop-up messages are expected after log in then the order of pop-up appearing should be the following:
    PRECONDITIONS: * Tutorial overlay -> FreeBets -> Odds Boost -> FreeBet expiration message.
    """
    keep_browser_open = True

    def test_001_clicktap_on_log_in_button(self):
        """
        DESCRIPTION: Click/Tap on 'Log In' button
        EXPECTED: 'Log in' pop-up is displayed
        """
        pass

    def test_002_tap_within_username_field_and_select_existing_users_username_see_preconditions(self):
        """
        DESCRIPTION: Tap within 'Username' field and select existing user's 'Username' (see preconditions)
        EXPECTED: * 'Username' and 'Password' fields are auto-filled with data
        EXPECTED: * 'Log In' button is enabled
        """
        pass

    def test_003_clicktap_on_log_in_button(self):
        """
        DESCRIPTION: Click/Tap on 'Log In' button
        EXPECTED: * Log in popup is closed
        EXPECTED: * User is logged in successfully
        EXPECTED: * User Balance is displayed
        EXPECTED: * Page from which user made log in is still shown
        """
        pass
