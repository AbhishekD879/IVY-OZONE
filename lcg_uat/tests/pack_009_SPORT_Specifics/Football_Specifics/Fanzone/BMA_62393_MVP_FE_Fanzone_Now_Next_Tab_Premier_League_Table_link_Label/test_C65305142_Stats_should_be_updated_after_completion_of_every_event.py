import voltron.environments.constants as vec
import pytest
import tests
from time import sleep
from crlat_cms_client.utils.exceptions import CMSException
from tests.base_test import vtest
from tests.Common import Common
from voltron.utils.waiters import wait_for_result


@pytest.mark.lad_stg2
@pytest.mark.lad_tst2
@pytest.mark.lad_prod
# @pytest.mark.lad_hl
@pytest.mark.medium
@pytest.mark.other
@pytest.mark.desktop
@pytest.mark.fanzone
@vtest
class Test_C65305142_Stats_should_be_updated_after_completion_of_every_event(Common):
    """
    TR_ID: C65305142
    NAME: Stats should be updated after completion of every event
    DESCRIPTION: Verify user should be able to see updated Stats after completion of every event
    PRECONDITIONS: 1)User has access to CMS and valid credentials to login
    PRECONDITIONS: 2)User has access to FE and valid credentials to login
    PRECONDITIONS: 3)Fanzone option is enabled in Structure and Fanzone entry points in Fanzone section in CMS
    PRECONDITIONS: 4)Premier league table and icon is configured in CMS successfully , League table is mapped to the Team for the competition team is playing
    PRECONDITIONS: 5)User has logged into Lads FE and is on Fanzone page
    """
    keep_browser_open = True

    def test_000_preconditions(self):
        """
        DESCRIPTION: Active the fanzone team and register a new user
        EXPECTED: Fanzone team is activated in cms and logged into the application
        """
        fanzone_status = self.get_initial_data_system_configuration().get(vec.sb.FANZONE)
        if not fanzone_status.get('enabled'):
            self.cms_config.update_system_configuration_structure(config_item='Fanzone',
                                                                  field_name='enabled',
                                                                  field_value=True)
        astonvilla_fanzone = self.cms_config.get_fanzone(vec.fanzone.TEAMS_LIST.aston_villa.title())
        if not astonvilla_fanzone['fanzoneConfiguration']['showCompetitionTable']:
            raise CMSException(f'"showCompetitionTable is not enabled for {vec.fanzone.TEAMS_LIST.aston_villa.title()}"')
        if tests.settings.backend_env != 'prod':
            event = self.ob_config.add_autotest_premier_league_football_outright_event()
            selection_name, selection_id = list(event.selection_ids.items())[0]
            self.ob_config.map_fanzone_event_selection_id(selection_id=selection_id,
                                                          fanzone_team=vec.fanzone.TEAMS_LIST.aston_villa,
                                                          team_external_id=self.ob_config.football_config.fanzone_external_id.aston_villa)
            self.cms_config.update_fanzone(vec.fanzone.TEAMS_LIST.aston_villa.title(),
                                           typeId=str(self.ob_config.football_config.autotest_class.autotest_premier_league.type_id))
        else:
            self.cms_config.update_fanzone(vec.fanzone.TEAMS_LIST.aston_villa.title())
        self.__class__.username = self.gvc_wallet_user_client.register_new_user().username
        self.site.login(username=self.username)
        self.site.open_sport(name='FOOTBALL', fanzone=True)
        self.site.wait_content_state("football", timeout=30)
        dialog_fb = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_SHOW_US_YOUR_COLORS, timeout=30)
        dialog_fb.imin_button.click()
        wait_for_result(lambda: self.site.show_your_colors.items_as_ordered_dict,
                        name='SYC is displayed',
                        timeout=5)
        teams = self.site.show_your_colors.items_as_ordered_dict
        teams[vec.fanzone.TEAMS_LIST.aston_villa.title()].scroll_to_we()
        teams[vec.fanzone.TEAMS_LIST.aston_villa.title()].click()
        dialog_confirm = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_TEAM_CONFIRMATION)
        dialog_confirm.confirm_button.click()
        sleep(3)
        dialog_alert = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_TEAM_ALERTS)
        dialog_alert.exit_button.click()

    def test_001_verify_if_user_is_able_to_see_premier_league_table_and_icon_in_now_and_next_tab_in_fe(self):
        """
        DESCRIPTION: Verify If user is able to see Premier League table and icon in Now and Next Tab in FE
        EXPECTED: User should be able to see Premier League table and icon in Now and Next Tab in FE
        """
        tabs_menu = self.site.fanzone.tabs_menu.items_as_ordered_dict
        self.assertIn(vec.fanzone.NOW_AND_NEXT, tabs_menu,
                      msg=f'"{vec.fanzone.NOW_AND_NEXT}" tab is not present in tabs menu')
        self.site.fanzone.tabs_menu.click_button(button_name=vec.fanzone.NOW_AND_NEXT)
        self.assertTrue(self.site.fanzone.premier_leauge_link, msg="Premier League Table is not displayed")

    def test_002_click_on_the_teams_bets_header_link(self):
        """
        DESCRIPTION: Click on the Teams bets header link
        EXPECTED: User should be able to see the league table is opened as overlay with close option(X)
        """
        self.device.driver.execute_script("return arguments[0].click();", self.site.fanzone.premier_leauge_link)
        self.assertTrue(self.site.fanzone.premier_leauge.close_button,
                        msg="Close Button in Premier League Table is not displayed")

    def test_003_click_on_close_x_option_in_overlay(self):
        """
        DESCRIPTION: Click on Close (X) option in overlay
        EXPECTED: League table overlay should be closed
        """
        self.site.fanzone.premier_leauge.close_button.click()

    def test_004_logout_from_applicationwait_for_the_events_to_complete(self):
        """
        DESCRIPTION: Logout from application/wait for the events to complete
        EXPECTED:
        """
        self.site.logout()

    def test_005_login_in_if_logged_out_previously_or_navigate_to_fanzone_page(self):
        """
        DESCRIPTION: Login in if logged out previously or navigate to Fanzone page
        EXPECTED: User should be navigated to homepage
        """
        self.site.login(username=self.username)
        banner = self.site.home.fanzone_banner()
        banner.let_me_see.click()

    def test_006_verify_if_user_is_able_to_see_premier_league_table_and_icon_in_now_and_next_tab_in_fe(self):
        """
        DESCRIPTION: Verify If user is able to see Premier League table and icon in Now and Next Tab in FE
        EXPECTED: User should be able to see Premier League table link and icon in Now and Next Tab in FE
        """
        self.test_001_verify_if_user_is_able_to_see_premier_league_table_and_icon_in_now_and_next_tab_in_fe()

    def test_007_click_on_the_teams_bets_header_link(self):
        """
        DESCRIPTION: Click on the Teams bets header link
        EXPECTED: User should be able to see the updated league table is opened as overlay with close option(X)
        """
        self.test_002_click_on_the_teams_bets_header_link()

    def test_008_click_on_close_x_option_in_overlay(self):
        """
        DESCRIPTION: Click on Close (X) option in overlay
        EXPECTED: League table overlay should be closed
        """
        self.test_003_click_on_close_x_option_in_overlay()
