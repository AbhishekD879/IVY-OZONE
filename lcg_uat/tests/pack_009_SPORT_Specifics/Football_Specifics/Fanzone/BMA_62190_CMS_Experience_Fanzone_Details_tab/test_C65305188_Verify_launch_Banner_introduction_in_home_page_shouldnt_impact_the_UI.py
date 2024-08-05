import pytest
import tests
from tests.base_test import vtest
from tests.Common import Common
from time import sleep
from voltron.environments import constants as vec
from voltron.utils.waiters import wait_for_result


@pytest.mark.lad_tst2
@pytest.mark.lad_stg2
@pytest.mark.lad_prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.fanzone
@pytest.mark.desktop
@pytest.mark.other
@vtest
class Test_C65305188_Verify_launch_Banner_introduction_in_home_page_shouldnt_impact_the_UI(Common):
    """
    TR_ID: C65305188
    NAME: Verify launch Banner introduction in home page shouldn't impact the UI
    DESCRIPTION: Verify launch Banner introduction in home page shouldn't impact the UI
    PRECONDITIONS: 1) User should be logged into CMS
    PRECONDITIONS: 2) Fanzone should be enabled in System Configuration
    PRECONDITIONS: 3) CMS--> System Configuration--> Structure-->Fanzone
    PRECONDITIONS: 4) Fanzone should be created
    PRECONDITIONS: 5) User has subscribed to Fanzone
    PRECONDITIONS: 6) All the entry points toggle should be on in Fanzone configuration
    PRECONDITIONS: 7) Image should be updated in Sitecore and capture the Item Id
    """
    keep_browser_open = True

    def check_homepage_impact(self):
        if self.device_type == 'desktop':
            sports = self.site.sport_menu.sport_menu_items_group('Main').items_as_ordered_dict.keys()
            self.assertTrue(sports, msg='No sports found in "A-Z Sports" section')
            self.assertTrue(self.site.header.is_displayed(), msg='"Main Navigation" header is not found')
            self.assertTrue(self.site.home.desktop_modules.inplay_live_stream_module.is_displayed(),
                            msg='"In-play and live stream" ribbon is not present on Homepage')
        else:
            module_ribbon_tab = self.site.home.module_selection_ribbon.tab_menu.items_as_ordered_dict
            self.assertTrue(module_ribbon_tab, msg='Module ribbon tab is not found in the homepage')
            sports_ribbon = self.site.home.menu_carousel.items_as_ordered_dict
            self.assertTrue(sports_ribbon, msg='Sports ribbon is not found in homepage')
            footer_items = self.site.navigation_menu.items_as_ordered_dict
            self.assertTrue(footer_items, msg='No items in Footer menu')

    def test_000_preconditions(self):
        """
        PRECONDITIONS: 1) User should be logged into CMS
        PRECONDITIONS: 2) Fanzone should be enabled in System Configuration
        PRECONDITIONS: 3) CMS--> System Configuration--> Structure-->Fanzone
        PRECONDITIONS: 4) Fanzone should be created
        PRECONDITIONS: 5) User has subscribed to Fanzone
        PRECONDITIONS: 6) All the entry points toggle should be on in Fanzone configuration
        PRECONDITIONS: 7) User is logged into application
        PRECONDITIONS: 8) Image should be updated in Sitecore and capture the Item Id
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
        self.check_homepage_impact()
        self.site.open_sport(name='FOOTBALL', fanzone=True)
        self.site.wait_content_state("football")
        dialog_fb = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_SHOW_US_YOUR_COLORS, timeout=30)
        dialog_fb.imin_button.click()
        wait_for_result(lambda: self.site.show_your_colors.items_as_ordered_dict,
                        name='All teams to be displayed')
        teams = self.site.show_your_colors.items_as_ordered_dict
        teams[vec.fanzone.TEAMS_LIST.aston_villa.title()].scroll_to_we()
        teams[vec.fanzone.TEAMS_LIST.aston_villa.title()].click()
        dialog_confirm = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_TEAM_CONFIRMATION, timeout=30)
        dialog_confirm.confirm_button.click()
        sleep(6)
        dialog_alert = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_TEAM_ALERTS, timeout=30)
        dialog_alert.exit_button.click()
        self.site.wait_content_state_changed(timeout=30)

    def test_001_login_to_lads_application(self):
        """
        DESCRIPTION: Login to Lads application
        EXPECTED: Application login should be successful
        """
        # covered in preconditions

    def test_002_verify_launch_banner_is_populated_in_home_page(self):
        """
        DESCRIPTION: Verify Launch banner is populated in Home page
        EXPECTED: Launch Banner should be populated
        """
        self.navigate_to_page('Homepage')
        self.site.wait_content_state('Homepage', timeout=10)
        if tests.settings.device_type == "mobile":
            self.site.home.module_selection_ribbon.tab_menu.items_as_ordered_dict.get(
                vec.racing.RACING_HIGHLIGHTS_TAB_NAME).click()
        banner = wait_for_result(lambda: self.site.home.fanzone_banner(), timeout=30)
        self.assertTrue(banner, msg='Launch Banner is not populated')

    def test_003_verify_there_is_no_impact_to_home_page_ui_with_introduction_of_new_launch_banner(self):
        """
        DESCRIPTION: Verify there is no impact to Home Page UI with introduction of new launch banner
        EXPECTED: There should be no impact to Home Page UI
        """
        self.check_homepage_impact()
