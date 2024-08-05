import pytest
from tests.base_test import vtest
from voltron.utils.waiters import wait_for_result
from voltron.environments import constants as vec
from tests.Common import Common
from time import sleep


@pytest.mark.lad_stg2
@pytest.mark.lad_tst2
@pytest.mark.lad_prod
@pytest.mark.medium
@pytest.mark.other
@pytest.mark.desktop
@pytest.mark.fanzone
@vtest
class Test_C65305030_Verify_only_Now_Next_tab_is_populated_when_other_tabs_are_not_available_also_validate_the_data(Common):
    """
    TR_ID: C65305030
    NAME: Verify only Now and Next tab is populated when other tabs are not available also validate the data
    DESCRIPTION: Verify only Now and Next tab is populated when other tabs are not available also validate the data
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
            self.cms_config.update_fanzone(vec.fanzone.TEAMS_LIST.aston_villa.title(),
                                           typeId=self.football_config.autotest_class.autotest_premier_league.type_id)
        if astonVilla_fanzone['fanzoneConfiguration']['sportsRibbon'] is False:
            self.cms_config.update_fanzone(vec.fanzone.TEAMS_LIST.aston_villa.title(), sportsRibbon=True)

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
        dialog_confirm = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_TEAM_CONFIRMATION, verify_name=False)
        dialog_confirm.confirm_button.click()
        sleep(3)
        dialog_alert = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_TEAM_ALERTS, verify_name=False)
        dialog_alert.exit_button.click()

    def test_001_navigate_to_fanzone_page_via_any_of_below_entry_pointsa_fanzone_in_a_z_menub_fanzone_in_sports_ribbonmobile_onlyc_launch_banner_in_home_pagehighlights_tabd_launch_banner_in_football_slp(self):
        """
        DESCRIPTION: Navigate to Fanzone page via any of below entry points
        DESCRIPTION: a) Fanzone in A-Z menu
        DESCRIPTION: b) Fanzone in Sports Ribbon(Mobile only)
        DESCRIPTION: c) Launch banner in Home page/Highlights tab
        DESCRIPTION: d) Launch banner in Football SLP
        EXPECTED: User should be able to navigate to Fanzone Page
        """
        self.navigate_to_page("homepage")
        self.site.wait_content_state("homepage")
        if self.device_type == 'desktop':
            self.assertTrue(self.site.header.sport_menu.items_as_ordered_dict.get(vec.sb.FANZONE.upper()),
                            msg="Fanzone option is not displayed in Sports Ribbon Menu")
            self.site.header.sport_menu.items_as_ordered_dict.get(vec.sb.FANZONE.upper()).click()
        else:
            self.assertTrue(self.site.home.menu_carousel.items_as_ordered_dict.get(
                vec.sb.FANZONE), msg="Fanzone option is not displayed in Sports Ribbon Menu")
            self.site.home.menu_carousel.items_as_ordered_dict.get(vec.sb.FANZONE).click()
        self.site.wait_content_state_changed(timeout=10)

    def test_002_verify_only_now_and_next_tab_data_is_populated(self):
        """
        DESCRIPTION: Verify only Now and Next tab data is populated
        EXPECTED: Only Now & Next tab should be displayed
        """
        wait_for_result(lambda: self.site.fanzone.tabs_menu.current,
                        name='Fanzone page not displayed',
                        timeout=5)
        current_tab = self.site.fanzone.tabs_menu.current
        self.assertEqual(current_tab, vec.fanzone.NOW_AND_NEXT,
                         msg=f'Actual Tab "{current_tab}", is not same '
                             f' expected tab "{vec.fanzone.NOW_AND_NEXT}"')

    def test_003_surface_bets__hclooks_like__standings_and_outright_information_should_be_displayednote_above_information_will_be_populated_upon_configuration_only(self):
        """
        DESCRIPTION: Surface Bets , HC(Looks like) , Standings and Outright information should be displayed
        DESCRIPTION: Note: Above information will be populated upon configuration only
        EXPECTED: Data should be populated as per configuration from CMS
        """
        tab_content = self.site.fanzone.tab_content
        self.assertTrue(tab_content, msg='data not populated as per cms config')
