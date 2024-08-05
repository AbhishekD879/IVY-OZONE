import pytest
import tests
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.Common import Common


@pytest.mark.lad_stg2
@pytest.mark.lad_tst2
@pytest.mark.lad_prod
# @pytest.mark.lad_h1
@pytest.mark.high
@pytest.mark.other
@pytest.mark.fanzone
@pytest.mark.desktop
@vtest
class Test_C65304981_To_verify_SYC_popup_in_Footaball_landing_page_when_user_kills_the_app_or_browser(Common):
    """
    TR_ID: C65304981
    NAME: To verify SYC popup in Footaball landing page when user kills the app or browser
    DESCRIPTION: To verify SYC popup in Footaball landing page when user kills the app or browser
    PRECONDITIONS: 1)User has access to CMS
    PRECONDITIONS: 2)Fanzone option is enabled in Structure and Fanzone entry points in Fanzone section in cms
    PRECONDITIONS: 3)Featured events are present to be displayed for competition for the particular team in OB
    PRECONDITIONS: 4)SYC page is created in cms with all required data in Fanzone SYC section
    PRECONDITIONS: 5)User has not performed any action on SYC overlay
    PRECONDITIONS: 6)User has FE url and Valid credentials to Login Lads FE and user has successfully logged into application
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        PRECONDITIONS: 1)User has access to CMS
        PRECONDITIONS: 2)Fanzone option is enabled in Structure and Fanzone entry points in Fanzone section in cms
        PRECONDITIONS: 3)Featured events are present to be displayed for competition for the particular team in OB
        PRECONDITIONS: 4) New user should be registered and login to application with newly registered user with Valid credentials
        """
        fanzone_status = self.get_initial_data_system_configuration().get('Fanzone')
        if not fanzone_status.get('enabled'):
            self.cms_config.update_system_configuration_structure(config_item='Fanzone',
                                                                  field_name='enabled',
                                                                  field_value=True)
        syc = self.cms_config.get_fanzone_syc()
        self.assertTrue(syc, msg='"SYC"is not configured in cms')
        self.__class__.username = self.gvc_wallet_user_client.register_new_user().username
        self.site.login(username=self.username)

    def test_001_navigate_to_football_page(self):
        """
        DESCRIPTION: Navigate to Football page
        EXPECTED: User should be navigated to Football page
        """
        self.site.open_sport(name='Football', fanzone=True)

    def test_002_verify_if_syc_overlay_is_shown_in_football_page(self):
        """
        DESCRIPTION: Verify if SYC overlay is shown in Football page
        EXPECTED: SYC overlay is shown to the user in Football Landing page
        """
        dialog_fb = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_SHOW_US_YOUR_COLORS, timeout=30)
        self.assertTrue(dialog_fb, msg="SYC overlay is not displayed")

    def test_003_close_the_page_or_kill_the_app(self):
        """
        DESCRIPTION: Close the Page or kill the app
        EXPECTED: User should be able to close the page or kill the app
        """
        self.device.open_new_tab()
        self.device.open_tab(tab_index=0)
        self.device.close_current_tab()
        self.device.switch_to_new_tab()
        self.device.navigate_to(tests.HOSTNAME)
        self.assertTrue(self.site.wait_logged_in(), msg='User is not logged in')

    def test_004_login_to_lads_application_and_navigate_to_football_slp(self):
        """
        DESCRIPTION: Login to lads application and navigate to Football slp
        EXPECTED: User should be navigated to Football landing page
        """
        self.site.open_sport(name='Football', fanzone=True)

    def test_005_verify_syc_popup_is_displayed(self):
        """
        DESCRIPTION: verify SYC popup is displayed
        EXPECTED: SYC popup should be displayed
        """
        self.test_002_verify_if_syc_overlay_is_shown_in_football_page()