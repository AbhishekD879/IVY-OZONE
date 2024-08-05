import datetime
import tests
import pytest
from collections import OrderedDict
from time import sleep
from crlat_ob_client.create_event import CreateSportEvent
from crlat_ob_client.utils.helpers import generate_name
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.utils.waiters import wait_for_result
from voltron.environments import constants as vec


@pytest.mark.lad_stg2
# @pytest.mark.lad_tst2      # Not configured in tst2
# @pytest.mark.lad_prod     # we cannot create events in prod
# @pytest.mark.lad_hl
@pytest.mark.medium
@pytest.mark.desktop
@pytest.mark.fanzone
@pytest.mark.other
@vtest
class Test_C65305120_User_should_be_able_to_place_bet_from_bet_slip_for_Outright_market(BaseBetSlipTest):
    """
    TR_ID: C65305120
    NAME: User should be able to place bet from bet slip for Outright market
    DESCRIPTION: To verify user should be able to place bet from bet slip for outright market in Fanzone page
    PRECONDITIONS: 1)User has access to CMS
    PRECONDITIONS: 2)Fanzone option is enabled in Structure and Fanzone entry points in Fanzone section in CMS
    PRECONDITIONS: 3)Outright markets are created with Premier league participating teams as selections for Various type such 442,438 etc.
    PRECONDITIONS: 4)User has FE url and Valid credentials to Login Lads FE
    PRECONDITIONS: 5) User has subscribed to Fanzone
    PRECONDITIONS: 6) User is navigated to Fanzone page
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
                                       typeId=str(
                                           self.ob_config.football_config.autotest_class.autotest_premier_league.type_id))
        typeId = self.ob_config.football_config.autotest_class.autotest_premier_league.type_id
        class_id = self.ob_config.football_config.autotest_class.class_id
        market_template_id = self.ob_config.football_config.autotest_class.autotest_premier_league.outright_market_template_id
        self.__class__.event = self.ob_config.add_autotest_premier_league_football_outright_event()
        event = CreateSportEvent(env=tests.settings.backend_env, brand=self.brand,
                                 category_id=self.ob_config.football_config.category_id,
                                 class_id=class_id, type_id=typeId)
        market_id = event.create_market(market_name="|Relegation|", market_template_id=market_template_id,
                                        class_id=class_id, event_id=self.event.event_id, bet_in_run='Y')
        selections_number = 2
        selection_types = ['A'] * selections_number  # actually, selection_types is not needed at all, but otherwise add_selections will fail
        selection_names = ['|Auto test %s|' % generate_name() for _ in range(0, selections_number)]
        prices = ['%s/%s' % (i + 1, i + 2) for i in range(0, 2)]
        event.add_selections(prices=prices,
                             marketID=market_id,
                             selection_names=selection_names,
                             selection_types=selection_types)
        self.__class__.event_name = self.event.ss_response['event']['name'].upper()
        self.__class__.market_name = self.event.ss_response['event']['children'][0]['market']['templateMarketName']
        self.__class__.selection_name, selection_id = list(self.event.selection_ids.items())[0]
        self.ob_config.map_fanzone_event_selection_id(selection_id=selection_id,
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
        self.site.wait_content_state("Home")
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

    def test_001_verify_if_user_is_able_to_see_outright_market_of_his_subscribed_team_alone_in_now_and_next_tab(self):
        """
        DESCRIPTION: Verify if user is able to see Outright Market of his subscribed team alone in Now and next Tab
        EXPECTED: User should be able to able to see single outright market of his subscribed team with one odd value in &lt;team&gt; Bets section in Now and Next tab
        """
        fanzone_banner = self.site.home.fanzone_banner()
        fanzone_banner.let_me_see.click()
        wait_for_result(lambda: self.site.fanzone.tabs_menu, timeout=5,
                        name='"Fanzone tab menus" to be displayed.')
        current_tab = self.site.fanzone.tabs_menu.current
        self.assertEqual(current_tab, vec.fanzone.NOW_AND_NEXT,
                         msg=f'Actual Tab "{current_tab}", is not same '
                             f' expected tab "{vec.fanzone.NOW_AND_NEXT}"')

        self.site.fanzone.tabs_menu.click_button(button_name=vec.fanzone.NOW_AND_NEXT)
        outrights = self.site.fanzone.tab_content.accordions_list.items_as_ordered_dict.get(self.event_name)
        market = outrights.accordions_list.items_as_ordered_dict.get(self.market_name)
        self.__class__.events = market.items_as_ordered_dict
        self.assertIn(self.selection_name, list(self.events),
                      msg=f'Expected event "{self.selection_name}" is not found in actual events "{list(self.events)}"')

    def test_002_now_click_on_the_odd_selection_and_add_it_to_bet_slip(self):
        """
        DESCRIPTION: Now click on the odd selection and add it to bet slip
        EXPECTED: The selected odd value should be add to bet slip
        """
        list(self.events.values())[0].bet_button.click()
        if self.device_type == 'mobile':
            self.site.add_first_selection_from_quick_bet_to_betslip()
            sleep(2)

    def test_003_click_on_place_bet(self):
        """
        DESCRIPTION: Click on Place bet
        EXPECTED: User should be able to place bet successfully on the outright market
        """
        self.site.open_betslip()
        sleep(5)
        self.place_single_bet()
        self.check_bet_receipt_is_displayed()
        self.site.bet_receipt.footer.done_button.click()

    def test_004_navigate_to_my_bets_section_ad_verify_if_the_place_bet_is_shown_there(self):
        """
        DESCRIPTION: Navigate to MY Bets section ad verify if the place bet is shown there
        EXPECTED: User should be able to see the Outright bet in MY bets section
        """
        self.site.open_my_bets_open_bets()
        bet_name, bet = self.site.open_bets.tab_content.accordions_list.get_bet(
            bet_type='SINGLE', event_names=self.event_name.title())
        self.assertTrue(bet, msg=f'{bet_name} event is not displayed in my bet section')
