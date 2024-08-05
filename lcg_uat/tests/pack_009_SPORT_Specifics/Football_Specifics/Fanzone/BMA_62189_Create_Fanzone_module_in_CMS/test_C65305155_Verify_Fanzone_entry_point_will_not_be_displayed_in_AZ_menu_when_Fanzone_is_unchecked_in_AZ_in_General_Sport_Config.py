import pytest
import voltron.environments.constants as vec
from tests.base_test import vtest
from tests.Common import Common
from time import sleep
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
class Test_C65305155_Verify_Fanzone_entry_point_will_not_be_displayed_in_AZ_menu_when_Fanzone_is_unchecked_in_AZ_in_General_Sport_Config(Common):
    """
    TR_ID: C65305155
    NAME: Verify Fanzone entry point will not be displayed in A-Z menu when Fanzone is unchecked for Show in AZ in General Sport Configuration
    DESCRIPTION: Verify Fanzone entry point will not be displayed in A-Z menu when Fanzone is unchecked for Show in AZ in General Sport Configuration
    PRECONDITIONS: 1) Fanzone should be enabled in System Configuration
    PRECONDITIONS: CMS--> System Configuration--> Structure-->Fanzone
    PRECONDITIONS: 2) Fanzone records should be created
    PRECONDITIONS: 3) Toggle should be ON for all the listed items in Fanzone Configuration(CMS)
    PRECONDITIONS: CMS-->Fanzone-->Fanzone Configurations
    PRECONDITIONS: 4) Show in A-Z menu should be checked
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        PRECONDITIONS: 1) Fanzone should be enabled in System Configuration
        PRECONDITIONS: CMS--> System Configuration--> Structure-->Fanzone
        PRECONDITIONS: 2) Fanzone records should be created
        PRECONDITIONS: 3) Toggle should be ON for all the listed items in Fanzone Configuration(CMS)
        PRECONDITIONS: CMS-->Fanzone-->Fanzone Configurations
        PRECONDITIONS: 4) Show in Sports Ribbon should be checked
        """

        fanzone_status = self.get_initial_data_system_configuration().get('Fanzone')
        if not fanzone_status.get('enabled'):
            self.cms_config.update_system_configuration_structure(config_item='Fanzone',
                                                                  field_name='enabled',
                                                                  field_value=True)
        tottenham_hotspur_atozMenu = self.cms_config.get_fanzone(vec.fanzone.TEAMS_LIST.tottenham_hotspur.title())['fanzoneConfiguration']['atozMenu']
        if tottenham_hotspur_atozMenu:
            self.cms_config.update_fanzone(vec.fanzone.TEAMS_LIST.tottenham_hotspur.title(), atozMenu=False)
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
        sleep(6)
        dialog_alert = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_TEAM_ALERTS,
                                                 verify_name=False)
        dialog_alert.exit_button.click()
        self.site.wait_content_state_changed(timeout=10)

    def test_001_login_in_to_cms_and_navigate_to_sports_pages__gtsports_categories(self):
        """
        DESCRIPTION: Login in to CMS and navigate to Sports Pages--&gt;Sports Categories
        EXPECTED: User should be able to navigate to Sports Categories
        """
        # covered in step 0

    def test_002_click_on_fanzone(self):
        """
        DESCRIPTION: Click on Fanzone
        EXPECTED: Fanzone page should open
        """
        # covered in step 0

    def test_003_click_on_down_arrow_in_general_sport_configuration_and_uncheck_show_in_az_click_on_save_change_button(
            self):
        """
        DESCRIPTION: Click on down arrow in General Sport configuration and uncheck Show in AZ ,click on save change button
        EXPECTED: Changes should be successful
        """
        # covered in step 0

    def test_004_login_to_lads_application(self):
        """
        DESCRIPTION: login to Lads application
        EXPECTED: Login should be successful
        """
        # covered in step 0

    def test_005_verify_fanzoneentry_point_is_not_displayed_in_a_z_menu(self):
        """
        DESCRIPTION: Verify Fanzone(entry point) is not displayed in A-Z menu
        EXPECTED: Fanzone shouldn't be displayed in A-Z menu
        """
        self.navigate_to_page(name='Homepage')
        if self.device_type == 'mobile':
            # Top Sports
            self.site.open_sport(name='ALL SPORTS')
            sports = self.site.all_sports.top_sports_section.items_as_ordered_dict
            self.assertNotIn('Fanzone', sports, msg='Fanzone is present in Top Sports')
            # A-Z Sports
            sports = self.site.all_sports.a_z_sports_section.items_as_ordered_dict
            self.assertNotIn('Fanzone', sports, msg='Fanzone is present in A-Z Sports')
        else:
            # A - Z Sports
            self.__class__.sports = self.site.sport_menu.sport_menu_items_group('Main').items_as_ordered_dict
            self.assertNotIn('Fanzone', self.sports, msg='Fanzone is present in A-Z Sports')

    def test_006_verify_user_is_able_to_navigate_to_fanzone_page_through_below_listed_entry_points1_launch_banner_in_home_page2_launch_banner_in_football_slp3_sports_ribbonmobile(
            self):
        """
        DESCRIPTION: Verify user is able to navigate to Fanzone page through below listed entry points
        DESCRIPTION: 1. Launch Banner in Home page
        DESCRIPTION: 2. Launch Banner in Football SLP
        DESCRIPTION: 3. Sports Ribbon(mobile)
        EXPECTED: User should be able to navigate to Fanzone page
        """
        self.navigate_to_page(name='Homepage')
        self.site.wait_content_state("homepage")
        if self.device_type == 'desktop':
            self.assertTrue(self.site.header.sport_menu.items_as_ordered_dict.get(vec.sb.FANZONE.upper()),
                            msg="Fanzone option is displayed in Sports Ribbon Menu")
        else:
            self.site.home.module_selection_ribbon.tab_menu.items_as_ordered_dict.get(
                vec.racing.RACING_HIGHLIGHTS_TAB_NAME).click()
            sleep(10)
            self.assertTrue(self.site.home.menu_carousel.items_as_ordered_dict.get(
                vec.sb.FANZONE), msg="Fanzone option is displayed in Sports Ribbon Menu")

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

    @classmethod
    def custom_tearDown(cls):
        # Reverting the AtoZ fanzone configuration
        cms_config = cls.get_cms_config()
        cms_config.update_fanzone(vec.fanzone.TEAMS_LIST.tottenham_hotspur.title(), atozMenu=True)
