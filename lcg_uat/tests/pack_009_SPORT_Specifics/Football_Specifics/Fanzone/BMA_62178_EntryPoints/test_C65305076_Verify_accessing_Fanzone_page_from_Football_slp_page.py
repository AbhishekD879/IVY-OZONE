import pytest
from tests.base_test import vtest
from tests.Common import Common
from time import sleep
from voltron.environments import constants as vec
from voltron.utils.waiters import wait_for_result


@pytest.mark.lad_stg2
@pytest.mark.lad_tst2
@pytest.mark.lad_prod
# @pytest.mark.lad_hl
@pytest.mark.high
@pytest.mark.other
@pytest.mark.desktop
@pytest.mark.fanzone_reg_tests
@vtest
class Test_C65305076_Verify_accessing_Fanzone_page_from_Football_slp_page(Common):
    """
    TR_ID: C65305076
    NAME: Verify accessing Fanzone page from Football slp page
    DESCRIPTION: To verify user should be able to access Fanzone page by clicking on "Let me see" cta button from Football slp page (Device/desktop )
    PRECONDITIONS: 1)User has access to CMS
    PRECONDITIONS: 2)Fanzone option is enabled in Structure and Fanzone entry points in Fanzone section in cms
    PRECONDITIONS: 3)User has FE url and Valid credentials to Login Lads FE
    PRECONDITIONS: 4)User has completed the Fanzone Syc successfully in FE
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
        if not astonVilla_fanzone['active'] or not astonVilla_fanzone['fanzoneConfiguration']['footballHome']:
            self.cms_config.update_fanzone(fanzone_name=vec.fanzone.TEAMS_LIST.aston_villa.title(), footballHome=True)
        username = self.gvc_wallet_user_client.register_new_user().username
        self.site.login(username=username)
        self.site.open_sport(name='FOOTBALL', fanzone=True)
        self.site.wait_content_state("football")
        dialog_fb = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_SHOW_US_YOUR_COLORS, timeout=30)
        dialog_fb.imin_button.click()
        results = wait_for_result(lambda: self.site.show_your_colors.items_as_ordered_dict, timeout=30,
                                  name='All Teams to be displayed')
        self.assertTrue(results, msg='Teams are not displayed')
        teams = self.site.show_your_colors.items_as_ordered_dict
        list(teams.values())[1].scroll_to_we()
        list(teams.values())[1].click()
        dialog_confirm = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_TEAM_CONFIRMATION)
        wait_for_result(lambda: dialog_confirm.confirm_button.is_displayed(), timeout=10, name='"CONFIRM" button to be displayed.')
        dialog_confirm.confirm_button.click()
        sleep(3)
        dialog_alert = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_TEAM_ALERTS)
        wait_for_result(lambda: dialog_alert.exit_button.is_displayed(), timeout=5, name='"EXIT" button to be displayed.')
        dialog_alert.exit_button.click()

    def test_001_hit_the_fe_url_and_login_to_lads_fe(self):
        """
        DESCRIPTION: Hit the FE url and login to Lads FE
        EXPECTED: User should be able to access the url and is logged into Lads application, User is on Homepage
        """
        self.navigate_to_page('Homepage')
        self.site.wait_content_state('Homepage')

    def test_002_click_on_football_option_from_a_z_menusports_ribbon(self):
        """
        DESCRIPTION: Click on Football option from A-z menu/Sports ribbon
        EXPECTED: User should be able to see Fanzone banner in Football slp page
        """
        self.navigate_to_page("sport/football")
        self.site.wait_content_state("football")
        self.assertTrue(self.site.football.fanzone_banner(), msg="Fanzone banner is not displayed")

    def test_003_click_on_let_me_see_cta_button__in_the_banner(self):
        """
        DESCRIPTION: Click on "Let me see" cta button  in the banner
        EXPECTED: User should be navigated to respective Fanzone details page
        """
        fanzone_banner = self.site.football.fanzone_banner()
        fanzone_banner.click()
        wait_for_result(lambda: self.site.fanzone.tabs_menu, timeout=5,
                        name='"Fanzone tab menus" to be displayed.')
        current_tab = self.site.fanzone.tabs_menu.current
        self.assertEqual(current_tab, vec.fanzone.NOW_AND_NEXT,
                         msg=f'Actual Tab "{current_tab}", is not same '
                             f' expected tab "{vec.fanzone.NOW_AND_NEXT}"')
        dialog_alert_email = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_EMAIL_OPT_IN)
        if dialog_alert_email:
            dialog_alert_email.remind_me_later.click()