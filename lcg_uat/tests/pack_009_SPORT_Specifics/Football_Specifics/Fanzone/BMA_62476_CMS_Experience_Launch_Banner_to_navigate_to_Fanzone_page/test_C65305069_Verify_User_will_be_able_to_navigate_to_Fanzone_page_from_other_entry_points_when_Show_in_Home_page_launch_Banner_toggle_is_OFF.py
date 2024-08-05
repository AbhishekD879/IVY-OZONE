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
class Test_C65305069_Verify_User_will_be_able_to_navigate_to_Fanzone_page_from_other_entry_points_when_Show_in_Home_page_launch_Banner_toggle_is_OFF(Common):
    """
    TR_ID: C65305069
    NAME: Verify User will be able to navigate to Fanzone page from other entry points when Show in Home page launch Banner toggle is OFF
    DESCRIPTION: Verify User will be able to navigate to Fanzone page from other entry points when Show in Home page launch Banner toggle is OFF
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        PRECONDITIONS: 1) User has already subscribed for Fanzone
        PRECONDITIONS: 2) Fanzone should be enabled in System Configuration
        PRECONDITIONS: CMS--> System Configuration--> Structure-->Fanzone
        PRECONDITIONS: 3) Show In Home Page Launch Banner toggle should be OFF and all other Toggle's should be ON in Fanzone Configuration(CMS)
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
        newcastle_united_fanzone = self.cms_config.get_fanzone(vec.fanzone.TEAMS_LIST.tottenham_hotspur.title())
        if newcastle_united_fanzone:
            self.cms_config.update_fanzone(vec.fanzone.TEAMS_LIST.tottenham_hotspur.title(),
                                           homePage=False,
                                           sportsRibbon=True,
                                           footballHome=True,
                                           atozMenu=True)

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
        teams[vec.fanzone.TEAMS_LIST.tottenham_hotspur.title()].scroll_to_we()
        teams[vec.fanzone.TEAMS_LIST.tottenham_hotspur.title()].click()
        dialog_confirm = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_TEAM_CONFIRMATION,
                                                   verify_name=False)
        dialog_confirm.confirm_button.click()
        sleep(5)
        dialog_alert = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_TEAM_ALERTS,
                                                 verify_name=False)
        dialog_alert.exit_button.click()

    def test_002_verify_launch_banner_in_home_page_is_not_displayed(self):
        """
        DESCRIPTION: Verify Launch Banner in Home page is not displayed
        EXPECTED: Launch Banner in Home page should not be displayed
        """
        self.navigate_to_page("homepage")
        self.site.wait_content_state("homepage")
        if self.device_type == 'mobile':
            self.site.home.module_selection_ribbon.tab_menu.items_as_ordered_dict[
                vec.SB.MOBILE_FEATURED_MODULE_NAME].click()
        self.assertFalse(self.site.home.fanzone_banner(), msg="Fanzone banner is not displayed")

    def test_003_verify_user_is_able_to_navigate_to_fanzone_page_using_any_of_the_below_listed_entry_pointsa_launch_banner_in_football_landing_pageb_fanzone_in_a_z_menuc_sports_ribbonmobile(self):
        """
        DESCRIPTION: Verify user is able to navigate to Fanzone page using any of the below listed entry points
        DESCRIPTION: a. Launch Banner in Football landing page
        DESCRIPTION: b. Fanzone in A-Z menu
        DESCRIPTION: c. Sports Ribbon(Mobile)
        EXPECTED: User should be able to navigate to Fanzone page through of any the 3 listed entry points
        """
        # Sports ribbon menu
        if self.device_type == 'mobile':
            sports_menu = self.site.home.menu_carousel.items_as_ordered_dict
            fanzone_name = vec.SB.FANZONE
        else:
            sports_menu = self.site.header.sport_menu.items_as_ordered_dict
            fanzone_name = vec.SB.FANZONE.upper()
        self.assertIn(fanzone_name, sports_menu,
                      msg="Fanzone option is not displayed in Sports Ribbon Menu")

        # In AtoZ sports
        if self.device_type == 'mobile':
            # Top Sports
            self.site.open_sport(name='ALL SPORTS')
            sports = self.site.all_sports.top_sports_section.items_as_ordered_dict
            self.assertIn(vec.SB.FANZONE, sports, msg='Fanzone is not present in Top Sports')
            # A-Z Sports
            sports = self.site.all_sports.a_z_sports_section.items_as_ordered_dict
            self.assertIn(vec.SB.FANZONE, sports, msg='Fanzone is not present in A-Z Sports')
        else:
            # A - Z Sports
            sports = self.site.sport_menu.sport_menu_items_group('Main').items_as_ordered_dict
            self.assertIn(vec.SB.FANZONE, sports, msg='Fanzone is not present in A-Z Sports')

        # Football Page
        self.navigate_to_page("sport/football")
        self.site.wait_content_state("football")
        self.assertTrue(self.site.home.fanzone_banner(), msg="Fanzone banner is not displayed")

    @classmethod
    def custom_tearDown(cls):
        cms_config = cls.get_cms_config()
        cms_config.update_fanzone(vec.fanzone.TEAMS_LIST.tottenham_hotspur.title(),
                                  homePage=True,
                                  sportsRibbon=True,
                                  footballHome=True,
                                  atozMenu=True)
