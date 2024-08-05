import pytest
from crlat_siteserve_client.constants import LEVELS, ATTRIBUTES, OPERATORS
from crlat_siteserve_client.siteserve_client import simple_filter
from tests.base_test import vtest
from tests.pack_003_Betslip.BaseBetSlipTest import BaseBetSlipTest
from voltron.environments import constants as vec


@pytest.mark.tst2
@pytest.mark.stg2
@pytest.mark.prod
@pytest.mark.desktop
# @pytest.mark.hl
@pytest.mark.medium
@pytest.mark.bet_history_open_bets
@pytest.mark.bet_selection_details
@vtest
@pytest.mark.timeout(1000)
# This test covering C66111709 test
class Test_C66111707_Verify_Location_of_odds_showing_at_selection_level_for_single_bets_in_My_Bets(BaseBetSlipTest):
    """
    TR_ID: C66111707
    NAME: Verify Location of odds showing at selection level for single bets in My Bets
    DESCRIPTION: This testcase verifies the location of odds showing at selection level for single bets in My Bets
    PRECONDITIONS: Sports,Lottos,Pools bets should be available in Open ,cash out settled tab
    """
    keep_browser_open = True

    def verify_my_bets_odds_location(self, bets=[], tab_name=None):
        expected_odds_location = 'end'
        for i in range(len(bets)):
            actual_odds_location = bets[i].odds.css_property_value('text-align')
            self.assertEqual(expected_odds_location, actual_odds_location,
                             msg=f'Expected My bets >> {tab_name} odds location is {expected_odds_location} but '
                                 f'Actul odds location '
                                 f'is {actual_odds_location}')

    def test_000_preconditions(self):
        """
        Get selections to place single and multiple bets
        """
        self.__class__.number_of_events = 3
        self.__class__.selection_ids = []
        self.__class__.tier2_selection_ids = []

        cashout_filter = simple_filter(LEVELS.EVENT, ATTRIBUTES.CASHOUT_AVAIL, OPERATORS.EQUALS,
                                       'Y'), simple_filter(
            LEVELS.MARKET, ATTRIBUTES.CASHOUT_AVAIL, OPERATORS.EQUALS, 'Y')
        hr_events = self.get_active_events_for_category(category_id=self.ob_config.horseracing_config.category_id,
                                                        additional_filters=cashout_filter,
                                                        number_of_events=self.number_of_events)
        for hr_event in hr_events:
            market = next((market['market'] for market in hr_event['event']['children'] if
                           market.get('market').get('templateMarketName') == 'Win or Each Way'), None)
            outcomes = market['children']
            hr_all_selection_ids = {i['outcome']['name']: i['outcome']['id'] for i in outcomes}
            hr_selection_id = list(hr_all_selection_ids.values())[0]
            self.selection_ids.append(hr_selection_id)

        tt_events = self.get_active_events_for_category(category_id=59,
                                                        additional_filters=cashout_filter,
                                                        number_of_events=self.number_of_events)
        for tt_event in tt_events:
            match_result_market = next((market['market'] for market in tt_event['event']['children'] if
                                        market.get('market').get('templateMarketName') == 'Match Betting'), None)
            outcomes = match_result_market['children']
            tt_all_selection_ids = {i['outcome']['name']: i['outcome']['id'] for i in outcomes}
            tt_selection_id = list(tt_all_selection_ids.values())[0]
            self.tier2_selection_ids.append(tt_selection_id)

    def test_001_load_oxygen_application(self):
        """
        DESCRIPTION: Load oxygen application
        EXPECTED: Homepage is opened
        """
        self.site.login()

    def test_002_login_to_the_application_with_valid_credentials(self):
        """
        DESCRIPTION: Login to the application with valid credentials
        EXPECTED: User is logged in
        """
        self.open_betslip_with_selections(selection_ids=self.selection_ids[0])
        self.place_single_bet()
        self.check_bet_receipt_is_displayed()

    def test_003_tap_on_my_bets_item_on_top_menu(self):
        """
        DESCRIPTION: Tap on 'My bets' item on top menu
        EXPECTED: My bets page/Betslip widget is opened.By default user will be on open tab
        """
        pass

    def test_004_verify_location_of_odds_displayed_for_the_single_bets_in_open_tab(self):
        """
        DESCRIPTION: Verify location of Odds displayed for the single bets in Open tab
        EXPECTED: Location of the Odds at selection level to be placed on the right hand side.
        EXPECTED: Should be displayed as per figma
        EXPECTED: ![](index.php?/attachments/get/674853b3-1fd0-45ed-a847-188501120939)
        """
        self.site.open_my_bets_open_bets()
        open_tab_bet = [
            list(self.site.open_bets.tab_content.accordions_list.n_items_as_ordered_dict(no_of_items=1).values())[0]]
        self.verify_my_bets_odds_location(bets=list(open_tab_bet), tab_name='Open tab')

    def test_005_verify_location_of_odds_displayed_for_the_single_bets_in_cash_out_tab(self):
        """
        DESCRIPTION: Verify location of Odds displayed for the single bets in Cash out tab
        EXPECTED: Location of the Odds at selection level to be placed on the right hand side.
        EXPECTED: Should be displayed as per figma
        """
        self.site.open_my_bets_cashout()
        bet = list(self.site.cashout.tab_content.accordions_list.n_items_as_ordered_dict(no_of_items=1).values())[0]
        cash_out_bet = [list(bet.items_as_ordered_dict.values())[0]]
        # cash_out_bet = [
        #     list(self.site.cashout.tab_content.accordions_list.n_items_as_ordered_dict(no_of_items=1).values())[0]]
        self.verify_my_bets_odds_location(bets=list(cash_out_bet), tab_name='Cash Out tab')

        bet.buttons_panel.full_cashout_button.click()
        bet.buttons_panel.cashout_button.click()
        self.assertTrue(bet.cash_out_successful_message is not None, msg='Cash Out is not successful')

    def test_006_verify_location_of_odds_displayed_for_the_single_bets_in_settled_tab(self):
        """
        DESCRIPTION: Verify location of Odds displayed for the single bets in Settled tab
        EXPECTED: Location of the Odds at selection level to be placed on the right hand side. Should be displayed as per figma
        """
        self.site.open_my_bets_settled_bets()
        settled_bet = [
            list(self.site.settled_bets.tab_content.accordions_list.n_items_as_ordered_dict(no_of_items=1).values())[0]]
        self.verify_my_bets_odds_location(bets=list(settled_bet), tab_name='Settled tab')

    def test_007_repeat_step_4_6__by_placing_single_bets_for_tier1_and_tier2_sports(self):
        """
        DESCRIPTION: Repeat step 4-6  by placing single bets for tier1 and tier2 Sports
        EXPECTED: Result should be same
        """
        self.__class__.expected_betslip_counter_value = 0
        self.open_betslip_with_selections(selection_ids=self.tier2_selection_ids[0])
        self.place_single_bet()
        self.check_bet_receipt_is_displayed()

        self.test_004_verify_location_of_odds_displayed_for_the_single_bets_in_open_tab()
        self.test_005_verify_location_of_odds_displayed_for_the_single_bets_in_cash_out_tab()
        self.test_006_verify_location_of_odds_displayed_for_the_single_bets_in_settled_tab()

    def test_008_repeat_step_4_6_for_horseracing_single_bets(self):
        """
        DESCRIPTION: Repeat step 4-6 for Horseracing single bets
        EXPECTED: Result should be same
        EXPECTED: ![](index.php?/attachments/get/9dcb5a39-5ffd-4491-8681-1af090b0b74d)
        """
        self.__class__.expected_betslip_counter_value = 0
        self.open_betslip_with_selections(selection_ids=self.selection_ids)
        sections = self.get_betslip_sections(multiples=True).Multiples
        self.assertIn(vec.betslip.DBL, sections.keys(),
                      msg=f'No "{vec.betslip.DBL}" stake was found in "{sections.keys()}"')
        self.place_multiple_bet(stake_name=vec.betslip.DBL)
        self.check_bet_receipt_is_displayed()

        self.site.open_my_bets_open_bets()
        open_bet = \
        list(self.site.open_bets.tab_content.accordions_list.n_items_as_ordered_dict(no_of_items=1).values())[0]
        open_tab_double_bets = list(open_bet.items_as_ordered_dict.values())
        self.verify_my_bets_odds_location(bets=open_tab_double_bets, tab_name='Open tab')

        self.site.open_my_bets_cashout()
        cash_out_bet = \
        list(self.site.cashout.tab_content.accordions_list.n_items_as_ordered_dict(no_of_items=1).values())[0]
        cash_out_tab_double_bets = list(cash_out_bet.items_as_ordered_dict.values())
        self.verify_my_bets_odds_location(bets=cash_out_tab_double_bets, tab_name='Cash Out tab')

        cash_out_bet.buttons_panel.full_cashout_button.click()
        cash_out_bet.buttons_panel.cashout_button.click()
        self.assertTrue(cash_out_bet.cash_out_successful_message is not None, msg='Cash Out is not successful')

        self.site.open_my_bets_settled_bets()
        settled_bet = \
        list(self.site.settled_bets.tab_content.accordions_list.n_items_as_ordered_dict(no_of_items=1).values())[0]
        settled_tab_double_bets = list(settled_bet.items_as_ordered_dict.values())
        self.verify_my_bets_odds_location(bets=settled_tab_double_bets, tab_name='Settled tab')

        self.__class__.expected_betslip_counter_value = 0
        self.open_betslip_with_selections(selection_ids=self.tier2_selection_ids)
        sections = self.get_betslip_sections(multiples=True).Multiples
        self.assertIn(vec.betslip.DBL, sections.keys(),
                      msg=f'No "{vec.betslip.DBL}" stake was found in "{sections.keys()}"')
        self.place_multiple_bet(stake_name=vec.betslip.DBL)
        self.check_bet_receipt_is_displayed()

        self.site.open_my_bets_open_bets()
        open_bet = \
        list(self.site.open_bets.tab_content.accordions_list.n_items_as_ordered_dict(no_of_items=1).values())[0]
        open_tab_double_bets = list(open_bet.items_as_ordered_dict.values())
        self.verify_my_bets_odds_location(bets=open_tab_double_bets, tab_name='Open tab')

        self.site.open_my_bets_cashout()
        cash_out_bet = \
        list(self.site.cashout.tab_content.accordions_list.n_items_as_ordered_dict(no_of_items=1).values())[0]
        cash_out_tab_double_bets = list(cash_out_bet.items_as_ordered_dict.values())
        self.verify_my_bets_odds_location(bets=cash_out_tab_double_bets, tab_name='Cash Out tab')

        cash_out_bet.buttons_panel.full_cashout_button.click()
        cash_out_bet.buttons_panel.cashout_button.click()
        self.assertTrue(cash_out_bet.cash_out_successful_message is not None, msg='Cash Out is not successful')

        self.site.open_my_bets_settled_bets()
        settled_bet = \
        list(self.site.settled_bets.tab_content.accordions_list.n_items_as_ordered_dict(no_of_items=1).values())[0]
        settled_tab_double_bets = list(settled_bet.items_as_ordered_dict.values())
        self.verify_my_bets_odds_location(bets=settled_tab_double_bets, tab_name='Settled tab')