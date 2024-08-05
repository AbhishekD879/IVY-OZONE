import pytest
import voltron.environments.constants as vec
from time import sleep
from tests.base_test import vtest
from tests.Common import Common
from voltron.utils.waiters import wait_for_result


@pytest.mark.lad_stg2
@pytest.mark.lad_tst2
@pytest.mark.lad_prod
# @pytest.mark.lad_hl
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.fanzone
@pytest.mark.other
@vtest
class Test_C65305158_Verify_Fanzone_entry_point_is_not_displayed_in_Sports_Ribbon_when_Show_in_Spots_Ribbon_toggle_is_OFF_in_Fanzone_Configuration(Common):
    """
    TR_ID: C65305158
    NAME: Verify Fanzone entry point is not displayed in Sports Ribbon when Show in Spots Ribbon toggle is OFF in Fanzone Configuration
    DESCRIPTION: Verify Fanzone entry point is not displayed in Sports Ribbon when Show in Spots Ribbon toggle is OFF in Fanzone Configuration
    PRECONDITIONS: 1) Fanzone should be enabled in System Configuration
    PRECONDITIONS: CMS--> System Configuration--> Structure-->Fanzone
    PRECONDITIONS: 2) Fanzone records should be created
    PRECONDITIONS: 3) Toggle should be OFF for Show in Sports Ribbon menu and for all the listed items toggle should be ON in Fanzone Configuration(CMS)
    PRECONDITIONS: CMS-->Fanzone-->Fanzone Configurations
    PRECONDITIONS: 4) Show in Sports Ribbon should be checked
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        DESCRIPTION: Verify Fanzone entry point is not displayed in Sports Ribbon when Show in Spots Ribbon toggle is OFF in Fanzone Configuration
        PRECONDITIONS: 1) Fanzone should be enabled in System Configuration
        PRECONDITIONS: CMS--> System Configuration--> Structure-->Fanzone
        PRECONDITIONS: 2) Fanzone records should be created
        PRECONDITIONS: 3) Toggle should be OFF for Show in Sports Ribbon menu and for all the listed items toggle should be ON in Fanzone Configuration(CMS)
        PRECONDITIONS: CMS-->Fanzone-->Fanzone Configurations
        PRECONDITIONS: 4) Show in Sports Ribbon should be checked
        """
        fanzone_status = self.get_initial_data_system_configuration().get('Fanzone')
        if not fanzone_status.get('enabled'):
            self.cms_config.update_system_configuration_structure(config_item='Fanzone',
                                                                  field_name='enabled',
                                                                  field_value=True)
        self.__class__.arsenal_sportsRibbon = self.cms_config.get_fanzone(vec.fanzone.TEAMS_LIST.arsenal.title())['fanzoneConfiguration']['sportsRibbon']
        if self.arsenal_sportsRibbon:
            self.cms_config.update_fanzone(vec.fanzone.TEAMS_LIST.arsenal.title(), sportsRibbon=False)
        username = self.gvc_wallet_user_client.register_new_user().username
        self.site.login(username=username)
        self.site.open_sport(name='FOOTBALL', fanzone=True)
        self.site.wait_content_state("football")
        dialog_fb = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_SHOW_US_YOUR_COLORS, timeout=30)
        dialog_fb.imin_button.click()
        wait_for_result(lambda: self.site.show_your_colors.items_as_ordered_dict,
                        name='OK button is displayed',
                        timeout=5)
        teams = self.site.show_your_colors.items_as_ordered_dict
        teams[vec.fanzone.TEAMS_LIST.arsenal.title()].scroll_to_we()
        teams[vec.fanzone.TEAMS_LIST.arsenal.title()].click()
        dialog_confirm = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_TEAM_CONFIRMATION, timeout=10)
        dialog_confirm.confirm_button.click()
        sleep(6)
        dialog_alert = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_TEAM_ALERTS)
        dialog_alert.exit_button.click()
        self.site.wait_content_state_changed(timeout=10)

    def test_001_login_to_lads_application(self):
        """
        DESCRIPTION: login to Lads application
        EXPECTED: Login should be successful
        """
        # Covered in above step

    def test_002_verify_fanzoneentry_point_is_not_displayed_in_sports_ribbonmobile(self):
        """
        DESCRIPTION: Verify Fanzone(entry point) is not displayed in Sports Ribbon(Mobile)
        EXPECTED: Fanzone shouldn't be displayed in Sports Ribbon
        """
        self.navigate_to_page(name='Homepage')
        if self.device_type == 'desktop':
            self.assertFalse(self.site.header.sport_menu.items_as_ordered_dict.get(vec.sb.FANZONE.upper()),
                             msg="Fanzone option is displayed in Sports Ribbon Menu")
        else:
            self.site.home.module_selection_ribbon.tab_menu.items_as_ordered_dict.get(vec.racing.RACING_HIGHLIGHTS_TAB_NAME).click()
            self.assertFalse(self.site.home.menu_carousel.items_as_ordered_dict.get(
                vec.sb.FANZONE), msg="Fanzone option is displayed in Sports Ribbon Menu")

    def test_003_verify_user_is_able_to_navigate_to_fanzone_page_through_below_listed_entry_points1_launch_banner_in_home_page2_launch_banner_in_football_slp3_sports_ribbonmobile(self):
        """
        DESCRIPTION: Verify user is able to navigate to Fanzone page through below listed entry points
        DESCRIPTION: 1. Launch Banner in Home page
        DESCRIPTION: 2. Launch Banner in Football SLP
        DESCRIPTION: 3. Sports Ribbon(mobile)
        EXPECTED: User should be able to navigate to Fanzone page
        """
        banner = self.site.home.fanzone_banner()
        banner.let_me_see.click()
        wait_for_result(lambda: self.site.fanzone.tabs_menu, timeout=5,
                        name='"Fanzone tab menus" to be displayed.')
        self.navigate_to_page('sport/football')
        self.assertTrue(self.site.football.fanzone_banner(), msg="Fanzone banner is not displayed")
        banner = self.site.home.fanzone_banner()
        banner.let_me_see.click()
        wait_for_result(lambda: self.site.fanzone.tabs_menu, timeout=5,
                        name='"Fanzone tab menus" to be displayed.')

    def tearDown(self):
        # Reverting the sportRibbon fanzone configuration
        self.cms_config.update_fanzone(vec.fanzone.TEAMS_LIST.arsenal.title(), sportsRibbon=self.arsenal_sportsRibbon)
