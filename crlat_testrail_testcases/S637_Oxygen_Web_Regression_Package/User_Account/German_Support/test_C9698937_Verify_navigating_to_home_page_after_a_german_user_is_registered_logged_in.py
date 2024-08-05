import pytest
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.tst2
@pytest.mark.stg2
# @pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.other
@vtest
class Test_C9698937_Verify_navigating_to_home_page_after_a_german_user_is_registered_logged_in(Common):
    """
    TR_ID: C9698937
    NAME: Verify navigating to home page after a german user is registered & logged in
    DESCRIPTION: This test case verifies navigating a german user to Home page after login
    DESCRIPTION: NOTE:
    DESCRIPTION: - "signupCountryCode" is received in WS "openapi" response from IMS (for Roxanne only, not valid for OX102 Ladbrokes Wallet)
    DESCRIPTION: - "signupCountryCode" is saved in Application > Local Storage > OX.countryCode
    DESCRIPTION: - "OX.countryCode" value is updated each time a user is logged in (after logout it keeps a value of the last logged in user)
    DESCRIPTION: AUTOTEST [C12676017]
    DESCRIPTION: Test case needs to be updated with new Registration form
    PRECONDITIONS: 1. App is loaded
    PRECONDITIONS: 2. Any page but Home is opened e.g. Football landing page
    """
    keep_browser_open = True

    def test_001_mobiletablettap_loginjoin__join_us_heredesktoptap_join_now(self):
        """
        DESCRIPTION: **Mobile&Tablet:**
        DESCRIPTION: Tap 'Login/Join' > 'Join us here'
        DESCRIPTION: **Desktop:**
        DESCRIPTION: Tap 'Join Now'
        EXPECTED: User is redirected Registration
        """
        pass

    def test_002_register_a_new_german_usernote_country__germany(self):
        """
        DESCRIPTION: Register a new German user
        DESCRIPTION: (Note: "Country" = "Germany")
        EXPECTED: - German user is registered
        """
        pass

    def test_003_finish_registration_and_close_deposit_page(self):
        """
        DESCRIPTION: Finish registration and close 'Deposit' page
        EXPECTED: - User is redirected back to an app
        EXPECTED: - User is redirected to Home page
        """
        pass

    def test_004_log_out_and_clear_local_storage(self):
        """
        DESCRIPTION: Log out and clear local storage
        EXPECTED: - User is logged out
        EXPECTED: - User is redirected to home page
        """
        pass

    def test_005_navigate_to_any_but_home_page_eg_next_races_tab(self):
        """
        DESCRIPTION: Navigate to any but home page e.g. 'Next Races' tab
        EXPECTED: 'Next Races' tab is opened
        """
        pass

    def test_006_log_in_with_a_german_user(self):
        """
        DESCRIPTION: Log in with a German user
        EXPECTED: - User is redirected back to an app
        EXPECTED: - User is redirected to Home page
        """
        pass
