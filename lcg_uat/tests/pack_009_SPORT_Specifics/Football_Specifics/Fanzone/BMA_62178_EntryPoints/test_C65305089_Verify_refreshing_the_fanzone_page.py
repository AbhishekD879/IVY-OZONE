import pytest
from tests.base_test import vtest
from tests.Common import Common
from voltron.utils.waiters import wait_for_result
from voltron.environments import constants as vec
from time import sleep


@pytest.mark.lad_stg2
@pytest.mark.lad_tst2
@pytest.mark.lad_prod
# @pytest.mark.lad_hl
@pytest.mark.medium
@pytest.mark.fanzone
@pytest.mark.desktop
@pytest.mark.other
@vtest
class Test_C65305089_Verify_refreshing_the_fanzone_page(Common):
    """
    TR_ID: C65305089
    NAME: Verify refreshing the fanzone page
    DESCRIPTION: To verify when user clicks Refresh option from Fanzone page then Still Fanzone page should be displayed
    PRECONDITIONS: 1)User has access to CMS
    PRECONDITIONS: 2)Fanzone option is enabled in Structure and Fanzone entry points in Fanzone section in cms
    PRECONDITIONS: 3)User has FE url and Valid credentials to Login Lads FE
    """
    keep_browser_open = True

    def test_000_precondition(self):
        fanzone_status = self.get_initial_data_system_configuration().get('Fanzone')
        if not fanzone_status.get('enabled'):
            self.cms_config.update_system_configuration_structure(config_item='Fanzone',
                                                                  field_name='enabled',
                                                                  field_value=True)
        aston_villa = vec.fanzone.TEAMS_LIST.aston_villa.title()
        astonVilla_fanzone = self.cms_config.get_fanzone(aston_villa)
        if astonVilla_fanzone['active'] is not True:
            self.cms_config.update_fanzone(vec.fanzone.TEAMS_LIST.aston_villa.title())
        username = self.gvc_wallet_user_client.register_new_user().username
        self.site.wait_content_state('Homepage')
        self.site.login(username=username)
        self.site.open_sport('football', fanzone=True)
        dialog_fb = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_SHOW_US_YOUR_COLORS)
        dialog_fb.imin_button.click()
        wait_for_result(lambda: self.site.show_your_colors.items_as_ordered_dict,
                        name='All Teams to be displayed',
                        timeout=5)
        teams = self.site.show_your_colors.items_as_ordered_dict
        teams.get(aston_villa).scroll_to_we()
        teams.get(aston_villa).click()
        sleep(3)
        dialog_confirm = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_TEAM_CONFIRMATION)
        dialog_confirm.confirm_button.click()
        sleep(3)
        dialog_alert = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_TEAM_ALERTS)
        dialog_alert.exit_button.click()

    def test_001_hit_the_fe_url_and_login_to_lads_fe(self):
        """
        DESCRIPTION: Hit the FE url and login to Lads FE
        EXPECTED: User should be able to access the url and is logged into Lads application, User is on Homepage
        """
        # covered in above step

    def test_002_now_navigate_homepage(self):
        """
        DESCRIPTION: Now navigate Homepage
        EXPECTED: User should be navigated to Homepage
        """
        self.navigate_to_page('homepage')
        self.site.wait_content_state('homepage')

    def test_003_click_on_launch_banner_and_navigate_fanzone_page(self):
        """
        DESCRIPTION: Click on Launch banner and navigate Fanzone page
        EXPECTED: User should be navigated Fanzone page
        """
        banner = self.site.home.fanzone_banner()
        banner.let_me_see.click()
        result = wait_for_result(lambda: self.site.fanzone.tabs_menu, timeout=5,
                                 name='"Fanzone tab menus" to be displayed.')
        self.assertTrue(result, msg='User is not on the Fanzone page')

    def test_004_click_on_refresh_option(self):
        """
        DESCRIPTION: Click on refresh option
        EXPECTED: User should be able to click on refresh
        """
        self.device.refresh_page()

    def test_005_verify_the_fanzone_page(self):
        """
        DESCRIPTION: Verify the Fanzone page
        EXPECTED: User should be on Fanzone page
        """
        result = wait_for_result(lambda: self.site.fanzone.tabs_menu, timeout=5,
                                 name='"Fanzone tab menus" to be displayed.')
        self.assertTrue(result, msg='User is not on the Fanzone page')
