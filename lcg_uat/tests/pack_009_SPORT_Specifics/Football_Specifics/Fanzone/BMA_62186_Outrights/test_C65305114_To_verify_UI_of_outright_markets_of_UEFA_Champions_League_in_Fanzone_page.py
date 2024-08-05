import pytest
import tests
from tests.base_test import vtest
from tests.Common import Common
from collections import OrderedDict
from time import sleep
from voltron.environments import constants as vec
from crlat_ob_client.create_event import CreateSportEvent
from voltron.utils.waiters import wait_for_result


@pytest.mark.lad_stg2
@pytest.mark.lad_tst2
# @pytest.mark.lad_prod     # Can't add market in prod/beta
# @pytest.mark.lad_hl
@pytest.mark.high
@pytest.mark.desktop
@pytest.mark.fanzone
@pytest.mark.other
@vtest
class Test_C65305114_To_verify_UI_of_outright_markets_of_UEFA_Champions_League_in_Fanzone_page(Common):
    """
    TR_ID: C65305114
    NAME: To verify UI of outright markets of UEFA Champions League in Fanzone page
    DESCRIPTION: To verify UI of outright markets of UEFA Champions League in Fanzone page
    PRECONDITIONS: 1)User has access to CMS
    PRECONDITIONS: 2)Fanzone option is enabled in Structure and Fanzone entry points in Fanzone section in CMS
    PRECONDITIONS: 3)Outright markets are created with Premier league participating teams as selections for Various type such 442,438 etc.
    PRECONDITIONS: 4)User has FE url and Valid credentials to Login Lads FE
    PRECONDITIONS: 5) User has subscribed to Fanzone
    """
    keep_browser_open = True
    teamname = vec.fanzone.TEAMS_LIST.burnley.title()
    price = OrderedDict([('odds_home', '1/2'), ('odds_away', '4/1')])
    new_market_name = "GROUP1 Winner"
    new_market_name2 = "GROUP2 Winner"

    def test_000_precondition(self):
        """
        PRECONDITIONS: 1)User has access to CMS
        PRECONDITIONS: 2)Fanzone option is enabled in Structure and Fanzone entry points in Fanzone section in CMS
        PRECONDITIONS: 3)Outright markets are created with Premier league participating teams as selections for Various type such 442,438 etc.
        PRECONDITIONS: 4)User has FE url and Valid credentials to Login Lads FE
        PRECONDITIONS: 5) User has subscribed to Fanzone
        PRECONDITIONS: 6) User is navigated to Fanzone page
        """
        fanzone_status = self.get_initial_data_system_configuration().get('Fanzone')
        if not fanzone_status.get('enabled'):
            self.cms_config.update_system_configuration_structure(config_item='Fanzone',
                                                                  field_name='enabled',
                                                                  field_value=True)
            self.cms_config.update_fanzone(vec.fanzone.TEAMS_LIST.burnley.title(),
                                           typeId=self.football_config.autotest_class.autotest_premier_league.type_id)
        typeId = self.ob_config.football_config.autotest_class.autotest_premier_league.type_id
        class_id = self.ob_config.football_config.autotest_class.class_id
        market_template_id = self.ob_config.football_config.autotest_class.autotest_premier_league.outright_market_template_id
        self.cms_config.update_fanzone(vec.fanzone.TEAMS_LIST.burnley.title(), str(typeId))
        self.__class__.event = self.ob_config.add_autotest_premier_league_football_outright_event()
        event = CreateSportEvent(env=tests.settings.backend_env, brand=self.brand,
                                 category_id=self.ob_config.football_config.category_id,
                                 class_id=class_id, type_id=typeId)
        market_id = event.create_market(market_name="|Relegation|", market_template_id=market_template_id,
                                        class_id=class_id, event_id=self.event.event_id, bet_in_run='Y')
        selections_number = 2
        selection_types = ['A'] * selections_number  # actually, selection_types is not needed at all, but otherwise add_selections will fail
        selection_names = [self.new_market_name, self.new_market_name2]
        prices = ['%s/%s' % (i + 1, i + 2) for i in range(0, 2)]
        selection = event.add_selections(prices=prices,
                                         marketID=market_id,
                                         selection_names=selection_names,
                                         selection_types=selection_types)
        self.__class__.event_name = self.event.ss_response['event']['name'].upper()
        self.__class__.market_name = self.event.ss_response['event']['children'][0]['market']['templateMarketName']
        self.__class__.selection_name, selection_id = list(self.event.selection_ids.items())[0]
        self.ob_config.map_fanzone_event_selection_id(selection_id=selection_id,
                                                      fanzone_team=vec.fanzone.TEAMS_LIST.burnley,
                                                      team_external_id=self.ob_config.football_config.fanzone_external_id.burnley)
        self.__class__.selection_name2, selection_2 = list(selection.items())[0]
        self.ob_config.map_fanzone_event_selection_id(selection_id=selection_2,
                                                      fanzone_team=vec.fanzone.TEAMS_LIST.burnley,
                                                      team_external_id=self.ob_config.football_config.fanzone_external_id.burnley)
        event.update_market_settings(market_id=self.event.default_market_id, event_id=self.event.event_id,
                                     market_template_id=market_template_id, market_display_sort_code='--',
                                     new_market_name=self.new_market_name)
        event.update_market_settings(market_id=market_id, event_id=self.event.event_id,
                                     market_template_id=market_template_id, market_display_sort_code='--',
                                     new_market_name=self.new_market_name2)

    def test_001_hit_the_fe_url_and_login_to_lads_fe(self):
        """
        DESCRIPTION: Hit the FE url and login to Lads FE
        EXPECTED: User should be able to access the url and is logged into Lads application
        """
        self.site.wait_content_state('Homepage')
        username = self.gvc_wallet_user_client.register_new_user().username
        self.site.login(username=username)
        sleep(3)

    def test_002_navigate_to_fanzone_page_via_below_entry_pointsa_launch_banner_in_home_pageb_fanzone_in_sports_ribbonc_fanzone_in_a_zall_sports_menud_launch_banner_in_football_landing_page(self):
        """
        DESCRIPTION: Navigate to Fanzone page via below entry points
        DESCRIPTION: a. Launch Banner in home page
        DESCRIPTION: b. Fanzone in Sports Ribbon
        DESCRIPTION: c. Fanzone in A-Z(All sports) menu
        DESCRIPTION: d. Launch Banner in Football landing page
        EXPECTED: User should be able to navigate Fanzone page
        """
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

    def test_003_verify_is_user_is_able_to_see_uefa_champions_league_outright_market_in_now_and_next_tab(self):
        """
        DESCRIPTION: Verify is user is able to see UEFA Champions League Outright Market in Now and next Tab
        EXPECTED: Verify is user is able to see UEFA Champions League Outright Market in Now and next Tab
        """
        banner = self.site.home.fanzone_banner()
        banner.let_me_see.click()
        current_tab = self.site.fanzone.tabs_menu.current
        self.assertEqual(current_tab, vec.fanzone.NOW_AND_NEXT,
                         msg=f'Actual Tab "{current_tab}", is not same '
                             f' expected tab "{vec.fanzone.NOW_AND_NEXT}"')

    def test_004_verify_ui_of_uefa_champions_league_outright_markets(self):
        """
        DESCRIPTION: Verify UI of UEFA Champions League outright markets
        EXPECTED: Outright UI should be similar to sample provided in Jira BMA-62186 or Zeplin attached to the story
        """
        outrights = self.site.fanzone.tab_content.accordions_list.items_as_ordered_dict.get(self.event_name)
        self.__class__.markets_list = outrights.accordions_list.items_as_ordered_dict
        self.assertIn(self.new_market_name, self.markets_list,
                      msg=f'Market "{self.new_market_name}" is not in the market list "{self.markets_list}"')
        self.assertIn(self.new_market_name2, self.markets_list,
                      msg=f'Market "{self.new_market_name2}" is not in the market list "{self.markets_list}"')

    def test_005_verify_content_for_outrights_markets_in_below_listed_orderltteamgt_bets__configurable_on_cmschampions_league_20222023to_win_marketgroup1_winnerselectionsgroup2_winnerselections_etc(self):
        """
        DESCRIPTION: Verify content for Outrights Markets in below listed order
        DESCRIPTION: &lt;Team&gt; Bets--Configurable on CMS
        DESCRIPTION: Champions League 2022/2023
        DESCRIPTION: To Win (market)
        DESCRIPTION: GROUP1 Winner
        DESCRIPTION: Selections
        DESCRIPTION: GROUP2 Winner
        DESCRIPTION: Selections etc.
        EXPECTED: Outright market content should be as per the order mentioned
        """
        market1 = list(self.markets_list.values())[0]
        market2 = list(self.markets_list.values())[1]
        selection1 = list(market1.items_as_ordered_dict.keys())[0]
        selection2 = list(market2.items_as_ordered_dict.keys())[0]
        self.assertEqual(selection1, self.selection_name,
                         msg=f'Actual selection "{selection1}" is not same as expected selection "{self.selection_name}"')
        self.assertEqual(selection2, self.selection_name2,
                         msg=f'Actual selection "{selection2}" is not same as expected selection "{self.selection_name2}"')
