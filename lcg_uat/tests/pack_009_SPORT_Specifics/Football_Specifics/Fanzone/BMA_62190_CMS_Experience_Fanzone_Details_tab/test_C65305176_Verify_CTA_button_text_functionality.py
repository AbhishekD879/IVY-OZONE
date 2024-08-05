import pytest
from tests.base_test import vtest
from tests.Common import Common
from time import sleep
from voltron.environments import constants as vec
from voltron.utils.waiters import wait_for_result


@pytest.mark.lad_tst2
@pytest.mark.lad_stg2
@pytest.mark.lad_prod
# @pytest.mark.hl
@pytest.mark.fanzone
@pytest.mark.desktop
@pytest.mark.medium
@pytest.mark.other
@vtest
class Test_C65305176_Verify_CTA_button_text_functionality(Common):
    """
    TR_ID: C65305176
    NAME: Verify CTA button text functionality
    DESCRIPTION: Verify CTA button text functionality
    PRECONDITIONS: 1) User should be logged into CMS
    PRECONDITIONS: 2) Fanzone should be enabled in System Configuration
    PRECONDITIONS: 3) CMS--> System Configuration--> Structure-->Fanzone
    PRECONDITIONS: 4) Fanzone should be created
    PRECONDITIONS: 5) User has subscribed to Fanzone
    PRECONDITIONS: 6) All the entry points toggle should be on in Fanzone configuration
    PRECONDITIONS: 7) User is logged into application
    PRECONDITIONS: 8) Image should be updated in Sitecore and capture the Item Id
    """
    keep_browser_open = True

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
        self.site.open_sport(name='FOOTBALL', fanzone=True)
        self.site.wait_content_state("football")
        dialog_fb = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_SHOW_US_YOUR_COLORS, timeout=30)
        dialog_fb.imin_button.click()
        wait_for_result(lambda: self.site.show_your_colors.items_as_ordered_dict,
                        name='OK button is displayed',
                        timeout=5)
        teams = self.site.show_your_colors.items_as_ordered_dict
        teams[vec.fanzone.TEAMS_LIST.aston_villa.title()].scroll_to_we()
        teams[vec.fanzone.TEAMS_LIST.aston_villa.title()].click()
        dialog_confirm = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_TEAM_CONFIRMATION, timeout=10)
        dialog_confirm.confirm_button.click()
        sleep(6)
        dialog_alert = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_TEAM_ALERTS)
        dialog_alert.exit_button.click()
        self.site.wait_content_state_changed(timeout=10)

    def test_001_verify_launch_banner_is_populated_in_home_page(self):
        """
        DESCRIPTION: Verify Launch banner is populated in Home page
        EXPECTED: Launch Banner should be populated
        """
        self.navigate_to_page('Homepage')
        self.site.wait_content_state('Homepage', timeout=10)
        self.__class__.banner = wait_for_result(lambda: self.site.home.fanzone_banner(), timeout=10)
        self.assertTrue(self.banner, msg='Launch Banner is not populated')

    def test_002_click_on_cta_button_let_me_see(self):
        """
        DESCRIPTION: Click on CTA Button 'Let Me See'
        EXPECTED: User should be navigated to Subscribed Fanzone page
        """
        self.banner.let_me_see.click()
        sleep(3)
        tabs_menu = self.site.fanzone.tabs_menu.items_as_ordered_dict
        self.assertIn(vec.fanzone.NOW_AND_NEXT, tabs_menu,
                      msg=f'"{vec.fanzone.NOW_AND_NEXT}" tab is not present in tabs menu')
