import pytest
from tests.base_test import vtest
from tests.Common import Common
from voltron.environments import constants as vec
from voltron.utils.waiters import wait_for_result
from time import sleep


@pytest.mark.lad_stg2
@pytest.mark.lad_tst2
@pytest.mark.lad_prod
# @pytest.mark.lad_hl
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.fanzone
@pytest.mark.other
@vtest
class Test_C65305062_Verify_Image_banner_will_not_populate_in_Home_page_when_Show_in_Home_Page_Launch_Banner_Toggle_is_OFF_in_Fanzone_Configuration_tab(Common):
    """
    TR_ID: C65305062
    NAME: Verify Image banner will not populate in Home page when Show in Home Page Launch Banner Toggle is OFF in Fanzone Configuration tab
    DESCRIPTION: Verify Image banner will not populate in Home page when Show in Home Page Launch Banner Toggle is OFF in Fanzone Configuration tab
    PRECONDITIONS: 1) User has already subscribed for Fanzone
    PRECONDITIONS: 2) Fanzone should be enabled in System Configuration
    PRECONDITIONS: CMS--> System Configuration--> Structure-->Fanzone
    PRECONDITIONS: 3) Show In Home Page Launch Banner toggle should be Off in Fanzone Configuration(CMS)
    PRECONDITIONS: CMS-->Fanzone-->Fanzone Configurations
    PRECONDITIONS: 4) Fanzone related Banner's should be uploaded into SiteCore
    PRECONDITIONS: 5) Image Banner Url field should be inputted Sitecore team Id of the banner we want to display
    PRECONDITIONS: CMS-->Fanzone-->Fanzone Details
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        PRECONDITIONS: 1) User has already subscribed for Fanzone
        PRECONDITIONS: 2) Fanzone should be enabled in System Configuration
        PRECONDITIONS: CMS--> System Configuration--> Structure-->Fanzone
        PRECONDITIONS: 3) Show In Home Page Launch Banner toggle should be Off in Fanzone Configuration(CMS)
        PRECONDITIONS: CMS-->Fanzone-->Fanzone Configurations
        PRECONDITIONS: 4) Fanzone related Banner's should be uploaded into SiteCore
        PRECONDITIONS: 5) Image Banner Url field should be inputted Sitecore team Id of the banner we want to display
        PRECONDITIONS: CMS-->Fanzone-->Fanzone Details
        """
        fanzone_status = self.get_initial_data_system_configuration().get('Fanzone')
        if not fanzone_status.get('enabled'):
            self.cms_config.update_system_configuration_structure(config_item='Fanzone',
                                                                  field_name='enabled',
                                                                  field_value=True)
        everton_fanzone = self.cms_config.get_fanzone(vec.fanzone.TEAMS_LIST.everton.title())
        if everton_fanzone['active'] is not True:
            self.cms_config.update_fanzone(vec.fanzone.TEAMS_LIST.everton.title())
        if everton_fanzone['fanzoneConfiguration']['homePage']:
            self.cms_config.update_fanzone(vec.fanzone.TEAMS_LIST.everton.title(), homePage=False)

    def test_001_logon_to_lads_application(self):
        """
        DESCRIPTION: Logon to Lads application
        EXPECTED: User login should be successful
        """
        username = self.gvc_wallet_user_client.register_new_user().username
        self.site.login(username=username)

    def test_002_verify_launch_banner_is_not_populated_in_home_pagedesktop_and_under_highlights_tab_in_mobile(self):
        """
        DESCRIPTION: Verify Launch Banner is Not Populated in Home page(desktop) and under Highlights tab in mobile
        EXPECTED: Launch banner should not be populated
        """
        self.site.open_sport(name='FOOTBALL', fanzone=True)
        self.site.wait_content_state("football")
        dialog_fb = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_SHOW_US_YOUR_COLORS, timeout=30)
        dialog_fb.imin_button.click()
        wait_for_result(lambda: self.site.show_your_colors.items_as_ordered_dict,
                        name='OK button is displayed',
                        timeout=5)
        teams = self.site.show_your_colors.items_as_ordered_dict
        teams[vec.fanzone.TEAMS_LIST.everton.title()].scroll_to_we()
        teams[vec.fanzone.TEAMS_LIST.everton.title()].click()
        sleep(3)
        dialog_confirm = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_TEAM_CONFIRMATION, timeout=10)
        dialog_confirm.confirm_button.click()
        sleep(6)
        dialog_alert = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_TEAM_ALERTS)
        dialog_alert.exit_button.click()
        self.site.wait_content_state_changed(timeout=10)
        sleep(3)
        self.navigate_to_page("homepage")
        self.site.wait_content_state("homepage")
        self.assertFalse(self.site.home.fanzone_banner(), msg="Fanzone banner is displayed")

    @classmethod
    def custom_tearDown(cls):
        cms_config = cls.get_cms_config()
        cms_config.update_fanzone(vec.fanzone.TEAMS_LIST.everton.title(), homePage=True)