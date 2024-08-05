import pytest
from tests.base_test import vtest
from tests.Common import Common
from time import sleep
from voltron.environments import constants as vec
from voltron.utils.waiters import wait_for_result


@pytest.mark.lad_stg2
@pytest.mark.lad_tst2
# @pytest.mark.prod # not configured in prod and Beta
# @pytest.mark.hl # not configured in prod and Beta
@pytest.mark.high
@pytest.mark.other
@pytest.mark.fanzone
@pytest.mark.desktop
@vtest
class Test_C65304890_To_verify_the_order_of_Special_Surface_Bets(Common):
    """
    TR_ID: C65304890
    NAME: To verify the order of Special Surface Bets
    DESCRIPTION: To verify the order of Special Surface Bets
    PRECONDITIONS: 1) Evens should be created and Special Marktes should be configured in Open Bet
    PRECONDITIONS: Event Creation-->Market Creation page--> Flags section-> Enable FANZONE checkbox
    PRECONDITIONS: 2) User should be Logged into applicaion
    PRECONDITIONS: 3) User should be navigated to Fanzone
    PRECONDITIONS: 4) Fanzone should be enabled in CMS-->System Configuration--> Structure-->Fanzone
    PRECONDITIONS: 5) Surface Bets should be configured using selections from Special Markets
    PRECONDITIONS: CMS--> Sports Pages--> Sports Categeories--> Fanzone-->Surface Bets
    PRECONDITIONS: 6) User should be in Fanzone page
    """
    keep_browser_open = True
    price_num = 4
    price_den = 9
    price_num2 = 3
    price_den2 = 4

    def test_000_precondition(self):
        fanzone_status = self.get_initial_data_system_configuration().get('Fanzone')
        if not fanzone_status.get('enabled'):
            self.cms_config.update_system_configuration_structure(config_item='Fanzone',
                                                                  field_name='enabled',
                                                                  field_value=True)
        market_name = vec.siteserve.EXPECTED_MARKETS_NAMES.both_teams_to_score
        minutes = -1
        start_time1 = self.get_date_time_formatted_string(minutes=-minutes)

        event_params = self.ob_config.add_autotest_premier_league_football_event(special=True,
                                                                                 default_market_name=market_name,
                                                                                 start_time=start_time1)
        self.__class__.event_id = event_params.event_id
        actual_market_name, market_id = next(iter(self.ob_config.market_ids.get(self.event_id).items()))

        selection_id = event_params.selection_ids[event_params.team1]
        market_template_id = next(iter(self.ob_config.football_config.autotest_class.
                                       autotest_premier_league.markets.get(actual_market_name).values()))
        self.ob_config.make_market_special(
            market_id=market_id,
            market_template_id=market_template_id,
            event_id=self.event_id,
            flags='FZ')

        self.__class__.surface_bet = self.cms_config.add_fanzone_surface_bet(selection_id=selection_id,
                                                                             priceNum=self.price_num,
                                                                             priceDen=self.price_den)

        # event 2
        minutes = -4
        start_time2 = self.get_date_time_formatted_string(minutes=-minutes)
        market_name = vec.siteserve.EXPECTED_MARKETS_NAMES.both_teams_to_score
        event_params2 = self.ob_config.add_autotest_premier_league_football_event(special=True,
                                                                                  default_market_name=market_name,
                                                                                  start_time=start_time2)
        self.__class__.event_id2 = event_params2.event_id
        actual_market_name, market_id = \
            next(iter(self.ob_config.market_ids.get(self.event_id2).items()))

        selection_id2 = event_params2.selection_ids[event_params2.team1]
        market_template_id = next(iter(self.ob_config.football_config.autotest_class.
                                       autotest_premier_league.markets.get(actual_market_name).values()))
        self.ob_config.make_market_special(
            market_id=market_id,
            market_template_id=market_template_id,
            event_id=self.event_id2,
            flags='FZ')

        self.__class__.surface_bet2 = self.cms_config.add_fanzone_surface_bet(selection_id=selection_id2,
                                                                              priceNum=self.price_num2,
                                                                              priceDen=self.price_den2)
        username = self.gvc_wallet_user_client.register_new_user().username
        self.site.login(username=username)
        self.site.open_sport(name='FOOTBALL', fanzone=True)
        self.site.wait_content_state("football")
        dialog_fb = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_SHOW_US_YOUR_COLORS,
                                              timeout=30)
        dialog_fb.imin_button.click()
        wait_for_result(lambda: self.site.show_your_colors.items_as_ordered_dict,
                        name='I Am In Button is displayed',
                        timeout=5)
        teams = self.site.show_your_colors.items_as_ordered_dict
        list(teams.values())[1].scroll_to_we()
        list(teams.values())[1].click()
        dialog_confirm = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_TEAM_CONFIRMATION)
        dialog_confirm.confirm_button.click()
        sleep(5)
        dialog_alert = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_TEAM_ALERTS)
        dialog_alert.exit_button.click()

    def test_001_verify_special_market_selectionssurface_bets_are_populated_in_fanzone_page(self):
        """
        DESCRIPTION: Verify Special Market selections(Surface Bets) are populated in Fanzone page
        EXPECTED: Special Market selections should be populated in Fanzone page
        """
        banner = self.site.home.fanzone_banner()
        banner.let_me_see.click()
        tabs_menu = self.site.fanzone.tabs_menu.items_as_ordered_dict
        self.assertIn(vec.fanzone.NOW_AND_NEXT, tabs_menu,
                      msg=f'"{vec.fanzone.NOW_AND_NEXT}" tab is not present in tabs menu')
        self.site.fanzone.tabs_menu.click_button(button_name='NOW & NEXT')

        self.assertTrue(self.site.fanzone.tab_content.has_surface_bets(),
                        msg=f'Surface Bets are not shown on Fanzone page')
        self.__class__.surface_bet_name1 = self.surface_bet['title'].upper()
        self.__class__.surface_bet_name2 = self.surface_bet2['title'].upper()

        self.__class__.surface_bets = self.site.fanzone.tab_content.surface_bets.items_as_ordered_dict

        self.assertIn(self.surface_bet_name1, self.surface_bets,
                      msg=f'Created surface bet "{self.surface_bet_name1}" is not present in "{self.surface_bets}"')
        self.assertIn(self.surface_bet_name2, self.surface_bets,
                      msg=f'Created surface bet "{self.surface_bet_name2}" is not present in "{self.surface_bets}"')

    def test_002_verify_order_of_the_surface_bets(self):
        """
        DESCRIPTION: Verify order of the Surface bets
        EXPECTED: Order of the surface bets should be similar to Prodcution Surface Bets i.e., Live Events,Disp Order,Start Time and Name.
        """
        surface_bet_index1 = list(self.surface_bets.keys()).index(self.surface_bet_name1)
        surface_bet_index2 = list(self.surface_bets.keys()).index(self.surface_bet_name2)
        self.assertGreater(surface_bet_index2, surface_bet_index1, msg='surface bets are not displayed in order')
