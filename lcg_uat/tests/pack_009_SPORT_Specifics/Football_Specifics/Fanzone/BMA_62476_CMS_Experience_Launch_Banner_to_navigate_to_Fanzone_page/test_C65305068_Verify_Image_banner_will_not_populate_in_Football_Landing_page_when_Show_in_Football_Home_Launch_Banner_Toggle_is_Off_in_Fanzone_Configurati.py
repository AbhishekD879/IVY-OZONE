import pytest
from time import sleep
from voltron.utils.waiters import wait_for_result
from tests.base_test import vtest
from tests.Common import Common
from voltron.environments import constants as vec


@pytest.mark.lad_stg2
@pytest.mark.lad_tst2
@pytest.mark.lad_prod
# @pytest.mark.lad_hl
@pytest.mark.medium
@pytest.mark.other
@pytest.mark.desktop
@pytest.mark.fanzone
@vtest
class Test_C65305068_Verify_Image_banner_will_not_populate_in_Football_Landing_page_when_Show_in_Football_Home_Launch_Banner_Toggle_is_Off_in_Fanzone_Configuration_tab(Common):
    """
    TR_ID: C65305068
    NAME: Verify Image banner will not populate in Football Landing page when Show in Football Home Launch Banner Toggle is Off in Fanzone Configuration tab
    DESCRIPTION: Verify Image banner will not populate in Football Landing page when Show in Football Home Launch Banner Toggle is Off in Fanzone Configuration tab
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        PRECONDITIONS: 1) User has already subscribed for Fanzone
        PRECONDITIONS: 2) Fanzone should be enabled in System Configuration
        PRECONDITIONS: CMS--> System Configuration--> Structure-->Fanzone
        PRECONDITIONS: 3) Show In Football Home Launch Banner toggle should be OFF and all other Toggle's should be OFF in Fanzone Configuration(CMS)
        PRECONDITIONS: CMS-->Fanzone-->Fanzone Configurations
        PRECONDITIONS: 4) Fanzone related Banner's should be uploaded into SiteCore
        PRECONDITIONS: 5) Image Banner Url field should be inputted Sitecore team Id of the banner we want to display
        PRECONDITIONS: CMS-->Fanzone-->Fanzone Details
        PRECONDITIONS: 6) Fanzone should be created in CMS
        """
        fanzone_status = self.get_initial_data_system_configuration().get('Fanzone')
        if not fanzone_status.get('enabled'):
            self.cms_config.update_system_configuration_structure(config_item='Fanzone',
                                                                  field_name='enabled',
                                                                  field_value=True)
        newcastle_united_fanzone = self.cms_config.get_fanzone(vec.fanzone.TEAMS_LIST.newcastle_united.title())
        if newcastle_united_fanzone:
            self.cms_config.update_fanzone(vec.fanzone.TEAMS_LIST.newcastle_united.title(),
                                           homePage=False,
                                           sportsRibbon=False,
                                           footballHome=False,
                                           atozMenu=False)

    def test_001_logon_to_lads_application(self):
        """
        DESCRIPTION: Logon to Lads application
        EXPECTED: Login should be successful
        """
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
        teams[vec.fanzone.TEAMS_LIST.newcastle_united.title()].scroll_to_we()
        teams[vec.fanzone.TEAMS_LIST.newcastle_united.title()].click()
        dialog_confirm = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_TEAM_CONFIRMATION,
                                                   verify_name=False)
        dialog_confirm.confirm_button.click()
        sleep(5)
        dialog_alert = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_TEAM_ALERTS,
                                                 verify_name=False)
        dialog_alert.exit_button.click()

    def test_002_navigate_to_football_landing_page(self):
        """
        DESCRIPTION: Navigate to Football landing page
        EXPECTED: User should be able to navigate to Football landing page
        """
        # Football Page
        self.navigate_to_page("sport/football")
        self.site.wait_content_state("football")

    def test_003_launch_banner_is_not_displayed(self):
        """
        DESCRIPTION: Launch Banner is not displayed
        EXPECTED: Launch Banner shouldn't be displayed
        """
        self.assertFalse(self.site.home.fanzone_banner(), msg="Fanzone banner is displayed")

    @classmethod
    def custom_tearDown(cls):
        cms_config = cls.get_cms_config()
        cms_config.update_fanzone(vec.fanzone.TEAMS_LIST.newcastle_united.title(),
                                  homePage=True,
                                  sportsRibbon=True,
                                  footballHome=True,
                                  atozMenu=True)
