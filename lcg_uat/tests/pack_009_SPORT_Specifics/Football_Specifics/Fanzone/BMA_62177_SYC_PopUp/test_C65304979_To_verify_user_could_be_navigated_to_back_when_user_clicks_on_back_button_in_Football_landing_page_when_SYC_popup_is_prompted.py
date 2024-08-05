import voltron.environments.constants as vec
import pytest
from selenium.webdriver import ActionChains
from time import sleep
from tests.base_test import vtest
from tests.Common import Common
from voltron.pages.shared import get_driver


@pytest.mark.lad_stg2
@pytest.mark.lad_tst2
@pytest.mark.lad_prod
# @pytest.mark.lad_hl
@pytest.mark.desktop
@pytest.mark.high
@pytest.mark.fanzone
@pytest.mark.other
@vtest
class Test_C65304979_To_verify_user_could_be_navigated_to_back_when_user_clicks_on_back_button_in_Football_landing_page_when_SYC_popup_is_prompted(Common):
    """
    TR_ID: C65304979
    NAME: To verify user could be navigated to back, when user clicks on back button in Football landing page when SYC popup is prompted
    DESCRIPTION: To verify user could be navigated to back, when user clicks on back button in Football landing page when SYC popup is prompted
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
        PRECONDITIONS: 4)SYC page is created in cms with all required data in Fanzone SYC section
        PRECONDITIONS: 5)User has not performed any action on SYC overlay
        PRECONDITIONS: 6)User has FE url and Valid credentials to Login Lads FE and user has successfully logged into application
        """
        fanzone_status = self.get_initial_data_system_configuration().get('Fanzone')
        if not fanzone_status.get('enabled'):
            self.cms_config.update_system_configuration_structure(config_item='Fanzone',
                                                                  field_name='enabled',
                                                                  field_value=True)

        syc = self.cms_config.get_fanzone_syc()
        self.assertTrue(syc, msg='"SYC"is not configured in cms')
        username = self.gvc_wallet_user_client.register_new_user().username
        self.site.wait_content_state(state_name='HomePage')
        sleep(3)
        self.site.login(username=username)

    def test_001_navigate_to_football_page(self):
        """
        DESCRIPTION: Navigate to Football page
        EXPECTED: User should be navigated to Football page
        """
        self.site.open_sport(name='football', fanzone=True)
        self.site.wait_content_state("football")

    def test_002_verify_if_syc_overlay_is_shown_in_football_page(self):
        """
        DESCRIPTION: Verify if SYC overlay is shown in Football page
        EXPECTED: SYC overlay is shown to the user in Football Landing page
        """
        dialog_fb = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_SHOW_US_YOUR_COLORS)
        self.assertTrue(dialog_fb, msg='"SYC overlay"is not displayed on Football landing page')

    def test_003_click_on_back_button(self):
        """
        DESCRIPTION: Click on Back Button.
        EXPECTED: User should navigated back to previous page from where he has visited to Football SLP
        """
        ActionChains(get_driver()).move_by_offset(30, 30).click().perform()
        self.site.wait_content_state("football")
