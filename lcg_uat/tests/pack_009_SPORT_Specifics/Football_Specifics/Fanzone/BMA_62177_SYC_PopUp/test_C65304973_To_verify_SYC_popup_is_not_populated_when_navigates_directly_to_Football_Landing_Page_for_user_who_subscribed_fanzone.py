import tests
import voltron.environments.constants as vec
import pytest
from crlat_siteserve_client.utils.exceptions import SiteServeException
from time import sleep
from tests.Common import Common
from tests.base_test import vtest
from voltron.utils.waiters import wait_for_result


@pytest.mark.lad_stg2
# @pytest.mark.lad_h1
@pytest.mark.lad_tst2
@pytest.mark.lad_prod
@pytest.mark.high
@pytest.mark.desktop
@pytest.mark.other
@pytest.mark.fanzone
@vtest
class Test_C65304973_To_verify_SYC_popup_is_not_populated_when_navigates_directly_to_Football_Landing_Page_for_user_who_subscribed_fanzone(Common):
    """
    TR_ID: C65304973
    NAME: To verify SYC popup is not populated when navigates directly to Football Landing Page for user who subscribed fanzone
    DESCRIPTION: To verify SYC popup is not populated when navigates directly to Football Landing Page for user who subscribed fanzone
    PRECONDITIONS: 1)User has access to CMS
    PRECONDITIONS: 2)Fanzone option is enabled in Structure and Fanzone entry points in Fanzone section in cms
    PRECONDITIONS: 3)Featured events are present to be displayed for competition for the particular team in OB
    PRECONDITIONS: 4)SYC page is created in cms with all required data in Fanzone SYC section and "Days to Hide Remind Me Later"- Xdays
    PRECONDITIONS: 5) User has subscribed for Fanzone previously
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        PRECONDITIONS: 1) In CMS-Fanzone SYC- data should be created, which will trigger SYC Entry points in front end
        PRECONDITIONS: 2) User has subscribed to Fanzone
        PRECONDITIONS: 3) User should be logged in state
        """
        fanzone_status = self.get_initial_data_system_configuration().get('Fanzone')
        if tests.settings.backend_env == 'prod':
            if not fanzone_status.get('enabled'):
                if 'beta' in tests.HOSTNAME:
                    self.cms_config.update_system_configuration_structure(config_item='Fanzone',
                                                                          field_name='enabled',
                                                                          field_value=True)
                else:
                    raise SiteServeException(f'Fanzone is not enabled for "{tests.HOSTNAME}"')
        astonVilla_fanzone = self.cms_config.get_fanzone(vec.fanzone.TEAMS_LIST.aston_villa.title())
        if astonVilla_fanzone['active'] is not True:
            self.cms_config.update_fanzone(vec.fanzone.TEAMS_LIST.aston_villa.title())
        username = self.gvc_wallet_user_client.register_new_user().username
        self.site.login(username=username)
        self.site.open_sport(name='Football', fanzone=True)
        dialog_fb = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_SHOW_US_YOUR_COLORS)
        dialog_fb.imin_button.click()
        wait_for_result(lambda: self.site.show_your_colors.items_as_ordered_dict,
                        name='All Fanzones are displayed',
                        timeout=5)
        fanzone = self.site.show_your_colors.items_as_ordered_dict
        fanzone[vec.fanzone.TEAMS_LIST.aston_villa.title()].scroll_to_we()
        fanzone[vec.fanzone.TEAMS_LIST.aston_villa.title()].click()
        sleep(2)
        dialog_confirm = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_TEAM_CONFIRMATION)
        dialog_confirm.confirm_button.click()
        sleep(3)
        dialog_teamalert = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_TEAM_ALERTS)
        dialog_teamalert.exit_button.click()

    def test_001_navigate_to_football_landing_page_httpsbeta_sportsladbrokescomsportfootballmatchestoday_without_login_to_application(self):
        """
        DESCRIPTION: Navigate to Football Landing Page "https://beta-sports.ladbrokes.com/sport/football/matches/today' without login to application
        EXPECTED: User should be navigated to Football page
        """
        self.navigate_to_page("Homepage")
        self.site.wait_content_state("HomePage")
        self.site.open_sport(name='Football', fanzone=True)
        self.site.wait_content_state("football")

    def test_002_note_login_to_the_env_in_which_the_code_is_deployed_above_is_just_example(self):
        """
        DESCRIPTION: Note: login to the env in which the code is deployed, above is just example
        """
        # Covered in above step

    def test_003_click_on_login_and_enter_the_valid_credentials(self):
        """
        DESCRIPTION: Click on login and enter the valid credentials
        EXPECTED: User should be logged into application successfully
        """
        # Covered in above step

    def test_004_verify_syc_overlay_is_not_displayed(self):
        """
        DESCRIPTION: Verify SYC overlay is not displayed
        EXPECTED: SYC overlay should not be displayed
        """
        try:
            dialog_fb = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_SHOW_US_YOUR_COLORS)
            self.assertFalse(dialog_fb.is_displayed(), msg='"SYC overlay"is displayed on Football landing page')
        except Exception:
            self._logger.info('SYC overlay is not displayed')
