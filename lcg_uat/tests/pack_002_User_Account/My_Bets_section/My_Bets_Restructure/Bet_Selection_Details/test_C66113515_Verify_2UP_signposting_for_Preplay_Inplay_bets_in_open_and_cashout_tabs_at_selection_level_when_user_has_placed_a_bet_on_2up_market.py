import pytest
import voltron.environments.constants as vec
from crlat_siteserve_client.constants import LEVELS, ATTRIBUTES, OPERATORS
from crlat_siteserve_client.siteserve_client import simple_filter
from datetime import datetime
import tests
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.utils.exceptions.siteserve_exception import SiteServeException


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.bet_history_open_bets
@pytest.mark.bet_selection_details
@pytest.mark.insprint_auto
@pytest.mark.desktop
@vtest
class Test_C66113515_Verify_2UP_signposting_for_Preplay_Inplay_bets_in_open_and_cashout_tabs_at_selection_level_when_user_has_placed_a_bet_on_2up_market(BaseBetSlipTest):
    """
    TR_ID: C66113515
    NAME: Verify 2UP signposting for Preplay/Inplay bets in open and cashout tabs at selection level when user has placed a bet on 2up market
    DESCRIPTION: This testcase verifies 2UP signposting for Preplay/Inplay bets in open and cashout tabs at selection level when user has placed a bet on 2up market
    PRECONDITIONS: Bets which are placed on 2UP market should be avilable in Open, Cashout,Settled tab
    """
    keep_browser_open = True
    bet_amount = 0.05
    markets_params = [('2up_market', {})]

    def is_expected_market(self, event, market_name):
        if event.get('event') and event['event'].get('children'):
            markets = event['event']['children']
            for market in markets:
                if market['market']['templateMarketName'].replace('|', '') == market_name:
                    return True
        return False

    def get_active_events_for_market(self, events, market_name=None):
        return [event for event in events if self.is_expected_market(event, market_name)]

    def test_000_preconditions(self):
        """
        Description: Getting 2UP market events
        """
        self.__class__.num_of_selections = 1
        if tests.settings.backend_env == 'prod':
            expected_template_market = '2Up&Win Early Payout' if self.brand != 'bma' else '2Up - Instant Win'
            cashout_filter = simple_filter(LEVELS.EVENT, ATTRIBUTES.CASHOUT_AVAIL, OPERATORS.EQUALS,
                                           'Y'), simple_filter(LEVELS.MARKET, ATTRIBUTES.CASHOUT_AVAIL,
                                                               OPERATORS.EQUALS, 'Y')
            events = self.get_active_events_for_category(category_id=self.ob_config.football_config.category_id,
                                                         all_available_events=True,additional_filters=cashout_filter)

            filtered_events = self.get_active_events_for_market(events=events,
                                                                market_name=expected_template_market)

            if not filtered_events:
                raise SiteServeException(f'there is no active events for {expected_template_market}')
            else:
                events = filtered_events
            match_result_market = next((market['market'] for market in events[0]['event']['children'] if
                                        market.get('market').get('templateMarketName') == expected_template_market), None)
            self.__class__.event_name = {events[0]['event']['name']: events[0]}
            # ******** Getting Selection IDs ********
            outcomes = match_result_market['children']
            all_selection_ids = {i['outcome']['name']: i['outcome']['id'] for i in outcomes}
            self.__class__.selection_id = list(all_selection_ids.values())[0]

        else:
            event1 = self.ob_config.add_autotest_premier_league_football_event(markets=self.markets_params)
            event2 = self.ob_config.add_autotest_premier_league_football_event(markets=self.markets_params)
            # getting type id
            self.__class__.type_id = event1[7]['event']['typeId']
            # getting type name
            self.__class__.expected_type_name = event1[7]['event']['typeName']
            # getting event name for type id
            self.__class__.event_names_for_type_id = list()
            self.event_names_for_type_id.append(event1[7]['event']['name'])
            self.event_names_for_type_id.append(event2[7]['event']['name'])
            # getting events for type id
            self.__class__.events_for_type_id = {event1[7]['event']['name']: event1[7],
                                                 event2[7]['event']['name']: event2[7]}
            limit = len(self.events_for_type_id) if len(self.events_for_type_id) < 2 else 2

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load oxygen application
        EXPECTED: Homepage is opened
        """
        self.site.login()

    def test_002_login_to_the_application_with_valid_credentials_with_precondition1(self):
        """
        DESCRIPTION: Login to the application with valid credentials with precondition1
        EXPECTED: User is logged in
        """
        # Covered in above step

    def test_003_tap_on_my_bets_item_on_top_menu(self):
        """
        DESCRIPTION: Tap on 'My bets' item on top menu
        EXPECTED: My bets page/Betslip widget is opened.By default user will be on open tab
        """
        self.open_betslip_with_selections(selection_ids=self.selection_id)
        self.place_and_validate_single_bet()
        self.check_bet_receipt_is_displayed()

    def test_004_verify_bets_which_are_placed_on_2_up_market_selections_in_open_tab(self):
        """
        DESCRIPTION: Verify Bets which are placed on 2 UP market selections in open tab
        EXPECTED: 2 UP signposting should be displayed
        """
        self.site.open_my_bets_open_bets()
        bet_name, bet = self.site.open_bets.tab_content.accordions_list.get_bet(
            bet_type=vec.bet_history.MY_BETS_SINGLE_STAKE_TITLE, event_names=self.event_name, number_of_bets=1)
        self.assertTrue(bet.has_bet_promotion(), msg=" '2UP&WIN' signposting is not displayed in MY Bets >> Open tab >> Sports Tab")
        bet_promotion_text = bet.bet_promotion_icon_text
        self.assertEqual(bet_promotion_text.upper(),'2UP&WIN', msg=f'2UP&WIN signposting text is not displayed in MY Bets >> Open tab >> Sports Tab')

    def test_005_verify_the_2up_signposting(self):
        """
        DESCRIPTION: Verify the 2UP signposting
        EXPECTED: It should be displayed with 100% opacity. It should as per figma provided
        EXPECTED: ![](index.php?/attachments/get/9349965e-445e-4e47-bb38-8ec13a46edf0)
        """
        # covered in above step

    def test_006_repeat_step_4_and_5_for_inplay_events(self):
        """
        DESCRIPTION: Repeat step 4 and 5 for inplay events
        EXPECTED: 2UP signposting should be displayed with 100% opacity. It should as per figma provided
        """
        # covered in preplay event only

    def test_007_repeat_step_4_6_in_cash_out_tab(self):
        """
        DESCRIPTION: Repeat step 4-6 in Cash out tab
        EXPECTED: 2UP signposting should be displayed with 100% opacity. It should as per figma provided
        """
        # Verify '2UP&WIN' Signposting in cashout tab
        self.site.open_my_bets_cashout()
        cashout_bet_name, cashout_bet = self.site.cashout.tab_content.accordions_list.get_bet(
            bet_type=vec.bet_history.MY_BETS_SINGLE_STAKE_TITLE, event_names=self.event_name,
            number_of_bets=1)

        # Verifying 2UP&WIN Signposting
        self.assertTrue(cashout_bet.has_bet_promotion(),
                        msg="'2UP&WIN' signposting is not displayed in MY Bets >> Cashout Tab")
        cashout_bet_promotion_text = cashout_bet.bet_promotion_icon_text
        self.assertEqual(cashout_bet_promotion_text.upper(), '2UP&WIN',
                         msg=f'2UP&WIN signposting text is not displayed in MY Bets >> Cashout Tab ')

        # Cashout 2up market selection

        cashout_bet.buttons_panel.full_cashout_button.click()
        cashout_amount = float(cashout_bet.buttons_panel.full_cashout_button.amount.value)
        confirmation_text = cashout_bet.buttons_panel.cashout_button.name
        expected_confirmation = vec.bet_history.CASHOUT_BET.confirm_cash_out + f' £{cashout_amount:.2f}'
        self.assertEqual(expected_confirmation, confirmation_text,
                         msg=f'Expected confirmation text: "{expected_confirmation}" '
                             f'is not equal to actual: "{confirmation_text}"')

        self.assertTrue(cashout_bet.buttons_panel.has_full_cashout_button(timeout=8),
                        msg=f'CASHOUT button was not found on bet: "{cashout_bet_name}" section')

        cashout_bet.buttons_panel.full_cashout_button.click()
        cashout_bet.buttons_panel.cashout_button.click()

        # Verifying '2up&win' signposting in settled tab
        self.site.open_my_bets_settled_bets()
        settled_tab_bet = next(
            iter(list(self.site.settled_bets.tab_content.accordions_list.n_items_as_ordered_dict(no_of_items=1).values())),
            None)
        self.assertIsNotNone(settled_tab_bet, msg='Bet is not available under Open tab')
        bet_name, bet = self.site.settled_bets.tab_content.accordions_list.get_bet(
            bet_type=vec.bet_history.MY_BETS_SINGLE_STAKE_TITLE, event_names=self.event_name,
            number_of_bets=1)
        self.assertTrue(bet.has_bet_promotion(), msg="'2UP&WIN' signposting is not displayed in MY Bets >> Settled Tab")
        bet_promotion_text = bet.bet_promotion_icon_text
        self.assertEqual(bet_promotion_text.upper(), '2UP&WIN',
                         msg=f'2UP&WIN signposting text is not displayed in MY Bets >> Settled Tab ')

