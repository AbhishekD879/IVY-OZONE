import datetime
import pytest
import tests
from collections import OrderedDict
from time import sleep
from crlat_ob_client.create_event import CreateSportEvent
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.environments import constants as vec
from tests.base_test import vtest
from voltron.utils.helpers import generate_name
from voltron.utils.waiters import wait_for_result


@pytest.mark.lad_stg2
@pytest.mark.lad_tst2 # Not configured in tst2
# @pytest.mark.lad_prod # we cannot create events in prod
@pytest.mark.high
@pytest.mark.desktop
@pytest.mark.fanzone
@pytest.mark.other
@vtest
class Test_C65305131_To_place_bets_on_different_type_of_Outright_markets(BaseBetSlipTest):
    """
    TR_ID: C65305131
    NAME: To place bets on different type of Outright markets
    DESCRIPTION: To place bets on different type of Outright markets
    PRECONDITIONS: 1)User has access to CMS
    PRECONDITIONS: 2)Fanzone option is enabled in Structure and Fanzone entry points in Fanzone section in CMS
    PRECONDITIONS: 3) Various Outrigh markets are created in OB for that type or competition
    PRECONDITIONS: 4)User has FE url and Valid credentials to Login Lads FE
    """
    keep_browser_open = True
    price = OrderedDict([('odds_home', '1/2'), ('odds_away', '4/1')])
    now = datetime.datetime.now()
    expiry_year = str(now.year)
    expiry_month = f'{now.month:02d}'

    def test_000_preconditions(self):
        """
        PRECONDITIONS: 1)User has access to CMS
        PRECONDITIONS: 2)Fanzone option is enabled in Structure and Fanzone entry points in Fanzone section in CMS
        PRECONDITIONS: 3) Various Outrigh markets are created in OB for that type or competition
        PRECONDITIONS: 4)User has FE url and Valid credentials to Login Lads FE
        """
        fanzone_status = self.get_initial_data_system_configuration().get('Fanzone')
        if not fanzone_status.get('enabled'):
            self.cms_config.update_system_configuration_structure(config_item='Fanzone',
                                                                  field_name='enabled',
                                                                  field_value=True)
        self.cms_config.update_fanzone(vec.fanzone.TEAMS_LIST.burnley.title(),
                                       typeId=str(self.ob_config.football_config.autotest_class.autotest_premier_league.type_id))
        typeId = self.ob_config.football_config.autotest_class.autotest_premier_league.type_id
        class_id = self.ob_config.football_config.autotest_class.class_id
        market_template_id = self.ob_config.football_config.autotest_class.autotest_premier_league.outright_market_template_id
        self.cms_config.update_fanzone(vec.fanzone.TEAMS_LIST.burnley.title(), str(typeId))
        self.__class__.event = self.ob_config.add_autotest_premier_league_football_outright_event()
        event = CreateSportEvent(env=tests.settings.backend_env, brand=self.brand,
                                 category_id=self.ob_config.football_config.category_id,
                                 class_id=class_id, type_id=typeId)
        market_id = event.create_market(market_name = "|Relegation|", market_template_id=market_template_id,
                            class_id =class_id, event_id = self.event.event_id, bet_in_run='Y')
        selections_number = 2
        selection_types = ['A'] * selections_number  # actually, selection_types is not needed at all, but otherwise add_selections will fail
        selection_names = ['|Auto test %s|' % generate_name() for _ in range(0, selections_number)]
        prices = ['%s/%s' % (i + 1, i + 2) for i in range(0, 2)]
        selection = event.add_selections(prices=prices,
                                               marketID=market_id,
                                               selection_names=selection_names,
                                               selection_types=selection_types)
        self.__class__.event_name = self.event.ss_response['event']['name'].upper()
        self.__class__.market_name = self.event.ss_response['event']['children'][0]['market']['templateMarketName']
        selection_name, selection_id = list(self.event.selection_ids.items())[0]
        self.ob_config.map_fanzone_event_selection_id(selection_id=selection_id,
                                                      fanzone_team=vec.fanzone.TEAMS_LIST.burnley,
                                                      team_external_id=self.ob_config.football_config.fanzone_external_id.burnley)
        selection_2 = list(selection.values())[0]
        self.ob_config.map_fanzone_event_selection_id(selection_id=selection_2,
                                                      fanzone_team=vec.fanzone.TEAMS_LIST.burnley,
                                                      team_external_id=self.ob_config.football_config.fanzone_external_id.burnley)
        username = self.gvc_wallet_user_client.register_new_user().username
        self.gvc_wallet_user_client.add_new_payment_card_and_deposit(username=username,
                                                                     amount=str(tests.settings.min_deposit_amount),
                                                                     card_number=tests.settings.visa_card,
                                                                     card_type='visa',
                                                                     expiry_month=self.expiry_month,
                                                                     expiry_year=self.expiry_year,
                                                                     cvv=tests.settings.master_card_cvv)
        self.site.login(username=username)
        self.site.open_sport('football', fanzone=True)
        self.site.wait_content_state("football")
        dialog_fb = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_SHOW_US_YOUR_COLORS,
                                              timeout=30)
        dialog_fb.imin_button.click()
        wait_for_result(lambda: self.site.show_your_colors.items_as_ordered_dict,
                        name='All Teams to be displayed',
                        timeout=5)
        team = self.site.show_your_colors.items_as_ordered_dict.get(vec.fanzone.TEAMS_LIST.burnley.title())
        team.click()
        dialog_confirm = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_TEAM_CONFIRMATION)
        dialog_confirm.confirm_button.click()
        sleep(5)
        dialog_alert = self.site.wait_for_dialog(dialog_name=vec.dialogs.DIALOG_MANAGER_TEAM_ALERTS)
        dialog_alert.exit_button.click()

    def test_001_hit_the_fe_url_and_login_to_lads_fe(self):
        """
        DESCRIPTION: Hit the FE url and login to Lads FE
        EXPECTED: User should be able to access the url and is logged into Lads application
        """
        #Covered in above step

    def test_002_now_navigate_homepage_football_slpa_z_menusports_ribbon(self):
        """
        DESCRIPTION: Now navigate Homepage /Football slp/A-Z menu/Sports ribbon
        EXPECTED: User should be navigated to Homepage /Football slp/A-Z menu/Sports ribbon
        """
        self.assertTrue(self.site.home.fanzone_banner(), msg="Fanzone banner is not displayed")

    def test_003_click_on_fanzone_labelfanzone_launch_banner(self):
        """
        DESCRIPTION: Click on Fanzone label/Fanzone launch banner
        EXPECTED: User should be on Fanzone page
        """
        fanzone_banner = self.site.home.fanzone_banner()
        fanzone_banner.let_me_see.click()
        wait_for_result(lambda: self.site.fanzone.tabs_menu, timeout=5,
                        name='"Fanzone tab menus" to be displayed.')
        current_tab = self.site.fanzone.tabs_menu.current
        self.assertEqual(current_tab, vec.fanzone.NOW_AND_NEXT,
                         msg=f'Actual Tab "{current_tab}", is not same '
                             f' expected tab "{vec.fanzone.NOW_AND_NEXT}"')

    def test_004_place_bet_on_different_markets_like_outright_top4_top6_top_goal_scorer_relegation_each_way_etc(self):
        """
        DESCRIPTION: Place bet on different markets like Outright, Top4, Top6, Top Goal scorer, Relegation, Each way etc.
        EXPECTED: Should be able to place bet on all various markets listed
        """
        self.site.fanzone.tabs_menu.click_button(button_name=vec.fanzone.NOW_AND_NEXT)
        outrights = self.site.fanzone.tab_content.accordions_list.items_as_ordered_dict.get(self.event_name)
        markets = list(outrights.accordions_list.items_as_ordered_dict.values())
        count = 0
        for market in markets:
            events = market.items_as_ordered_dict
            bet_button = list(events.values())[0].bet_button
            bet_button.click()
            sleep(1)
            if self.device_type == 'mobile' and count == 0:
                self.site.add_first_selection_from_quick_bet_to_betslip()
                sleep(2)
        self.site.open_betslip()
        self.place_single_bet()
