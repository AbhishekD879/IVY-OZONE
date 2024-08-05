import pytest
import tests
import voltron.environments.constants as vec
from crlat_siteserve_client.utils.exceptions import SiteServeException
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.lad_stg2
@pytest.mark.lad_tst2
@pytest.mark.lad_prod
# @pytest.mark.lad_hl
@pytest.mark.desktop
@pytest.mark.high
@pytest.mark.fanzone_reg_tests
@pytest.mark.other
@vtest
class Test_C65304983_verify_user_gets_SYC_popup_If_user_clicks_on_DONT_SHOW_ME_THIS_AGAIN_or_REMIND_ME_LATER_and_clear_cach_cookies(Common):
    """
    TR_ID: C65304983
    NAME: verify user gets SYC popup If user clicks on DONT SHOW ME THIS AGAIN or REMIND ME LATER and clear cach/cookies.
    DESCRIPTION: verify user gets SYC popup If user clicks on DONT SHOW ME THIS AGAIN or REMIND ME LATER and clear cach/cookies.
    PRECONDITIONS: 1)User has access to CMS
    PRECONDITIONS: 2)Fanzone option is enabled in Structure and Fanzone entry points in Fanzone section in cms
    PRECONDITIONS: 3)Featured events are present to be displayed for competition for the particular team in OB
    PRECONDITIONS: 4)SYC page is created in cms with all required data in Fanzone SYC section and "Days to Hide Remind Me Later"- 15days
    PRECONDITIONS: 5)User has FE url and Valid credentials to Login Lads FE and user has successfully logged into application and is on Football landing page
    """
    keep_browser_open = True

    def test_000_precondition(self):
        """
        PRECONDITIONS: 1)User has access to CMS
        PRECONDITIONS: 2)Fanzone option is enabled in Structure and Fanzone entry points in Fanzone section in cms
        PRECONDITIONS: 3)Featured events are present to be displayed for competition for the particular team in OB
        PRECONDITIONS: 4)SYC page is created in cms with all required data in Fanzone SYC section and "Days to Hide Remind Me Later"- 15days
        PRECONDITIONS: 5)User has FE url and Valid credentials to Login Lads FE and user has successfully logged into application and is on Football landing page
        """
        fanzone_status = self.get_initial_data_system_configuration().get('Fanzone')
        if not fanzone_status.get('enabled'):
            if 'beta' in tests.HOSTNAME:
                self.cms_config.update_system_configuration_structure(config_item='Fanzone',
                                                                      field_name='enabled',
                                                                      field_value=True)
            else:
                raise SiteServeException(f'Fanzone is not enabled for "{tests.HOSTNAME}"')

        self.__class__.username = self.gvc_wallet_user_client.register_new_user().username

    def test_001_navigate_to_football_landing_page(self):
        """
        DESCRIPTION: Navigate to Football Landing Page
        EXPECTED: User should be navigated to Football page and should display SYC overlay
        """
        self.site.login(username=self.username)
        self.site.open_sport(name='FOOTBALL', fanzone=True)
        self.site.wait_content_state("football", timeout=30)
        self.__class__.dialog_fb = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_SHOW_US_YOUR_COLORS)
        self.assertTrue(self.dialog_fb, msg='SYC overlay is not displayed')

    def test_002_click_on_remind_me_later(self):
        """
        DESCRIPTION: Click on REMIND ME LATER
        EXPECTED: popup should be undisplayed
        """
        self.dialog_fb.remind_later_button.click()
        self.assertFalse(self.dialog_fb.has_remind_later_button(expected_result=False))

    def test_003_clear_cachecookies(self):
        """
        DESCRIPTION: Clear cache/cookies
        EXPECTED: Cache/Cookies are cleared
        """
        self.delete_cookies()
        self.device.driver.execute_script('localStorage.clear();')

    def test_004_navigate_football_page(self):
        """
        DESCRIPTION: Navigate football page
        EXPECTED: Users should get SYC popup
        """
        self.navigate_to_page("Homepage")
        self.site.wait_content_state("Homepage")
        self.test_001_navigate_to_football_landing_page()
