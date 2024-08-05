import pytest
import voltron.environments.constants as vec
from time import sleep
from datetime import datetime
from crlat_cms_client.utils.date_time import get_date_time_as_string
from tests.base_test import vtest
from tests.Common import Common
from voltron.utils.waiters import wait_for_result


@pytest.mark.lad_stg2
@pytest.mark.lad_tst2
# @pytest.mark.lad_prod # Cannot create leagues on prod
# @pytest.mark.lad_hl
@pytest.mark.medium
@pytest.mark.other
@pytest.mark.desktop
@pytest.mark.fanzone
@vtest
class Test_C65305143_Verify_league_table_is_populated_even_if_matches_havent_started(Common):
    """
    TR_ID: C65305143
    NAME: Verify league table is populated even if matches haven't started
    DESCRIPTION: Verify league table is populated even if matches haven't started
    PRECONDITIONS: 1)User has access to CMS and valid credentials to login
    PRECONDITIONS: 2)User has access to FE and valid credentials to login
    PRECONDITIONS: 3)Fanzone option is enabled in Structure and Fanzone entry points in Fanzone section in CMS
    PRECONDITIONS: 4)Premier league table and icon is configured in CMS successfully , League table is mapped to the Team for the competition team is playing for the events which has not started yet
    PRECONDITIONS: 5)User has logged into Lads FE and is on Fanzone page
    """
    keep_browser_open = True

    def test_000_precondition(self):
        """
        DESCRIPTION: Active the fanzone team and register a new user
        EXPECTED: Fanzone team is activated in cms and logged into the application
        """
        fanzone_status = self.get_initial_data_system_configuration().get('Fanzone')
        if not fanzone_status.get('enabled'):
            self.cms_config.update_system_configuration_structure(config_item='Fanzone',
                                                                  field_name='enabled',
                                                                  field_value=True)
        self.__class__.home_team = vec.fanzone.TEAMS_LIST.leeds_united.title()
        self.__class__.away_team = vec.fanzone.TEAMS_LIST.leicester_city.title()
        astonVilla_fanzone = self.cms_config.get_fanzone(self.home_team)
        if astonVilla_fanzone['active'] is not True:
            self.cms_config.update_fanzone(self.home_team,
                                           typeId=self.football_config.autotest_class.autotest_premier_league.type_id)

        now = datetime.now()
        time_format = '%Y-%m-%d %H:%M:%S'
        date_from = get_date_time_as_string(date_time_obj=now, time_format=time_format,
                                            url_encode=False, days=1)
        self.ob_config.create_fanzone_league_event_id(
            league_id=self.ob_config.football_config.autotest_class.autotest_premier_league.type_id,
            home_team=str(self.home_team),
            away_team=str(self.away_team),
            home_team_external_id=self.ob_config.football_config.fanzone_external_id.leeds_united,
            away_team_external_id=self.ob_config.football_config.fanzone_external_id.leicester_city, start_date=str(date_from))

        username = self.gvc_wallet_user_client.register_new_user().username
        self.site.login(username=username)
        self.site.open_sport(name='FOOTBALL', fanzone=True)
        dialog_fb = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_SHOW_US_YOUR_COLORS,
                                              timeout=30)
        dialog_fb.imin_button.click()
        wait_for_result(lambda: self.site.show_your_colors.items_as_ordered_dict,
                        name='SYC is displayed',
                        timeout=5)
        teams = self.site.show_your_colors.items_as_ordered_dict
        teams[self.home_team].scroll_to_we()
        teams[self.home_team].click()
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
        banner = self.site.home.fanzone_banner()
        banner.let_me_see.click()
        tabs_menu = self.site.fanzone.tabs_menu.items_as_ordered_dict
        self.assertIn(vec.fanzone.NOW_AND_NEXT, tabs_menu,
                      msg=f'"{vec.fanzone.NOW_AND_NEXT}" tab is not present in tabs menu')
        self.site.fanzone.tabs_menu.click_button(button_name=vec.fanzone.NOW_AND_NEXT)
        next_games = self.site.fanzone.tab_content.highlight_carousels.get('NEXT GAMES')
        events = next_games.items_as_ordered_dict
        self.assertTrue(events, msg="Events are not found in HC")
        event_name = self.home_team + '\n' + self.away_team if self.device_type == 'mobile' else self.home_team + ' v ' + self.away_team
        self.assertIn(event_name, events,
                      msg='Match betting market is not shown in HC '
                          'even if Fanzone flag is checked in Match betting from OB')
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
        self.assertFalse(self.site.fanzone.premier_leauge.is_league_table_opened(expected_result=False),
                         msg="Premier League Table is displayed after clicking close button")
