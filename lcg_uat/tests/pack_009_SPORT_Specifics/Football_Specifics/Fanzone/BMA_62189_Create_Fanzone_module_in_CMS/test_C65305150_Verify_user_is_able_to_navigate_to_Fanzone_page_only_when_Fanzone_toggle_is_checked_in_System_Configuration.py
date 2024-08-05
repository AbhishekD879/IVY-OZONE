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
class Test_C65305150_Verify_user_is_able_to_navigate_to_Fanzone_page_only_when_Fanzone_toggle_is_checked_in_System_Configuration(Common):
    """
    TR_ID: C65305150
    NAME: Verify user is able to navigate to Fanzone page only when Fanzone toggle is checked in System Configuration
    DESCRIPTION: Verify user is able to navigate to Fanzone page only when Fanzone toggle is checked in System Configuration
    PRECONDITIONS: 1) User has Logged into CMS-->Lads
    PRECONDITIONS: 2) Fanzone should be enabled in System Configuration
    PRECONDITIONS: CMS--> System Configuration--> Structure-->Fanzone
    PRECONDITIONS: 3) Fanzone records should be created
    PRECONDITIONS: 4) Toggle should be On for all the listed items in Fanzone Configuration(CMS)
    PRECONDITIONS: CMS-->Fanzone-->Fanzone Configurations
    """
    keep_browser_open = True

    def fanzone_page_verification(self):
        sleep(5)
        self.assertEqual(self.site.fanzone.header_line.page_title.text, vec.sb.FANZONE,
                         msg=f'Actual page title "{self.site.fanzone.header_line.page_title.text}" '
                             f'is not same as Expected title "{vec.sb.FANZONE}"')

    def test_000_preconditions(self):
        """PRECONDITIONS: 1) User has Logged into CMS-->Lads
        PRECONDITIONS: 2) Fanzone should be enabled in System Configuration
        PRECONDITIONS: CMS--> System Configuration--> Structure-->Fanzone
        PRECONDITIONS: 3) Fanzone records should be created
        PRECONDITIONS: 4) Toggle should be On for all the listed items in Fanzone Configuration(CMS)
        PRECONDITIONS: CMS-->Fanzone-->Fanzone Configurations"""
        fanzone_status = self.get_initial_data_system_configuration().get('Fanzone')
        if not fanzone_status.get('enabled'):
            self.cms_config.update_system_configuration_structure(config_item='Fanzone',
                                                                  field_name='enabled',
                                                                  field_value=True)
        username = self.gvc_wallet_user_client.register_new_user().username
        self.site.wait_content_state('Homepage', timeout=30)
        self.site.login(username=username, timeout=30)
        self.site.open_sport(name='FOOTBALL', fanzone=True, timeout=30)
        dialog_fb = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_SHOW_US_YOUR_COLORS, timeout=30)
        dialog_fb.imin_button.click()
        wait_for_result(lambda: self.site.show_your_colors.items_as_ordered_dict,
                        name='All teams to be displayed')
        teams = self.site.show_your_colors.items_as_ordered_dict
        teams[vec.fanzone.TEAMS_LIST.aston_villa.title()].click()
        sleep(3)
        dialog_confirm = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_TEAM_CONFIRMATION, timeout=30)
        dialog_confirm.confirm_button.click()
        sleep(5)
        dialog_alert = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_TEAM_ALERTS, timeout=30)
        dialog_alert.exit_button.click()

    def test_001_login_to_lads_application(self):
        """
        DESCRIPTION: login to Lads application
        EXPECTED: Login should be successful
        """
        self.navigate_to_page("homepage")
        self.site.wait_content_state("homepage", timeout=30)

    def test_002_verify_below_entry_points_are_displayeda_launch_banner_in_home_pageb_fanzone_in_a_z_menuc_fanzone_in_sports_ribbonmobiled_launch_banner_in_football_landing_page(self):
        """
        DESCRIPTION: Verify below entry points are displayed
        DESCRIPTION: a. Launch Banner in home page
        DESCRIPTION: b. Fanzone in A-Z menu
        DESCRIPTION: c. Fanzone in Sports Ribbon(mobile)
        DESCRIPTION: d. Launch Banner in Football landing page
        EXPECTED: All the entry points should be listed
        EXPECTED: Note: If any of the entry point toggle is Off, then that particular entry point will not displayed
        """
        entry_points = self.cms_config.get_fanzone(vec.fanzone.TEAMS_LIST.aston_villa.title())['fanzoneConfiguration']
        self.__class__.az_menu = entry_points['atozMenu']
        if self.az_menu:
            # Fanzone in A-Z menu
            if self.device_type == 'mobile':
                # Top Sports
                self.site.open_sport(name='ALL SPORTS')
                sports = self.site.all_sports.top_sports_section.items_as_ordered_dict
                self.assertIn('Fanzone', sports, msg='Fanzone is not present in Top Sports')
                # A-Z Sports
                sports = self.site.all_sports.a_z_sports_section.items_as_ordered_dict
                self.assertIn('Fanzone', sports, msg='Fanzone is not present in A-Z Sports')
            else:
                # A - Z Sports
                self.__class__.sports = self.site.sport_menu.sport_menu_items_group('Main').items_as_ordered_dict
                self.assertIn('Fanzone', self.sports, msg='Fanzone is not present in A-Z Sports')
        else:
            self._logger.info(f"**** A-Z entry point toggle is off in CMS for {vec.fanzone.TEAMS_LIST.aston_villa.title()}")

        self.__class__.sports_ribbon = entry_points['sportsRibbon']
        if self.sports_ribbon:
            # sports ribbon
            if self.device_type == 'desktop':
                self.assertTrue(self.site.header.sport_menu.items_as_ordered_dict.get(vec.sb.FANZONE.upper()),
                                msg="Fanzone option is not displayed in Sports Ribbon Menu")
            else:
                self.navigate_to_page('Homepage')
                self.assertTrue(self.site.home.menu_carousel.items_as_ordered_dict.get(
                    vec.sb.FANZONE), msg="Fanzone option is not displayed in Sports Ribbon Menu")
        else:
            self._logger.info(
                f"**** sports ribbon entry point toggle is off in CMS for {vec.fanzone.TEAMS_LIST.aston_villa.title()}")

        self.__class__.home_page = entry_points['homePage']
        if self.home_page:
            # Launch Banner in home page
            if tests.settings.device_type == "mobile":
                self.site.home.module_selection_ribbon.tab_menu.items_as_ordered_dict.get(
                    vec.racing.RACING_HIGHLIGHTS_TAB_NAME).click()
            self.assertTrue(self.site.home.fanzone_banner(), msg="Fanzone banner is not displayed")
        else:
            self._logger.info(
                f"**** Homepage entry point toggle is off in CMS for {vec.fanzone.TEAMS_LIST.aston_villa.title()}")

        self.__class__.football_page = entry_points['footballHome']
        if self.football_page:
            # Launch Banner in Football landing page
            self.navigate_to_page("sport/football")
            self.site.wait_content_state("football")
            self.assertTrue(self.site.home.fanzone_banner(), msg="Fanzone banner is not displayed")
        else:
            self._logger.info(
                f"**** Football entry point toggle is off in CMS for {vec.fanzone.TEAMS_LIST.aston_villa.title()}")

    def test_003_verify_user_is_able_to_navigate_to_fanzone_page_through_any_of_the_4_entry_points_listed_in_step_no_2(self):
        """
        DESCRIPTION: Verify user is able to navigate to Fanzone page through any of the 4 entry points listed in step no 2
        EXPECTED: User should be able to navigate to Fanzone page
        """
        if self.football_page:
            fanzone_banner = self.site.home.fanzone_banner()
            fanzone_banner.let_me_see.click()
            self.fanzone_page_verification()
        else:
            self._logger.info(
                f"**** Football entry point toggle is off in CMS for {vec.fanzone.TEAMS_LIST.aston_villa.title()}")

    def test_004_note_user_should_be_able_to_navigate_through_all_the_entry_points(self):
        """
        DESCRIPTION: Note: User should be able to navigate through all the entry points
        """
        if self.home_page:
            # Launch Banner in home page
            self.test_001_login_to_lads_application()
            if tests.settings.device_type == "mobile":
                self.site.home.module_selection_ribbon.tab_menu.items_as_ordered_dict.get(
                    vec.racing.RACING_HIGHLIGHTS_TAB_NAME).click()
            fanzone_banner = self.site.home.fanzone_banner()
            fanzone_banner.let_me_see.click()
            self.fanzone_page_verification()
        else:
            self._logger.info(
                f"**** Homepage entry point toggle is off in CMS for {vec.fanzone.TEAMS_LIST.aston_villa.title()}")

        if self.az_menu:
            # Fanzone in A-Z menu
            self.test_001_login_to_lads_application()
            if self.device_type == 'mobile':
                self.site.open_sport(name='ALL SPORTS')
                self.site.all_sports.click_item(vec.sb.FANZONE)
            else:
                self.site.sport_menu.click_item(vec.sb.FANZONE)
            self.fanzone_page_verification()
        else:
            self._logger.info(
                f"**** A-Z entry point toggle is off in CMS for {vec.fanzone.TEAMS_LIST.aston_villa.title()}")

        if self.sports_ribbon:
            # sports ribbon
            self.test_001_login_to_lads_application()
            if self.device_type == 'desktop':
                self.site.header.sport_menu.items_as_ordered_dict.get(vec.sb.FANZONE.upper()).click()
            else:
                self.site.home.menu_carousel.items_as_ordered_dict.get(vec.sb.FANZONE).click()
            self.fanzone_page_verification()
        else:
            self._logger.info(
                f"**** Sports Ribbon entry point toggle is off in CMS for {vec.fanzone.TEAMS_LIST.aston_villa.title()}")
