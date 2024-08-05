import pytest
from tests.base_test import vtest
from tests.Common import Common


# @pytest.mark.lad_tst2  # VANO-1483, BMA-52554
# @pytest.mark.lad_stg2
# @pytest.mark.lad_prod
# @pytest.mark.lad_hl
@pytest.mark.medium
@pytest.mark.other
@pytest.mark.desktop
@pytest.mark.registration
@pytest.mark.login
@vtest
class Test_C9698937_Verify_German_User_Is_Registered_And_Logged_In(Common):
    """
    TR_ID: C9698937
    NAME: Verify navigating to home page after a german user is registered & logged in
    DESCRIPTION: This test case verifies navigating a german user to Home page after login
    DESCRIPTION: NOTE:
    DESCRIPTION: - "signupCountryCode" is received in WS "openapi" response from IMS
    DESCRIPTION: - "signupCountryCode" is saved in Application > Local Storage > OX.countryCode
    DESCRIPTION: - "OX.countryCode" value is updated each time a user is logged in (after logout it keeps a value of the last logged in user)
    PRECONDITIONS: 1. App is loaded
    PRECONDITIONS: 2. Any page but Home is opened e.g. Football landing page
    """
    keep_browser_open = True

    def test_001_navigate_to_registration_page(self):
        """
        DESCRIPTION: **Mobile&Tablet:**
        DESCRIPTION: Tap 'Login/Join' > 'Join us here'
        DESCRIPTION: **Desktop:**
        DESCRIPTION: Tap 'Join Now'
        EXPECTED: User is redirected Registration
        """
        self.__class__.is_mobile = False if self.device_type == 'desktop' else True
        self.__class__.german_username = self.generate_user()
        self.site.register_new_user(country='Germany', state='Hamburg', post_code='60306',
                                    username=self.german_username,
                                    city='Hamburg', currency='EUR',
                                    mobile='+4915735987904')

    def test_002_in_account_one_register_a_new_german_user(self):
        """
        DESCRIPTION: Register a new German user
        DESCRIPTION: (Note: "Country" = "Germany")
        EXPECTED: - German user is registered
        """
        # Done in the scope of step 1

    def test_003_in_account_one_save_preferences_and_close_deposit_page(self):
        """
        DESCRIPTION: Finish registration and close 'Deposit' page
        EXPECTED: - User is redirected back to an app
        EXPECTED: - User is redirected to Home page
        """
        # Done in the scope of step 1

    def test_004_log_out(self):
        """
        DESCRIPTION: Log out and clear local storage
        EXPECTED: - User is logged out
        EXPECTED: - User is redirected to home page
        """
        self.site.logout()
        self.delete_cookies()
        self.device.refresh_page()
        self.site.wait_splash_to_hide()
        homepage = self.site.wait_content_state('Homepage')
        self.assertTrue(homepage, msg='User not on home page')

    def test_005_navigate_to_any_but_home_page(self):
        """
        DESCRIPTION: Navigate to any but home page e.g. 'Next Races' tab
        EXPECTED: 'Next Races' tab is opened
        """
        self.site.open_sport(name=self.get_sport_title(self.ob_config.horseracing_config.category_id))

    def test_006_log_in_with_a_german_user(self):
        """
        DESCRIPTION: Log in with a German user
        EXPECTED: - User is redirected back to an app
        EXPECTED: - User is redirected to Home page
        """
        self.site.login(username=self.german_username)
        homepage = self.site.wait_content_state('Homepage')
        self.assertTrue(homepage, msg='User not on home page')
