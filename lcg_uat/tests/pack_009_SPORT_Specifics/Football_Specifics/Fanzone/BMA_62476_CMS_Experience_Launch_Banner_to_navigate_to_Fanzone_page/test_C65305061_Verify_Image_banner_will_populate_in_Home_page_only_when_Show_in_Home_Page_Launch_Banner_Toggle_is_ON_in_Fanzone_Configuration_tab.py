import pytest
import tests
from tests.base_test import vtest
from tests.Common import Common
from time import sleep
from voltron.environments import constants as vec
from voltron.utils.waiters import wait_for_result


@pytest.mark.lad_stg2
@pytest.mark.lad_tst2
@pytest.mark.lad_prod
# @pytest.mark.lad_hl
@pytest.mark.medium
@pytest.mark.other
@pytest.mark.fanzone
@pytest.mark.desktop
@vtest
class Test_C65305061_Verify_Image_banner_will_populate_in_Home_page_only_when_Show_in_Home_Page_Launch_Banner_Toggle_is_ON_in_Fanzone_Configuration_tab(Common):
    """
    TR_ID: C65305061
    NAME: Verify Image banner will populate in Home page only when Show in Home Page Launch Banner Toggle is ON in Fanzone Configuration tab
    DESCRIPTION: Verify Image banner will populate in Home page only when Show in Home Page Launch Banner Toggle is ON in Fanzone Configuration tab
    PRECONDITIONS: 1) User has already subscribed for Fanzone
    PRECONDITIONS: 2) Fanzone should be enabled in System Configuration
    PRECONDITIONS: CMS--> System Configuration--> Structure-->Fanzone
    PRECONDITIONS: 3) Show In Home Page Launch Banner toggle should be On in Fanzone Configuration(CMS)
    PRECONDITIONS: CMS-->Fanzone-->Fanzone Configurations
    PRECONDITIONS: 4) Fanzone related Banner's should be uploaded into SiteCore
    PRECONDITIONS: 5) Image Banner Url field should be inputted Sitecore team Id of the banner we want to display
    PRECONDITIONS: CMS-->Fanzone-->Fanzone Details
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        fanzone_status = self.get_initial_data_system_configuration().get('Fanzone')
        if not fanzone_status.get('enabled'):
            self.cms_config.update_system_configuration_structure(config_item='Fanzone',
                                                                  field_name='enabled',
                                                                  field_value=True)
        astonVilla_fanzone = self.cms_config.get_fanzone(vec.fanzone.TEAMS_LIST.aston_villa.title())
        if astonVilla_fanzone['active'] is not True:
            self.cms_config.update_fanzone(vec.fanzone.TEAMS_LIST.aston_villa.title(),
                                           typeId=self.football_config.autotest_class.autotest_premier_league.type_id)

        username = self.gvc_wallet_user_client.register_new_user().username
        self.site.login(username=username)
        self.site.open_sport(name='FOOTBALL', fanzone=True)
        dialog_fb = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_SHOW_US_YOUR_COLORS, timeout=30)
        dialog_fb.imin_button.click()
        wait_for_result(lambda: self.site.show_your_colors.items_as_ordered_dict,
                        name='OK button is displayed',
                        timeout=5)
        teams = self.site.show_your_colors.items_as_ordered_dict
        teams[vec.fanzone.TEAMS_LIST.aston_villa.title()].click()
        dialog_confirm = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_TEAM_CONFIRMATION, timeout=15)
        dialog_confirm.confirm_button.click()
        sleep(6)
        dialog_alert = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_TEAM_ALERTS, timeout=15)
        dialog_alert.exit_button.click()

    def test_001_logon_to_lads_application(self):
        """
        DESCRIPTION: Logon to Lads application
        EXPECTED: User login should be successful
        """
        self.navigate_to_page('homepage')
        self.site.wait_content_state('homepage')

    def test_002_verify_launch_banner_is_populated_in_home_pagedesktop_and_under_highlights_tab_in_mobile(self):
        """
        DESCRIPTION: Verify Launch Banner is Populated in Home page(desktop) and under Highlights tab in mobile
        EXPECTED: Launch banner should be populated
        """
        if tests.settings.device_type == "mobile":
            self.site.home.module_selection_ribbon.tab_menu.items_as_ordered_dict. \
                get(vec.racing.RACING_HIGHLIGHTS_TAB_NAME).click()
        self.assertTrue(self.site.home.fanzone_banner(), msg="Fanzone banner is not displayed")
