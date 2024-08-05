import pytest
from voltron.utils.waiters import wait_for_result, wait_for_haul
from tests.base_test import vtest
from tests.Common import Common
from voltron.environments import constants as vec


@pytest.mark.lad_stg2
@pytest.mark.lad_tst2
@pytest.mark.lad_prod
# @pytest.mark.lad_hl
@pytest.mark.high
@pytest.mark.other
@pytest.mark.desktop
@pytest.mark.fanzone_reg_tests
@vtest
class Test_C65305075_Verify_accessing_Fanzone_page_from_Homepage(Common):
    """
    TR_ID: C65305075
    NAME: Verify accessing Fanzone page from Homepage
    DESCRIPTION: To verify user should be able to access Fanzone page by clicking on "Let me see" cta button from homepage(Device/desktop)
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        PRECONDITIONS: User has access to CMS
        PRECONDITIONS: Fanzone option is enabled in Structure and Fanzone entry points in Fanzone section in cms
        PRECONDITIONS: User has FE url and Valid credentials to Login Lads FE
        PRECONDITIONS: User has completed the Fanzone Syc successfully in FE
        """
        fanzone_status = self.get_initial_data_system_configuration().get('Fanzone')
        if not fanzone_status.get('enabled'):
            self.cms_config.update_system_configuration_structure(config_item='Fanzone',
                                                                  field_name='enabled',
                                                                  field_value=True)
        astonVilla_fanzone = self.cms_config.get_fanzone(vec.fanzone.TEAMS_LIST.aston_villa.title())
        if astonVilla_fanzone['active'] is not True:
            self.cms_config.update_fanzone(vec.fanzone.TEAMS_LIST.aston_villa.title())

        username = self.gvc_wallet_user_client.register_new_user().username
        self.site.login(username=username)
        self.site.open_sport(name='FOOTBALL', fanzone=True)
        self.site.wait_content_state("football")
        dialog_fb = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_SHOW_US_YOUR_COLORS, timeout=30)
        dialog_fb.imin_button.click()
        wait_for_result(lambda: self.site.show_your_colors.items_as_ordered_dict,
                        name='I am in button is displayed',
                        timeout=5)
        teams = self.site.show_your_colors.items_as_ordered_dict
        teams[vec.fanzone.TEAMS_LIST.aston_villa.title()].scroll_to_we()
        teams[vec.fanzone.TEAMS_LIST.aston_villa.title()].click()
        dialog_confirm = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_TEAM_CONFIRMATION)
        dialog_confirm.confirm_button.click()
        wait_for_haul(5)
        dialog_alert = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_TEAM_ALERTS)
        dialog_alert.exit_button.click()

    def test_001_Hit_the_FE_url_and_login_to_Lads_FE(self):
        """
        DESCRIPTION: Hit the FE url and login to Lads FE
        EXPECTED: User should be able to access the url and is logged into Lads application, User is on Homepage
        """
        self.navigate_to_page("homepage")
        self.site.wait_content_state("homepage")

    def test_002_verify_user_is_able_to_see_Fanzone_banner_in_Homepage_section(self):
        """
        DESCRIPTION: verify user is able to see Fanzone banner in Homepage section
        EXPECTED: User should be able to see Fanzone banner
        """
        self.assertTrue(self.site.home.fanzone_banner(), msg="Fanzone banner is not displayed")

    def test_003_Click_on_Let_me_see_cta_button_in_the_banner(self):
        """
        DESCRIPTION: Click on "Let me see "cta  button in the banner
        EXPECTED: User should be navigated to respective Fanzone details page
        """
        fanzone_banner = self.site.home.fanzone_banner()
        fanzone_banner.click()
        wait_for_result(lambda: self.site.fanzone.tabs_menu.current,
                        name='Fanzone page not displayed',
                        timeout=5)
        current_tab = self.site.fanzone.tabs_menu.current
        self.assertEqual(current_tab, vec.fanzone.NOW_AND_NEXT,
                         msg=f'Actual Tab "{current_tab}", is not same '
                             f' expected tab "{vec.fanzone.NOW_AND_NEXT}"')
        dialog_alert_email = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_EMAIL_OPT_IN)
        if dialog_alert_email:
            dialog_alert_email.remind_me_later.click()

