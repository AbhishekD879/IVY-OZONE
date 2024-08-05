import pytest
import tests
from tests.Common import Common
from tests.base_test import vtest


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.hl
@pytest.mark.user_account
@pytest.mark.vip
@pytest.mark.desktop
@pytest.mark.safari
@pytest.mark.low
@pytest.mark.login
@vtest
@pytest.mark.issue('https://jira.egalacoral.com/browse/VANO-1001')
class Test_C52638_Verify_Vip_level_setting_in_Local_Storage_after_login(Common):
    """
    TR_ID: C52638
    NAME: Verify Vip level setting in Local Storage after login
    DESCRIPTION: This test case verifies that user's vip level is set in Local Storage after login
    PRECONDITIONS: 1. Load app and clear all cookies and local storage
    PRECONDITIONS: 2. User's Vip level can be checked in User Menu
    """
    keep_browser_open = True

    vip_level_users = None
    cookie_name = 'OX.vipLevel'
    cookie_value = None
    username = None
    vip_level = None

    def test_000_preconditions(self):
        """
        DESCRIPTION: Prepare user data
        """
        self.__class__.username = tests.settings.betplacement_user

        self.__class__.vip_level = '10' if self.brand == 'ladbrokes' else '9'

        if self.brand == 'ladbrokes':
            self.__class__.vip_level_users = {tests.settings.bronze_user_vip_level_11: '59'
                                              if tests.settings.backend_env == 'prod' else '10',
                                              tests.settings.platinum_user_vip_level_14: '81'
                                              }
        else:
            self.__class__.vip_level_users = {tests.settings.bronze_user_vip_level_11: '11',
                                              tests.settings.platinum_user_vip_level_14: '12'
                                              }

    def test_001_log_in(self):
        """
        DESCRIPTION: Log in
        EXPECTED: User is successfully logged in
        """
        self.site.login(username=self.username, async_close_dialogs=False)
        self._logger.info(
            f'*** Verifying Vip level setting in Local Storage with user "{self.username}" and level "{self.vip_level}"')

    def test_002_check_oxviplevel_correct_value_displaying_in_local_storage(self):
        """
        DESCRIPTION: Check 'OX.vipLevel' correct value displaying in Local Storage
        EXPECTED: 'OX.vipLevel' value = Casino VIP level
        """
        self.__class__.cookie_value = self.get_local_storage_cookie_value_as_dict(self.cookie_name)
        # TODO bug VANO-1001
        self.softAssert(self.assertEqual, self.cookie_value, self.vip_level,
                        msg=f'Cookie value for vip level user "{self.vip_level}" is "{self.cookie_value}"')

    def test_003_refresh_the_page(self):
        """
        DESCRIPTION: Refresh the page
        """
        self.device.refresh_page()
        self.site.wait_splash_to_hide()
        self.site.wait_logged_in()

    def test_004_check_oxviplevel_value_displaying_in_local_storage(self):
        """
        DESCRIPTION: Check 'OX.vipLevel' value displaying in Local Storage
        EXPECTED: 'OX.vipLevel' value is displayed in Local Storage
        """
        self.__class__.cookie_value = self.get_local_storage_cookie_value_as_dict(self.cookie_name)
        self.softAssert(self.assertEqual, self.cookie_value, self.vip_level,
                        msg=f'Cookie value for vip level user "{self.vip_level}" after refresh is "{self.cookie_value}"')

    def test_005_log_out(self):
        """
        DESCRIPTION: Log out
        EXPECTED: User is logged out. User's 'OX.vipLevel' is still present in Local Storage
        """
        self.site.logout()
        self.site.wait_content_state('Homepage')
        self.softAssert(self.assertEqual, self.cookie_value, self.vip_level,
                        msg=f'Cookie value for vip level user "{self.vip_level}" after logout is "{self.cookie_value}"')

    def test_006_repeat_1_5_steps_for_bronze_and_platinum_users(self):
        """
        DESCRIPTION: Repeat steps 1-5 for bronze and platinum users
        DESCRIPTION: Check 'OX.vipLevel' correct value displaying in Local Storage
        DESCRIPTION: Refresh the page
        DESCRIPTION: Check 'OX.vipLevel' value displaying in Local Storage
        DESCRIPTION: Log out
        EXPECTED: User is successfully logged in
        EXPECTED: 'OX.vipLevel' value = Casino VIP level
        EXPECTED: 'OX.vipLevel' value is displayed in Local Storage
        EXPECTED: User is logged out. User's 'OX.vipLevel' is still present in Local Storage
        """
        for username, vip_level in self.vip_level_users.items():
            self.__class__.username = username
            self.__class__.vip_level = vip_level
            self._logger.info(f'*** Repeating validations with user "{self.username}" and level "{self.vip_level}"')
            if self.brand == 'ladbrokes' and tests.settings.backend_env == 'prod':
                vip_password = tests.settings.default_vip_password
            else:
                vip_password = tests.settings.default_password
            self.site.login(username=self.username, password=vip_password)
            self.test_002_check_oxviplevel_correct_value_displaying_in_local_storage()
            self.test_003_refresh_the_page()
            self.test_004_check_oxviplevel_value_displaying_in_local_storage()
            self.test_005_log_out()
