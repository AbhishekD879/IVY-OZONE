import pytest
from time import sleep
from voltron.environments import constants as vec
from tests.base_test import vtest
from tests.Common import Common
from voltron.utils.waiters import wait_for_result


@pytest.mark.lad_tst2
@pytest.mark.lad_stg2
@pytest.mark.lad_prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.fanzone
@pytest.mark.other
@vtest
class Test_C65305029_Verify_3_tabs_Now_Next_Stats_and_Club_tabs_in_Fanzone_page(Common):
    """
    TR_ID: C65305029
    NAME: Verify 3 tabs Now & Next Stats and Club tabs in Fanzone page
    DESCRIPTION: Verify 3 tabs Now & Next Stats and Club tabs in Fanzone page
    PRECONDITIONS: 1) User login should be successful
    PRECONDITIONS: 2) User has already subscribed for Fanzone
    PRECONDITIONS: 3) Fanzone should be enabled in System Configuration
    PRECONDITIONS: CMS--> System Configuration--> Structure-->Fanzone
    PRECONDITIONS: 4) All the entry points should be enabled in Fanzone Configuration(CMS)
    PRECONDITIONS: CMS-->Fanzone-->Fanzone Configurations
    PRECONDITIONS: 5) Image should be uploaded in Site core and image id should be inputted while creating the Fanzone for respective teams
    PRECONDITIONS: 6) Fanzone should be enabled in A-Z menu and Sports Ribbon
    PRECONDITIONS: CMS-->Sports Pages-->Sport Categories-->Fanzone-->General Sport Configuration
    PRECONDITIONS: 7) Toggle should be ON for all the 3 tabs Now & Next, Stats and Club in CMS->Fanzone->Fanzone Details page
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        PRECONDITIONS: 1) User login should be successful
        PRECONDITIONS: 2) User has already subscribed for Fanzone
        PRECONDITIONS: 3) Fanzone should be enabled in System Configuration
        PRECONDITIONS: CMS--> System Configuration--> Structure-->Fanzone
        PRECONDITIONS: 4) All the entry points should be enabled in Fanzone Configuration(CMS)
        PRECONDITIONS: CMS-->Fanzone-->Fanzone Configurations
        PRECONDITIONS: 5) Image should be uploaded in Site core and image id should be inputted while creating the Fanzone for respective teams
        PRECONDITIONS: 6) Fanzone should be enabled in A-Z menu and Sports Ribbon
        PRECONDITIONS: CMS-->Sports Pages-->Sport Categories-->Fanzone-->General Sport Configuration
        PRECONDITIONS: 7) Toggle should be ON for all the 3 tabs Now & Next, Stats and Club in CMS->Fanzone->Fanzone Details page
        """
        fanzone_status = self.get_initial_data_system_configuration().get('Fanzone')
        if not fanzone_status.get('enabled'):
            self.cms_config.update_system_configuration_structure(config_item='Fanzone',
                                                                  field_name='enabled',
                                                                  field_value=True)
        astonVilla_fanzone = self.cms_config.get_fanzone(vec.fanzone.TEAMS_LIST.aston_villa.title())
        if astonVilla_fanzone['active'] is not True:
            self.cms_config.update_fanzone(vec.fanzone.TEAMS_LIST.aston_villa.title())
        if astonVilla_fanzone['fanzoneConfiguration']['showStats'] is not True:
            self.cms_config.update_fanzone(vec.fanzone.TEAMS_LIST.aston_villa.title(), showStats=True)
        if astonVilla_fanzone['fanzoneConfiguration']['showClubs'] is not True:
            self.cms_config.update_fanzone(vec.fanzone.TEAMS_LIST.aston_villa.title(), showClubs=True)
        if astonVilla_fanzone['fanzoneConfiguration']['showClubs'] is not True:
            self.cms_config.update_fanzone(vec.fanzone.TEAMS_LIST.aston_villa.title(), showNowNext=True)
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

    def test_001_navigate_to_fanzone_page_via_any_of_below_entry_pointsa_fanzone_in_a_z_menub_fanzone_in_sports_ribbonmobile_onlyc_launch_banner_in_home_pagehighlights_tabd_launch_banner_in_football_slp(
            self):
        """
        DESCRIPTION: Navigate to Fanzone page via any of below entry points
        DESCRIPTION: a) Fanzone in A-Z menu
        DESCRIPTION: b) Fanzone in Sports Ribbon(Mobile only)
        DESCRIPTION: c) Launch banner in Home page/Highlights tab
        DESCRIPTION: d) Launch banner in Football SLP
        EXPECTED: User should be able to navigate to Fanzone Page
        """
        # banner = wait_for_result(lambda: self.site.home.fanzone_banner(), timeout=10)
        # banner.let_me_see.click()   as per the new change, after subscription, we will be in fanzone page only

    def test_002_check_all_the_3_tabs_now__next_stats_and_club_are_displayed(self):
        """
        DESCRIPTION: Check all the 3 tabs Now & Next, Stats, and Club are displayed
        EXPECTED: All the 3 tabs should be displayed
        EXPECTED: Note: If Toggle is Off for any of the tab in CMS, then that particular tab will not be populated
        """
        tabs_menu = self.site.fanzone.tabs_menu.items_as_ordered_dict
        self.assertIn(vec.fanzone.NOW_AND_NEXT, tabs_menu,
                      msg=f'"{vec.fanzone.NOW_AND_NEXT}" tab is not present in tabs menu')
        self.assertIn(vec.fanzone.CLUB, tabs_menu,
                      msg=f'"{vec.fanzone.CLUB}" tab is not present in tabs menu')
        self.assertIn(vec.fanzone.STATS, tabs_menu, msg=f'"{vec.fanzone.STATS}" tab is not present in tabs menu')
