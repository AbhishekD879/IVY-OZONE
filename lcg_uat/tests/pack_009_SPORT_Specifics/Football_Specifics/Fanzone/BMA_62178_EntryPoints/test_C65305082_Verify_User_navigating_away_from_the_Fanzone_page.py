import pytest
from time import sleep
from tests.base_test import vtest
from tests.Common import Common
from voltron.environments import constants as vec
from voltron.utils.waiters import wait_for_result


@pytest.mark.lad_stg2
@pytest.mark.lad_tst2
@pytest.mark.lad_prod
# @pytest.mark.lad_hl
@pytest.mark.high
@pytest.mark.fanzone
@pytest.mark.desktop
@pytest.mark.other
@vtest
class Test_C65305082_Verify_User_navigating_away_from_the_Fanzone_page(Common):
    """
    TR_ID: C65305082
    NAME: Verify User navigating away from the Fanzone page
    DESCRIPTION: To verify user can navigate away from Fanzone page by click on back button from the site header
    PRECONDITIONS: 1)User has access to CMS
    PRECONDITIONS: 2)Fanzone option is enabled in Structure and Fanzone entry points in Fanzone section in cms
    PRECONDITIONS: 3)User has FE url and Valid credentials to Login Lads FE
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        PRECONDITIONS: 1)User has access to CMS
        PRECONDITIONS: 2)Fanzone option is enabled in Structure and Fanzone entry points in Fanzone section in cms
        PRECONDITIONS: 3)User has FE url and Valid credentials to Login Lads FE
        """
        fanzone_status = self.get_initial_data_system_configuration().get('Fanzone')
        if not fanzone_status.get('enabled'):
            self.cms_config.update_system_configuration_structure(config_item='Fanzone',
                                                                  field_name='enabled',
                                                                  field_value=True)

    def test_001_hit_the_fe_url_and_login_to_lads_fe(self):
        """
        DESCRIPTION: Hit the FE url and login to Lads FE
        EXPECTED: User should be able to access the url and is logged into Lads application, User is on Homepage
        """
        username = self.gvc_wallet_user_client.register_new_user().username
        self.site.login(username=username)

    def test_002_now_navigate_homepage_football_slpa_z_menusports_ribbon(self):
        """
        DESCRIPTION: Now navigate Homepage /Football slp/A-Z menu/Sports ribbon
        EXPECTED: User should be navigated to Homepage /Football slp/A-Z menu/Sports ribbon
        """
        self.site.open_sport(name='FOOTBALL', fanzone=True)
        self.site.wait_content_state("football")
        dialog_fb = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_SHOW_US_YOUR_COLORS,
                                              timeout=30)
        dialog_fb.imin_button.click()
        results = wait_for_result(lambda: self.site.show_your_colors.items_as_ordered_dict, timeout=30,
                                  name='All Teams to be displayed')
        self.assertTrue(results, msg='Teams are not displayed')
        teams = self.site.show_your_colors.items_as_ordered_dict
        teams[vec.fanzone.TEAMS_LIST.aston_villa.title()].scroll_to_we()
        teams[vec.fanzone.TEAMS_LIST.aston_villa.title()].click()
        dialog_confirm = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_TEAM_CONFIRMATION)
        dialog_confirm.confirm_button.click()
        sleep(5)
        dialog_alert = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_TEAM_ALERTS)
        dialog_alert.exit_button.click()

    def test_003_click_on_fanzone__launch_banner_from_homepage(self):
        """
        DESCRIPTION: Click on Fanzone  Launch banner from homepage
        EXPECTED: User is navigated to Fanzone Page
        """
        self.navigate_to_page(name='Home')
        self.site.wait_content_state(state_name="homepage")
        banner = self.site.home.fanzone_banner()
        banner.let_me_see.click()
        tabs_menu = self.site.fanzone.tabs_menu.items_as_ordered_dict
        self.assertIn(vec.fanzone.NOW_AND_NEXT, tabs_menu,
                      msg=f'"{vec.fanzone.NOW_AND_NEXT}" tab is not present in tabs menu')

    def test_004_click_on_back_button_from_browser(self):
        """
        DESCRIPTION: Click on back button from browser
        EXPECTED: User should be navigated to Last visited page before navigating to Fanzone page
        """
        self.device.driver.back()
        self.site.wait_content_state(state_name="homepage")
