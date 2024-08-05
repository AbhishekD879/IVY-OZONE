import pytest
from tests.base_test import vtest
from tests.Common import Common
from time import sleep
from voltron.utils.waiters import wait_for_result
from voltron.environments import constants as vec


@pytest.mark.lad_stg2
@pytest.mark.lad_tst2
# @pytest.mark.lad_prod     # Cannot create events in prod/beta
# @pytest.mark.lad_hl
@pytest.mark.high
@pytest.mark.desktop
@pytest.mark.fanzone
@pytest.mark.other
@vtest
class Test_C65304909_Verify_Now_and_Next_tab_will_not_populate_matches_of_non_subscribed_team_in_Fanzone_page(Common):
    """
    TR_ID: C65304909
    NAME: Verify Now and Next tab will not populate matches of non subscribed team in Fanzone page
    DESCRIPTION: Verify Now and Next tab will not populate matches of non subscribed team in Fanzone page
    PRECONDITIONS: 1)User has access to CMS
    PRECONDITIONS: 2)Fanzone option is enabled in System Configuration and Fanzone entry points in Fanzone section in CMS
    PRECONDITIONS: 3) Events should be configured for all the Fanzones in OB, some of the events should be In-Play
    PRECONDITIONS: 4)User has FE URL and Valid credentials to Login Lads FE and user has successfully logged into application
    PRECONDITIONS: 5) HC should be created in CMS, as per below path
    PRECONDITIONS: CMS-->Sports Pages--> Sport Categories-->Fanzone-->Module-->Highlight Carousel Module
    PRECONDITIONS: 6) Surface Bets are configured in CMS, as per below path
    PRECONDITIONS: CMS-->Sports Pages--> Sport Categories-->Fanzone-->Module-->Highlight Carousel Module
    PRECONDITIONS: 7) Outright Markets data is configured in Open Bet
    """
    keep_browser_open = True
    price_num = 1
    price_den = 2

    def test_000_preconditions(self):
        fanzone_status = self.get_initial_data_system_configuration().get('Fanzone')
        if not fanzone_status.get('enabled'):
            self.cms_config.update_system_configuration_structure(config_item='Fanzone',
                                                                  field_name='enabled',
                                                                  field_value=True)

        burnley_fanzone = self.cms_config.get_fanzone(vec.fanzone.TEAMS_LIST.burnley.title())
        if burnley_fanzone['active'] is not True:
            self.cms_config.update_fanzone(vec.fanzone.TEAMS_LIST.burnley.title(),
                                           typeId=self.football_config.autotest_class.autotest_premier_league.type_id)

        event = self.ob_config.add_autotest_premier_league_football_event()
        self.__class__.selection_id = event.selection_ids[event.team1]
        self.__class__.surface_bet = self.cms_config.add_fanzone_surface_bet(selection_id=self.selection_id,
                                                                             priceNum=self.price_num,
                                                                             priceDen=self.price_den)

        typeId = self.ob_config.football_config.autotest_class.autotest_premier_league.type_id
        self.cms_config.update_fanzone(vec.fanzone.TEAMS_LIST.burnley.title(), str(typeId))
        event = self.ob_config.add_autotest_premier_league_football_outright_event()
        self.__class__.event_name = event.ss_response['event']['name'].upper()
        self.__class__.market_name = event.ss_response['event']['children'][0]['market']['templateMarketName']
        self.__class__.selection_name, selection_id = list(event.selection_ids.items())[0]
        self.ob_config.map_fanzone_event_selection_id(selection_id=selection_id,
                                                      fanzone_team=vec.fanzone.TEAMS_LIST.burnley,
                                                      team_external_id=self.ob_config.football_config.fanzone_external_id.burnley)

        home_team = vec.fanzone.TEAMS_LIST.burnley.title()
        away_team = vec.fanzone.TEAMS_LIST.brentford.title()
        self.ob_config.create_fanzone_league_event_id(
            league_id=self.ob_config.football_config.autotest_class.autotest_premier_league.type_id,
            home_team=home_team,
            away_team=away_team,
            home_team_external_id=self.ob_config.football_config.fanzone_external_id.burnley,
            away_team_external_id=self.ob_config.football_config.fanzone_external_id.brentford)

        username = self.gvc_wallet_user_client.register_new_user().username
        self.site.wait_content_state('Homepage')
        sleep(3)
        self.site.login(username=username)
        self.site.open_sport(name='FOOTBALL', fanzone=True)
        self.site.wait_content_state("football")
        dialog_fb = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_SHOW_US_YOUR_COLORS, timeout=30)
        dialog_fb.imin_button.click()
        wait_for_result(lambda: self.site.show_your_colors.items_as_ordered_dict,
                        name='OK button is displayed',
                        timeout=5)
        teams = self.site.show_your_colors.items_as_ordered_dict
        teams[vec.fanzone.TEAMS_LIST.burnley.title()].click()
        dialog_confirm = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_TEAM_CONFIRMATION)
        dialog_confirm.confirm_button.click()
        sleep(3)
        dialog_alert = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_TEAM_ALERTS)
        dialog_alert.exit_button.click()

    def test_001_navigate_to_fanzone_page_any_of_the_below_listed_entry_pointsa_fanzone_in_sports_ribbononly_mobileb_fanzone_in_a_zall_sportsc_launch_banner_in_home_paged_launch_banner_in_football_landing_page(self):
        """
        DESCRIPTION: Navigate to Fanzone page any of the below listed entry points
        DESCRIPTION: a. Fanzone in Sports Ribbon(only mobile)
        DESC/.RIPTION: b. Fanzone in A-Z/All sports
        DESCRIPTION: c. Launch Banner in Home page
        DESCRIPTION: d. Launch banner in Football landing page
        EXPECTED: User should be navigated to Fanzone page
        """
        banner = self.site.home.fanzone_banner()
        banner.let_me_see.click()
        self.site.wait_content_state_changed(timeout=10)
        wait_for_result(lambda: self.site.fanzone.tabs_menu.current,
                        name='Fanzone page not displayed',
                        timeout=5)

    def test_002_verify_user_is_able_to_see_events_in_now_and_next_tab(self):
        """
        DESCRIPTION: Verify user is able to see Events in Now and Next tab
        EXPECTED: User should be able to see Events section in Now and Next tab
        """
        current_tab = self.site.fanzone.tabs_menu.current
        self.assertEqual(current_tab, vec.fanzone.NOW_AND_NEXT,
                         msg=f'Actual Tab "{current_tab}", is not same '
                             f' expected tab "{vec.fanzone.NOW_AND_NEXT}"')

    def test_003_verify_surface_betshc_and_outright_data_populated_belongs_to_subscribed_teamfanzone(self):
        """
        DESCRIPTION: Verify Surface Bets,HC and Outright data populated belongs to subscribed team/Fanzone
        EXPECTED: User should see Surface Bets,HC and Outright of his subscribed team alone, other Fanzone team data should not be populated.
        """
        sleep(3)
        self.device.refresh_page()
        self.assertTrue(self.site.fanzone.tab_content.has_surface_bets(),
                        msg=f'Surface Bets are not shown on Fanzone page')
        surface_bet_name = self.surface_bet['title'].upper()
        surface_bets = self.site.fanzone.tab_content.surface_bets.items_as_ordered_dict
        self.assertIn(surface_bet_name, surface_bets,
                      msg=f'Created surface bet "{surface_bet_name}" is not present in "{surface_bets}"')
        outright = self.site.fanzone.tab_content.accordions_list.items_as_ordered_dict.get(self.event_name)
        market = outright.accordions_list.items_as_ordered_dict.get(self.market_name)
        events = market.items_as_ordered_dict
        self.assertIn(self.selection_name, list(events),
                      msg=f'Expected event "{self.selection_name}" is not found in actual events "{list(events)}"')
