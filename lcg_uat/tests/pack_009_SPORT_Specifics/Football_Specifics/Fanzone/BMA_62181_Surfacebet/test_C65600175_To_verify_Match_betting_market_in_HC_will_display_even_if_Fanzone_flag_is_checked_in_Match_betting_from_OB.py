import pytest
from tenacity import retry, stop_after_attempt, retry_if_exception_type, wait_fixed
from tests.base_test import vtest
from voltron.utils.exceptions.voltron_exception import VoltronException
from voltron.utils.waiters import wait_for_result
from voltron.environments import constants as vec
from time import sleep
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest


@pytest.mark.lad_stg2
@pytest.mark.lad_tst2
@pytest.mark.desktop
@pytest.mark.fanzone
@pytest.mark.medium
@pytest.mark.other
@vtest
class Test_C65600175_To_verify_Match_betting_market_in_HC_will_display_even_if_Fanzone_flag_is_checked_in_Match_betting_from_OB(BaseBetSlipTest):
    """
    TR_ID: C65600175
    NAME: To verify Match betting market in HC will display, even if Fanzone flag is checked in Match betting from OB
    DESCRIPTION: To verify Match betting market in HC will display, even if Fanzone flag is checked in Match betting from OB
    """
    keep_browser_open = True
    team1 = vec.fanzone.TEAMS_LIST.manchester_city
    team2 = vec.fanzone.TEAMS_LIST.manchester_united

    def test_000_precondition(self):
        """
        PRECONDITIONS: 1)User has access to CMS
        PRECONDITIONS: 2)Fanzone option is enabled in Structure and Fanzone entry points in Fanzone section in CMS
        PRECONDITIONS: 3)Fanzone should be checked to match betting market.
        PRECONDITIONS: 4)highlight carousel are created.
        PRECONDITIONS: 5)User has logged into application and navigated to Fanzone page
        """
        fanzone_status = self.get_initial_data_system_configuration().get('Fanzone')
        if not fanzone_status.get('enabled'):
            self.cms_config.update_system_configuration_structure(config_item='Fanzone',
                                                                  field_name='enabled',
                                                                  field_value=True)

        market_name = vec.siteserve.EXPECTED_MARKETS_NAMES.match_result
        self.ob_config.add_autotest_premier_league_football_event(team1=self.team1,
                                                                  team2=self.team2,
                                                                  default_market_name=market_name,
                                                                  flags='FZ')
        self.ob_config.create_fanzone_league_event_id(
            league_id=self.ob_config.football_config.autotest_class.autotest_premier_league.type_id,
            home_team=self.team1,
            away_team=self.team2,
            home_team_external_id=self.ob_config.football_config.fanzone_external_id.manchester_city,
            away_team_external_id=self.ob_config.football_config.fanzone_external_id.manchester_united)

        username = self.gvc_wallet_user_client.register_new_user().username
        self.site.login(username)
        self.site.open_sport('football', fanzone=True)
        dialog_fb = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_SHOW_US_YOUR_COLORS)
        dialog_fb.imin_button.click()
        wait_for_result(lambda: self.site.show_your_colors.items_as_ordered_dict,
                        name='I Am In Button is displayed',
                        timeout=5)
        teams = self.site.show_your_colors.items_as_ordered_dict
        team = teams.get(self.team1.title())
        team.click()
        sleep(3)
        dialog_confirm = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_TEAM_CONFIRMATION)
        dialog_confirm.confirm_button.click()
        sleep(2)
        dialog_alert = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_TEAM_ALERTS)
        dialog_alert.exit_button.click()

    def test_001_verify_user_is_able_to_see_now_and_next_tab_in_fanzone_page(self):
        """
        DESCRIPTION: Verify user is able to see Now and Next tab in Fanzone page
        EXPECTED: User should be able to see Now and Next Tab in Fanzone page
        """
        banner = self.site.home.fanzone_banner()
        banner.let_me_see.click()
        tabs_menu = self.site.fanzone.tabs_menu.items_as_ordered_dict
        self.assertIn(vec.fanzone.NOW_AND_NEXT, tabs_menu,
                      msg=f'"{vec.fanzone.NOW_AND_NEXT}" tab is not present in tabs menu')
        self.site.fanzone.tabs_menu.click_button(button_name=vec.fanzone.NOW_AND_NEXT)

    @retry(stop=stop_after_attempt(3), retry=retry_if_exception_type((VoltronException)),
           wait=wait_fixed(wait=15),
           reraise=True)
    def test_002_verify_Match_betting_market_in_HC_will_display_even_if_Fanzone_flag_is_checked_in_Match_betting_from_OB(self):
        """
        DESCRIPTION: verify Match betting market in HC will display, even if Fanzone flag is checked in Match betting from OB
        EXPECTED: User should see Match betting market in HC, even if Fanzone flag is checked in Match betting from OB
        """
        self.device.refresh_page()
        self.site.wait_splash_to_hide()
        next_games = self.site.fanzone.tab_content.highlight_carousels.get('NEXT GAMES')
        events = next_games.items_as_ordered_dict
        self.assertTrue(events, msg="Events are not found in HC")
        event_name = self.team1+'\n'+self.team2 if self.device_type == 'mobile' else self.team1 + ' v ' + self.team2
        self.assertIn(event_name, events,
                      msg='Match betting market is not shown in HC '
                          'even if Fanzone flag is checked in Match betting from OB')
