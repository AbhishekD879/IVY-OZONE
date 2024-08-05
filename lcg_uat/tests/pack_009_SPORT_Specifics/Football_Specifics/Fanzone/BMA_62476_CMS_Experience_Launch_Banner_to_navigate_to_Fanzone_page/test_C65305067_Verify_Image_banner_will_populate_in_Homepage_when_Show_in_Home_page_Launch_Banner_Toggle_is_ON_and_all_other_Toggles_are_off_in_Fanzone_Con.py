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
class Test_C65305067_Verify_Image_banner_will_populate_in_Homepage_when_Show_in_Home_page_Launch_Banner_Toggle_is_ON_and_all_other_Toggles_are_off_in_Fanzone_Configuration_tab(Common):
    """
    TR_ID: C65305067
    NAME: Verify Image banner will populate in Homepage when Show in Home page Launch Banner Toggle is ON and all other Toggle's are off in Fanzone Configuration tab
    DESCRIPTION: Verify Image banner will populate in Homepage when Show in Home page Launch Banner Toggle is ON and all other Toggle's are off in Fanzone Configuration tab
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        PRECONDITIONS: 1) User has already subscribed for Fanzone
        PRECONDITIONS: 2) Fanzone should be enabled in System Configuration
        PRECONDITIONS: CMS--> System Configuration--> Structure-->Fanzone
        PRECONDITIONS: 3) Show In Home Page Launch Banner toggle should be ON and all other Toggle's should be OFF in Fanzone Configuration(CMS)
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
        west_ham_fanzone = self.cms_config.get_fanzone(vec.fanzone.TEAMS_LIST.west_ham_united.title())
        if west_ham_fanzone:
            self.cms_config.update_fanzone(vec.fanzone.TEAMS_LIST.west_ham_united.title(), homePage=True,
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
        teams[vec.fanzone.TEAMS_LIST.west_ham_united.title()].scroll_to_we()
        teams[vec.fanzone.TEAMS_LIST.west_ham_united.title()].click()
        dialog_confirm = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_TEAM_CONFIRMATION,
                                                   verify_name=False)
        dialog_confirm.confirm_button.click()
        sleep(5)
        dialog_alert = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_TEAM_ALERTS,
                                                 verify_name=False)
        dialog_alert.exit_button.click()

    def test_002_verify_launch_banner_is_displayed_without_any_distortion_to_actual_ui(self):
        """
        DESCRIPTION: Verify Launch Banner is displayed without any distortion to actual UI
        EXPECTED: Launch Banner should be displayed without any distortion
        """
        self.navigate_to_page("homepage")
        self.site.wait_content_state("homepage")
        if self.device_type == 'mobile':
            self.site.home.module_selection_ribbon.tab_menu.items_as_ordered_dict[vec.SB.MOBILE_FEATURED_MODULE_NAME].click()
        self.assertTrue(self.site.home.fanzone_banner(), msg="Fanzone banner is not displayed")

        # Sports ribbon menu
        if self.device_type == 'mobile':
            sports_menu = self.site.home.menu_carousel.items_as_ordered_dict
        else:
            sports_menu = self.site.header.sport_menu.items_as_ordered_dict
        self.assertNotIn(vec.SB.FANZONE.upper(), sports_menu,
                         msg="Fanzone option is displayed in Sports Ribbon Menu")

        # In AtoZ sports
        if self.device_type == 'mobile':
            # Top Sports
            self.site.open_sport(name='ALL SPORTS')
            sports = self.site.all_sports.top_sports_section.items_as_ordered_dict
            self.assertNotIn(vec.SB.FANZONE, sports, msg='Fanzone is present in Top Sports')
            # A-Z Sports
            sports = self.site.all_sports.a_z_sports_section.items_as_ordered_dict
            self.assertNotIn(vec.SB.FANZONE, sports, msg='Fanzone is present in A-Z Sports')
        else:
            # A - Z Sports
            sports = self.site.sport_menu.sport_menu_items_group('Main').items_as_ordered_dict
            self.assertNotIn(vec.SB.FANZONE, sports, msg='Fanzone is present in A-Z Sports')

        #Football Page
        self.navigate_to_page("sport/football")
        self.site.wait_content_state("football")
        self.assertFalse(self.site.home.fanzone_banner(), msg="Fanzone banner is displayed")


    @classmethod
    def custom_tearDown(cls):
        cms_config = cls.get_cms_config()
        cms_config.update_fanzone(vec.fanzone.TEAMS_LIST.west_ham_united.title(),
                                  homePage=True,
                                  sportsRibbon=True,
                                  footballHome=True,
                                  atozMenu=True)

